import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  FileText, CheckCircle, AlertTriangle, ArrowRight, Download, Printer,
  Sparkles, RefreshCw, Eye, BookOpen, Layers
} from 'lucide-react';
import confetti from 'canvas-confetti';

import { api } from '../services/api';
import { translations } from '../utils/translations';
import VoiceControl from '../components/VoiceControl';
import ConflictBanner from '../components/ConflictBanner';
import DocumentChecklist from '../components/DocumentChecklist';

export default function DigitalAssistant({
  language,
  speechHook
}) {
  const [searchParams] = useSearchParams();
  const [session, setSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [serviceInfo, setServiceInfo] = useState(null);
  const [conflicts, setConflicts] = useState([]);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [pdfReadyUrl, setPdfReadyUrl] = useState(null);

  const t = translations[language] || translations.en;
  const { isListening, transcript, setTranscript, startListening, stopListening, speak } = speechHook;

  // Initialize Session
  useEffect(() => {
    initSession();
  }, [language]);

  const initSession = async () => {
    try {
      setLoading(true);
      const newSession = await api.createSession('digital', language);
      setSession(newSession);
      
      const welcomeText = t.welcomeDigital || "Hello! I am your FormSaathi AI Assistant. Tell me what service or scholarship you need help with.";

      const initMsg = {
        role: 'assistant',
        content: welcomeText
      };
      setMessages([initMsg]);
      speak(welcomeText, language);

      // Check URL demo param
      const demoParam = searchParams.get('demo');
      if (demoParam === 'scholarship') {
        setTimeout(() => {
          const demoInput = language === 'hi'
            ? "मुझे स्कॉलरशिप के लिए अप्लाई करना है। मैं बी.टेक छात्र हूँ।"
            : language === 'te'
            ? "Naaku scholarship apply cheyyali. Nenu B.Tech student ni."
            : "I want to apply for student scholarship. I am a B.Tech student.";
          handleSendMessage(demoInput, newSession.session_id);
        }, 800);
      } else if (demoParam === 'conflict') {
        setTimeout(() => {
          triggerConflictDemo(newSession.session_id);
        }, 800);
      }
    } catch (e) {
      console.error("Init session error:", e);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (text, activeSessionId = null) => {
    const sId = activeSessionId || session?.session_id;
    if (!sId || !text.trim()) return;

    // Add user message to UI
    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await api.sendMessage(text, language, sId);
      
      if (res.session) {
        setSession(res.session);
        setFormData(res.session.form_data || {});
        setConflicts(res.session.conflicts || []);
      }

      // Add assistant response
      const botMsg = { role: 'assistant', content: res.reply_text };
      setMessages(prev => [...prev, botMsg]);

      // Speak prompt aloud
      if (res.audio_prompt) {
        speak(res.audio_prompt, language);
      }

      // If intent matched a service, fetch full service schema
      if (res.service_id) {
        const services = await api.getServices();
        const matched = services.find(s => s.service_id === res.service_id);
        if (matched) setServiceInfo(matched);
      }

    } catch (e) {
      console.error("Chat error:", e);
      const errMsg = {
        role: 'assistant',
        content: "Error communicating with server. Please try again."
      };
      setMessages(prev => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  // Upload Supporting Document
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
      const verifiedName = res.ocr_result?.doc_name || "Document";
      const reply = `✅ **${verifiedName}** ${t.verified} (OCR Ready).`;
      
      setMessages(prev => [...prev, { role: 'assistant', content: reply }]);
      speak(reply, language);
    } catch (e) {
      console.error("Doc upload error:", e);
    } finally {
      setLoading(false);
    }
  };

  // 1-Click Sample Document Demo
  const handleUseSampleDoc = async (sampleType) => {
    if (!session?.session_id) return;
    const filename = sampleType === 'aadhaar' ? 'sample_aadhaar.jpg' : 'sample_income_cert.jpg';
    try {
      setLoading(true);
      const fileRes = await fetch(`/static/samples/${filename}`);
      const blob = await fileRes.blob();
      const mockFile = new File([blob], filename, { type: 'image/jpeg' });
      await handleUploadDoc(mockFile, sampleType);
    } catch (e) {
      console.error("Sample doc error:", e);
    }
  };

  // Conflict Resolution
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
      console.error("Conflict resolution error:", e);
    }
  };

  // Generate Final PDF
  const handleGeneratePdf = async () => {
    if (!session?.session_id) return;
    try {
      setLoading(true);
      const res = await api.generateDigitalPdf(session.session_id);
      if (res.pdf_url) {
        setPdfReadyUrl(res.pdf_url);
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
        const readyMsg = `${t.readyTitle} ${t.downloadPdf}`;
        setMessages(prev => [...prev, { role: 'assistant', content: readyMsg }]);
        speak(readyMsg, language);
      }
    } catch (e) {
      console.error("PDF generation error:", e);
    } finally {
      setLoading(false);
    }
  };

  // Conflict Demo Preset
  const triggerConflictDemo = async (sId) => {
    const prompt1 = language === 'hi' ? "मुझे स्कॉलरशिप के लिए अप्लाई करना है" : "Naaku scholarship apply cheyyali";
    await handleSendMessage(prompt1, sId);
    setTimeout(async () => {
      await handleSendMessage("Sai Praneetha", sId);
      setTimeout(async () => {
        // User states DOB as 15/06/2006
        await handleSendMessage("15/06/2006", sId);
        setTimeout(async () => {
          // Then upload sample Aadhaar which has 15/06/2005!
          await handleUseSampleDoc('aadhaar');
        }, 1200);
      }, 1000);
    }, 1000);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
      
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <span className="text-xs font-black uppercase tracking-wider text-indigo-700 bg-indigo-50 border border-indigo-200 px-3 py-1 rounded-full">
            Mode 1 — {t.navDigital}
          </span>
          <h1 className="text-3xl sm:text-4xl font-black text-slate-900 mt-2">
            {serviceInfo ? (serviceInfo[`title_${language}`] || serviceInfo.title_en) : t.navDigital}
          </h1>
          <p className="text-sm text-slate-500 font-medium mt-1">
            Voice-first guidance with document OCR and conflict resolution
          </p>
        </div>

        <button
          onClick={initSession}
          className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl flex items-center gap-2 self-start sm:self-auto transition-colors"
        >
          <RefreshCw className="w-4 h-4" /> Start Fresh
        </button>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Conversational Voice Feed (7 cols) */}
        <div className="lg:col-span-7 flex flex-col space-y-6">
          
          {/* Messages Feed */}
          <div className="bg-white rounded-3xl p-6 shadow-md border border-slate-200 min-h-[420px] max-h-[550px] overflow-y-auto space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-3xl p-4 sm:p-5 shadow-xs text-sm sm:text-base ${
                    msg.role === 'user'
                      ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-tr-xs font-medium'
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
                  <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"></span>
                  <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                  <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                  <span>FormSaathi is thinking...</span>
                </div>
              </div>
            )}
          </div>

          {/* Voice & Input Controls with language-specific suggestions */}
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
              "Scholarship",
              "Sai Praneetha",
              "15/06/2005",
              "B.Tech",
              "Yes",
              "No"
            ]}
          />

        </div>

        {/* Right Column: Documents, Conflicts, Live Preview (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Conflict Banner */}
          <ConflictBanner
            conflicts={conflicts}
            onResolve={handleResolveConflict}
            language={language}
          />

          {/* Document Checklist */}
          <DocumentChecklist
            uploadedDocs={session?.uploaded_documents || []}
            missingDocs={session?.missing_documents || (serviceInfo ? serviceInfo.required_documents.map(d => d[`name_${language}`] || d.name_en) : [])}
            onUploadDoc={handleUploadDoc}
            onUseSampleDoc={handleUseSampleDoc}
            language={language}
          />

          {/* Live Form Values & Preview Card */}
          <div className="bg-white rounded-3xl p-6 shadow-md border border-slate-200">
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
              <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
                <Layers className="w-5 h-5 text-indigo-600" />
                {t.previewTitle}
              </h3>
              <span className="text-xs bg-indigo-50 text-indigo-700 font-bold px-2.5 py-1 rounded-full">
                {Object.keys(formData).length} Fields Filled
              </span>
            </div>

            {Object.keys(formData).length === 0 ? (
              <p className="text-xs text-slate-400 italic">
                Speak or answer questions to see live autofill data...
              </p>
            ) : (
              <div className="space-y-2.5 max-h-[220px] overflow-y-auto pr-1">
                {Object.entries(formData).map(([k, v]) => (
                  <div key={k} className="flex justify-between items-center text-xs p-2 bg-slate-50 rounded-xl">
                    <span className="font-bold text-slate-600 capitalize">{k.replace('_', ' ')}:</span>
                    <span className="font-extrabold text-indigo-950 text-right truncate max-w-[180px]">{String(v)}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Final Action Button */}
            <div className="mt-6 pt-4 border-t border-slate-100 space-y-3">
              {pdfReadyUrl ? (
                <div className="flex gap-2">
                  <a
                    href={pdfReadyUrl}
                    download="FormSaathi_Application.pdf"
                    className="flex-1 py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-2xl text-center text-sm font-extrabold flex items-center justify-center gap-2 shadow-md transition-colors"
                  >
                    <Download className="w-4 h-4" /> {t.downloadPdf}
                  </a>
                  <button
                    onClick={() => window.open(pdfReadyUrl, '_blank')}
                    className="p-3 bg-slate-900 text-white rounded-2xl hover:bg-slate-800 transition-colors"
                    title={t.printPdf}
                  >
                    <Printer className="w-5 h-5" />
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={handleGeneratePdf}
                  disabled={Object.keys(formData).length < 2 || loading}
                  className="w-full py-4 bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-700 hover:to-indigo-900 disabled:opacity-40 text-white rounded-2xl text-base font-extrabold flex items-center justify-center gap-2 shadow-lg transition-all transform active:scale-95"
                >
                  <Sparkles className="w-5 h-5 text-amber-300" />
                  {t.confirmAndGenerate}
                </button>
              )}
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
