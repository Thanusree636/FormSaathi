import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Camera, Upload, Sparkles, CheckCircle2, AlertCircle, FileCheck,
  Download, Printer, RefreshCw, FileText, ArrowRight, Eye, ShieldCheck
} from 'lucide-react';
import confetti from 'canvas-confetti';

import { api } from '../services/api';
import { translations } from '../utils/translations';
import VoiceControl from '../components/VoiceControl';
import ConflictBanner from '../components/ConflictBanner';
import DocumentChecklist from '../components/DocumentChecklist';
import FormOverlayViewer from '../components/FormOverlayViewer';

export default function PhysicalFormAssistant({
  language,
  speechHook
}) {
  const [searchParams] = useSearchParams();
  const [session, setSession] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [messages, setMessages] = useState([]);
  const [formData, setFormData] = useState({});
  const [conflicts, setConflicts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filledImageUrl, setFilledImageUrl] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [currentStep, setCurrentStep] = useState(1); // 1: Upload, 2: Analysis & Questions, 3: Review & Filled Form

  const fileInputRef = useRef(null);
  const t = translations[language] || translations.en;
  const { isListening, transcript, setTranscript, startListening, stopListening, speak } = speechHook;

  useEffect(() => {
    initPhysicalSession();
  }, [language]);

  const initPhysicalSession = async () => {
    try {
      setLoading(true);
      const newSession = await api.createSession('physical', language, 'bank_account');
      setSession(newSession);

      const welcomeText = t.welcomePhysical || "Hello! Please upload a photo or scan of your physical bank or government form. I will analyze its fields and guide you step by step.";

      const initMsg = {
        role: 'assistant',
        content: welcomeText
      };
      setMessages([initMsg]);
      speak(welcomeText, language);

      // Check if demo query param is set
      if (searchParams.get('demo') === 'bank') {
        setTimeout(() => {
          handleUseSampleBankForm(newSession.session_id);
        }, 800);
      }
    } catch (e) {
      console.error("Init physical error:", e);
    } finally {
      setLoading(false);
    }
  };

  // Upload Physical Form
  const handleFileUpload = async (file) => {
    if (!session?.session_id) return;
    setLoading(true);
    try {
      const res = await api.uploadPhysicalForm(session.session_id, file, language);
      setSession(res.session);
      setAnalysis(res.analysis);
      setFormData(res.session.form_data || {});
      setCurrentStep(2);

      const explMsg = { role: 'assistant', content: res.explanation };
      setMessages(prev => [...prev, explMsg]);
      speak(res.explanation, language);

      // Trigger first question
      setTimeout(async () => {
        const chatRes = await api.sendMessage("Next question", language, session.session_id);
        if (chatRes.reply_text) {
          setMessages(prev => [...prev, { role: 'assistant', content: chatRes.reply_text }]);
          if (chatRes.audio_prompt) speak(chatRes.audio_prompt, language);
        }
      }, 1000);

    } catch (e) {
      console.error("Upload form error:", e);
    } finally {
      setLoading(false);
    }
  };

  // 1-Click Sample Bank Form Loader
  const handleUseSampleBankForm = async (activeSessionId = null) => {
    const sId = activeSessionId || session?.session_id;
    if (!sId) return;
    try {
      setLoading(true);
      const res = await fetch('/static/samples/bank_application_form.jpg');
      const blob = await res.blob();
      const mockFile = new File([blob], 'bank_application_form.jpg', { type: 'image/jpeg' });
      
      const uploadRes = await api.uploadPhysicalForm(sId, mockFile, language);
      setSession(uploadRes.session);
      setAnalysis(uploadRes.analysis);
      setFormData(uploadRes.session.form_data || {});
      setCurrentStep(2);

      setMessages(prev => [...prev, { role: 'assistant', content: uploadRes.explanation }]);
      speak(uploadRes.explanation, language);

      // Prompt first field
      setTimeout(async () => {
        const q1 = "👉 What is your full name as per official documents?";
        setMessages(prev => [...prev, { role: 'assistant', content: q1 }]);
        speak(q1, language);
      }, 1200);

    } catch (e) {
      console.error("Sample bank form error:", e);
    } finally {
      setLoading(false);
    }
  };

  // Chat message submission
  const handleSendMessage = async (text) => {
    if (!session?.session_id || !text.trim()) return;

    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setLoading(true);

    try {
      const res = await api.sendMessage(text, language, session.session_id);
      if (res.session) {
        setSession(res.session);
        setFormData(res.session.form_data || {});
        setConflicts(res.session.conflicts || []);
      }

      setMessages(prev => [...prev, { role: 'assistant', content: res.reply_text }]);
      if (res.audio_prompt) speak(res.audio_prompt, language);

    } catch (e) {
      console.error("Chat error:", e);
    } finally {
      setLoading(false);
    }
  };

  // Upload Supporting Document (Aadhaar / PAN)
  const handleUploadDoc = async (file, docHint = null) => {
    if (!session?.session_id) return;
    setLoading(true);
    try {
      const res = await api.uploadDocument(session.session_id, file, docHint, language);
      if (res.session) {
        setSession(res.session);
        setFormData(res.session.form_data || {});
        setConflicts(res.session.conflicts || []);
      }
      const ack = `✅ **${res.ocr_result?.doc_name}** ${t.verified}. Auto-filled to form.`;
      setMessages(prev => [...prev, { role: 'assistant', content: ack }]);
      speak(ack, language);
    } catch (e) {
      console.error("Upload doc error:", e);
    } finally {
      setLoading(false);
    }
  };

  const handleUseSampleDoc = async (sampleType) => {
    if (!session?.session_id) return;
    const filename = sampleType === 'aadhaar' ? 'sample_aadhaar.jpg' : 'sample_income_cert.jpg';
    try {
      setLoading(true);
      const res = await fetch(`/static/samples/${filename}`);
      const blob = await res.blob();
      const mockFile = new File([blob], filename, { type: 'image/jpeg' });
      await handleUploadDoc(mockFile, sampleType);
    } catch (e) {
      console.error("Sample doc error:", e);
    }
  };

  const handleResolveConflict = async (fieldId, selectedValue, sourceChoice) => {
    if (!session?.session_id) return;
    try {
      const res = await api.resolveConflict(session.session_id, fieldId, selectedValue, sourceChoice);
      if (res.session) {
        setSession(res.session);
        setFormData(res.session.form_data || {});
        setConflicts(res.session.conflicts || []);
      }
      const ack = `Confirmed: **${selectedValue}**`;
      setMessages(prev => [...prev, { role: 'assistant', content: ack }]);
      speak(ack, language);
    } catch (e) {
      console.error("Conflict error:", e);
    }
  };

  // Fill Physical Form (Overlay & PDF)
  const handleFillPhysicalForm = async () => {
    if (!session?.session_id) return;
    setLoading(true);
    try {
      const res = await api.fillPhysicalForm(session.session_id);
      if (res.success) {
        setFilledImageUrl(res.filled_image_url);
        setPdfUrl(res.pdf_url);
        setCurrentStep(3);
        confetti({ particleCount: 120, spread: 80, origin: { y: 0.6 } });

        const doneMsg = `${t.readyTitle} ${t.downloadPdf}`;
        setMessages(prev => [...prev, { role: 'assistant', content: doneMsg }]);
        speak(doneMsg, language);
      }
    } catch (e) {
      console.error("Fill physical form error:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <span className="text-xs font-black uppercase tracking-wider text-amber-900 bg-amber-100 border border-amber-300 px-3 py-1 rounded-full">
            Mode 2 — {t.navPhysical}
          </span>
          <h1 className="text-3xl sm:text-4xl font-black text-slate-900 mt-2">
            {analysis?.form_title || t.navPhysical}
          </h1>
          <p className="text-sm text-slate-500 font-medium mt-1">
            Upload paper form photo → AI detects fields & layout → Voice answers → Filled original form & PDF
          </p>
        </div>

        <button
          onClick={initPhysicalSession}
          className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl flex items-center gap-2 self-start sm:self-auto transition-colors"
        >
          <RefreshCw className="w-4 h-4" /> Start Fresh
        </button>
      </div>

      {/* Step 1: Upload or 1-Click Sample Form */}
      {currentStep === 1 && (
        <div className="bg-white rounded-3xl p-8 sm:p-12 shadow-xl border-2 border-dashed border-amber-300 text-center max-w-3xl mx-auto mb-10">
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleFileUpload(file);
            }}
            accept="image/*,application/pdf"
            className="hidden"
          />

          <div className="w-20 h-20 rounded-3xl bg-amber-100 text-amber-700 mx-auto flex items-center justify-center mb-6 shadow-inner">
            <Camera className="w-10 h-10" />
          </div>

          <h2 className="text-2xl sm:text-3xl font-black text-slate-900 mb-3">
            {t.uploadFormBtn}
          </h2>
          <p className="text-slate-600 max-w-md mx-auto text-sm sm:text-base font-medium mb-8">
            Bank account form, government office paper, or scholarship form.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => fileInputRef.current?.click()}
              className="w-full sm:w-auto px-8 py-4 bg-amber-600 hover:bg-amber-700 text-white rounded-2xl font-extrabold text-base flex items-center justify-center gap-2 shadow-lg transition-all transform active:scale-95"
            >
              <Upload className="w-5 h-5" />
              Upload Image / PDF
            </button>

            <button
              onClick={() => handleUseSampleBankForm()}
              className="w-full sm:w-auto px-6 py-4 bg-slate-900 hover:bg-slate-800 text-amber-400 rounded-2xl font-extrabold text-base flex items-center justify-center gap-2 shadow-lg border border-slate-700 transition-all transform active:scale-95"
            >
              <Sparkles className="w-5 h-5" />
              Use Sample Bank Form (1-Click Demo)
            </button>
          </div>
        </div>
      )}

      {/* Step 2 & 3: Form Analysis, Live Fields, Voice Feed, and Overlay Viewer */}
      {currentStep >= 2 && (
        <div className="space-y-8">
          
          {/* Analysis Banner */}
          {analysis && (
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-3xl p-5 sm:p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-amber-600 text-white flex items-center justify-center shrink-0 font-bold shadow-md">
                  <CheckCircle2 className="w-7 h-7" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full">
                      ✓ {t.detectedForm}
                    </span>
                    <span className="text-xs bg-indigo-100 text-indigo-800 font-bold px-2.5 py-0.5 rounded-full">
                      {analysis.fields.length} {t.detectedFields}
                    </span>
                  </div>
                  <h3 className="text-lg font-black text-slate-900 mt-1">
                    {analysis.form_title}
                  </h3>
                  <p className="text-xs text-slate-600 font-medium">
                    {analysis[`description_${language}`] || analysis.description_en}
                  </p>
                </div>
              </div>

              {/* Instructions Pill */}
              <div className="bg-white/80 p-3 rounded-2xl border border-amber-200 text-xs text-slate-700 max-w-sm">
                <span className="font-bold text-amber-900 block mb-1">Key Instructions:</span>
                <ul className="list-disc list-inside space-y-0.5">
                  {(analysis[`instructions_${language}`] || analysis.instructions_en).slice(0, 2).map((ins, i) => (
                    <li key={i} className="truncate">{ins}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Form Overlay Viewer */}
          <FormOverlayViewer
            filledImageUrl={filledImageUrl}
            originalImageUrl={session?.original_form_url || '/static/samples/bank_application_form.jpg'}
            pdfUrl={pdfUrl}
            formData={formData}
            fieldsSchema={analysis?.fields || []}
            onConfirmAndGenerate={handleFillPhysicalForm}
            language={language}
            isGenerated={Boolean(filledImageUrl)}
          />

          {/* Main Grid: Left Chat & Voice, Right Documents & Conflict */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            {/* Left: Conversational Voice Feed (7 cols) */}
            <div className="lg:col-span-7 space-y-6">
              
              <div className="bg-white rounded-3xl p-6 shadow-md border border-slate-200 min-h-[380px] max-h-[500px] overflow-y-auto space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[85%] rounded-3xl p-4 sm:p-5 shadow-xs text-sm sm:text-base ${
                        msg.role === 'user'
                          ? 'bg-gradient-to-r from-amber-600 to-amber-700 text-white rounded-tr-xs font-medium'
                          : 'bg-slate-50 text-slate-900 border border-slate-200/80 rounded-tl-xs font-medium'
                      }`}
                    >
                      <p className="whitespace-pre-line leading-relaxed">{msg.content}</p>
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-slate-100 p-4 rounded-3xl flex items-center gap-2 text-slate-500 text-sm font-semibold">
                      <span className="w-2 h-2 bg-amber-600 rounded-full animate-bounce"></span>
                      <span className="w-2 h-2 bg-amber-600 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                      <span className="w-2 h-2 bg-amber-600 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                      <span>Processing physical form...</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Voice Control */}
              <VoiceControl
                onSendMessage={handleSendMessage}
                isListening={isListening}
                startListening={startListening}
                stopListening={stopListening}
                transcript={transcript}
                setTranscript={setTranscript}
                language={language}
                disabled={loading}
                quickSuggestions={t.quickSuggestions || [
                  "Sai Praneetha",
                  "15/06/2005",
                  "Female",
                  "9876543210",
                  "Student",
                  "Yes",
                  "No"
                ]}
              />

            </div>

            {/* Right: Documents, Conflict Resolution, Fill Action (5 cols) */}
            <div className="lg:col-span-5 space-y-6">
              
              {/* Conflict Banner */}
              <ConflictBanner
                conflicts={conflicts}
                onResolve={handleResolveConflict}
                language={language}
              />

              {/* Supporting Document Checklist */}
              <DocumentChecklist
                uploadedDocs={session?.uploaded_documents || []}
                missingDocs={session?.missing_documents || (analysis ? analysis.required_documents : [])}
                onUploadDoc={handleUploadDoc}
                onUseSampleDoc={handleUseSampleDoc}
                language={language}
              />

              {/* Action Button: Fill Original Form */}
              <div className="bg-white rounded-3xl p-6 shadow-md border border-slate-200 text-center">
                <h4 className="font-extrabold text-slate-900 mb-2">
                  Complete & Fill Original Physical Form
                </h4>
                <p className="text-xs text-slate-500 mb-4 font-medium">
                  Renders answers into original bounding boxes and prepares print-ready PDF
                </p>

                <button
                  type="button"
                  onClick={handleFillPhysicalForm}
                  disabled={loading}
                  className="w-full py-4 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white rounded-2xl font-black text-base shadow-lg transition-all transform active:scale-95 flex items-center justify-center gap-2"
                >
                  <FileCheck className="w-5 h-5" />
                  Fill Original Form & Generate PDF
                </button>
              </div>

            </div>

          </div>

        </div>
      )}

    </div>
  );
}
