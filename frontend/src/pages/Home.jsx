import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Mic, Camera, FileText, Upload, Sparkles, ArrowRight,
  ShieldCheck, CheckCircle2, UserCheck, BookOpen, AlertTriangle
} from 'lucide-react';
import { translations } from '../utils/translations';

export default function Home({ language }) {
  const navigate = useNavigate();
  const t = translations[language] || translations.en;

  const targetUsers = [
    { icon: "👴", title: "Elderly Citizens", desc: "No complex portals or typing. Just speak naturally in your mother tongue." },
    { icon: "🌾", title: "Rural Citizens", desc: "Complete forms in your local language with voice guidance." },
    { icon: "👩‍🎓", title: "Students", desc: "Instant scholarship, college admission, and fee assistance." },
    { icon: "👨‍🌾", title: "Farmers", desc: "Easy access to welfare schemes, subsidies, and land certificates." },
    { icon: "👷", title: "Workers", desc: "Welfare scheme enrollment and benefit applications." },
    { icon: "👨‍👩‍👧", title: "Family Helpers", desc: "Assist parents and grandparents to complete paper forms." },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      
      {/* Hero Section */}
      <div className="text-center max-w-4xl mx-auto mb-12">
        <div className="inline-flex items-center gap-2 bg-gradient-to-r from-amber-50 to-indigo-50 border border-indigo-200 px-4 py-2 rounded-full text-indigo-900 text-xs sm:text-sm font-extrabold mb-6 shadow-xs">
          <Sparkles className="w-4 h-4 text-amber-500" />
          <span>Multilingual Voice-First Citizen AI Agent for All Indians</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black text-slate-900 tracking-tight leading-tight">
          Tell us what you need. <br />
          <span className="bg-gradient-to-r from-indigo-700 via-purple-700 to-amber-600 bg-clip-text text-transparent">
            Show us the form.
          </span> <br />
          FormSaathi helps you complete the rest.
        </h1>

        <p className="mt-6 text-lg sm:text-xl text-slate-600 font-medium max-w-2xl mx-auto">
          {t.tagline}
        </p>

        {/* Hackathon Quick Demo Preset Buttons */}
        <div className="mt-8 p-4 bg-slate-900 text-white rounded-3xl shadow-xl flex flex-col sm:flex-row items-center justify-center gap-3">
          <span className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles className="w-4 h-4" /> Quick Hackathon Demos:
          </span>
          <button
            onClick={() => navigate('/digital?demo=scholarship')}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-xl text-xs sm:text-sm font-bold transition-all flex items-center gap-1.5"
          >
            {t.demoA}
          </button>
          <button
            onClick={() => navigate('/physical?demo=bank')}
            className="px-4 py-2 bg-amber-600 hover:bg-amber-500 rounded-xl text-xs sm:text-sm font-bold transition-all flex items-center gap-1.5"
          >
            {t.demoB}
          </button>
          <button
            onClick={() => navigate('/digital?demo=conflict')}
            className="px-4 py-2 bg-rose-700 hover:bg-rose-600 rounded-xl text-xs sm:text-sm font-bold transition-all flex items-center gap-1.5"
          >
            {t.demoConflict}
          </button>
        </div>
      </div>

      {/* Main Action Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
        
        {/* Button 1: Speak */}
        <div
          onClick={() => navigate('/digital')}
          className="bg-gradient-to-br from-indigo-600 to-indigo-800 text-white p-7 rounded-3xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all cursor-pointer group flex flex-col justify-between"
        >
          <div>
            <div className="w-16 h-16 rounded-2xl bg-white/10 flex items-center justify-center mb-5 group-hover:scale-110 transition-transform">
              <Mic className="w-9 h-9 text-amber-300" />
            </div>
            <h3 className="text-2xl font-black mb-2">{t.speakBtn}</h3>
            <p className="text-indigo-100 text-sm font-medium">
              Speak in any Indian language. Tell us what scheme or certificate you need.
            </p>
          </div>
          <div className="mt-6 flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-amber-300">
            Start Talking <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        {/* Button 2: Upload Physical Form */}
        <div
          onClick={() => navigate('/physical')}
          className="bg-gradient-to-br from-amber-500 to-orange-600 text-white p-7 rounded-3xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all cursor-pointer group flex flex-col justify-between"
        >
          <div>
            <div className="w-16 h-16 rounded-2xl bg-white/10 flex items-center justify-center mb-5 group-hover:scale-110 transition-transform">
              <Camera className="w-9 h-9 text-white" />
            </div>
            <h3 className="text-2xl font-black mb-2">{t.uploadFormBtn}</h3>
            <p className="text-amber-50 text-sm font-medium">
              Upload a bank or paper form. We detect fields and preserve original layout.
            </p>
          </div>
          <div className="mt-6 flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-white">
            Upload Paper Form <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        {/* Button 3: Start Application */}
        <div
          onClick={() => navigate('/digital')}
          className="bg-white border-2 border-slate-200 hover:border-indigo-600 p-7 rounded-3xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer group flex flex-col justify-between"
        >
          <div>
            <div className="w-16 h-16 rounded-2xl bg-indigo-50 text-indigo-700 flex items-center justify-center mb-5 group-hover:scale-110 transition-transform">
              <FileText className="w-9 h-9" />
            </div>
            <h3 className="text-2xl font-black text-slate-900 mb-2">{t.startAppBtn}</h3>
            <p className="text-slate-600 text-sm font-medium">
              Step-by-step conversational guidance. No complex 30-field pages.
            </p>
          </div>
          <div className="mt-6 flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-indigo-600">
            View Services <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

        {/* Button 4: Upload Documents */}
        <div
          onClick={() => navigate('/digital')}
          className="bg-white border-2 border-slate-200 hover:border-emerald-500 p-7 rounded-3xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer group flex flex-col justify-between"
        >
          <div>
            <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-700 flex items-center justify-center mb-5 group-hover:scale-110 transition-transform">
              <Upload className="w-9 h-9" />
            </div>
            <h3 className="text-2xl font-black text-slate-900 mb-2">{t.uploadDocsBtn}</h3>
            <p className="text-slate-600 text-sm font-medium">
              OCR extracts Aadhaar, Income certificate, College ID with conflict checking.
            </p>
          </div>
          <div className="mt-6 flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-emerald-700">
            Check KYC Docs <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

      </div>

      {/* Target Users Showcase */}
      <div className="mb-16">
        <div className="text-center mb-8">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            Designed for Citizens Across All of India
          </h2>
          <p className="text-slate-500 text-sm sm:text-base font-medium mt-1">
            Empowering everyone in their own language regardless of digital literacy
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {targetUsers.map((user, idx) => (
            <div
              key={idx}
              className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs flex items-start gap-4 hover:border-indigo-300 transition-colors"
            >
              <div className="text-4xl p-3 bg-slate-50 rounded-2xl shrink-0">
                {user.icon}
              </div>
              <div>
                <h4 className="font-extrabold text-lg text-slate-900">{user.title}</h4>
                <p className="text-sm text-slate-600 mt-1 font-medium">{user.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Two Modes Workflow Visualizer */}
      <div className="bg-slate-900 text-white rounded-3xl p-8 sm:p-12 shadow-2xl mb-12">
        <h2 className="text-2xl sm:text-3xl font-black text-center mb-10">
          Two Breakthrough Workflows
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* Mode 1 Card */}
          <div className="bg-slate-800/80 p-6 sm:p-8 rounded-3xl border border-slate-700">
            <span className="text-xs bg-indigo-500/20 text-indigo-300 font-bold px-3 py-1 rounded-full uppercase tracking-wider">
              Mode 1
            </span>
            <h3 className="text-2xl font-black mt-3 mb-2 text-indigo-300">
              Digital Application Assistant
            </h3>
            <p className="text-slate-300 text-sm mb-6 font-medium">
              Speak or type in your language: <i>"मुझे छात्रवृत्ति के लिए आवेदन करना है" / "Naaku scholarship kavali"</i>
            </p>

            <ul className="space-y-2.5 text-xs sm:text-sm text-slate-300">
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Intent & Eligibility Detection</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Sequential Multilingual Voice Questions</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Supporting Document OCR & Autofill</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Conflict Detection (DOB / Name)</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Print-Ready Application PDF</li>
            </ul>
          </div>

          {/* Mode 2 Card */}
          <div className="bg-slate-800/80 p-6 sm:p-8 rounded-3xl border border-slate-700">
            <span className="text-xs bg-amber-500/20 text-amber-300 font-bold px-3 py-1 rounded-full uppercase tracking-wider">
              Mode 2 — Differentiator
            </span>
            <h3 className="text-2xl font-black mt-3 mb-2 text-amber-300">
              Physical Paper Form Assistant
            </h3>
            <p className="text-slate-300 text-sm mb-6 font-medium">
              Elderly citizen receives complicated paper form from bank or government office.
            </p>

            <ul className="space-y-2.5 text-xs sm:text-sm text-slate-300">
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> Upload Paper Form Photo / PDF</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> Form Analysis & Field Detection</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> AI Explains Form & Asks in Your Language</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> Original Form Layout 100% Preserved</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> Filled Form Image + Print Ready PDF</li>
            </ul>
          </div>

        </div>
      </div>

    </div>
  );
}
