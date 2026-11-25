import React, { useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Volume2, Globe, FileText, Sparkles, History, Camera, ChevronDown, Check } from 'lucide-react';
import { translations, SUPPORTED_LANGUAGES } from '../utils/translations';

export default function Navbar({ language, setLanguage, isSpeaking, stopSpeaking }) {
  const t = translations[language] || translations.en;
  const location = useLocation();
  const [langMenuOpen, setLangMenuOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setLangMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const currentLangObj = SUPPORTED_LANGUAGES.find(l => l.code === language) || SUPPORTED_LANGUAGES[0];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          
          {/* Logo & Pan-Indian Tagline (No single regional language in top-left) */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-500 via-orange-600 to-indigo-700 flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform">
              <Sparkles className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-slate-900 to-indigo-950 bg-clip-text text-transparent">
                  FormSaathi
                </span>
                <span className="text-xs bg-indigo-50 text-indigo-900 font-bold px-2 py-0.5 rounded-full border border-indigo-200 flex items-center gap-1 shadow-2xs">
                  <span>🇮🇳</span> All India Edition
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block font-medium">
                Voice-First AI Citizen Assistant for All Indian Languages
              </p>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-2">
            <Link
              to="/digital"
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-colors flex items-center gap-2 ${
                location.pathname === '/digital'
                  ? 'bg-indigo-50 text-indigo-700 border border-indigo-200'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <FileText className="w-4 h-4" />
              {t.navDigital}
            </Link>

            <Link
              to="/physical"
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-colors flex items-center gap-2 ${
                location.pathname === '/physical'
                  ? 'bg-amber-50 text-amber-800 border border-amber-200'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Camera className="w-4 h-4" />
              {t.navPhysical}
            </Link>

            <Link
              to="/history"
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-colors flex items-center gap-2 ${
                location.pathname === '/history'
                  ? 'bg-slate-100 text-slate-900'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <History className="w-4 h-4" />
              {t.navHistory}
            </Link>
          </nav>

          {/* Controls: Audio status & All-India Language Dropdown */}
          <div className="flex items-center gap-3">
            {isSpeaking && (
              <button
                onClick={stopSpeaking}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-rose-50 text-rose-700 border border-rose-200 rounded-full text-xs font-bold animate-pulse"
                title="Stop audio playback"
              >
                <Volume2 className="w-4 h-4 text-rose-600" />
                <span>Speaking... Stop</span>
              </button>
            )}

            {/* All-India Language Selector Dropdown */}
            <div className="relative" ref={dropdownRef}>
              <button
                type="button"
                onClick={() => setLangMenuOpen(!langMenuOpen)}
                className="flex items-center gap-2 px-3 py-2 bg-slate-50 hover:bg-slate-100 text-slate-800 rounded-xl border border-slate-300 font-bold text-sm shadow-xs transition-colors"
                title="Choose Indian Language"
              >
                <Globe className="w-4 h-4 text-indigo-600" />
                <span>{currentLangObj.label}</span>
                <span className="text-xs text-slate-400 font-normal">({currentLangObj.englishName})</span>
                <ChevronDown className={`w-3.5 h-3.5 text-slate-500 transition-transform ${langMenuOpen ? 'rotate-180' : ''}`} />
              </button>

              {/* Language Dropdown Menu */}
              {langMenuOpen && (
                <div className="absolute right-0 mt-2 w-64 bg-white rounded-2xl shadow-2xl border border-slate-200 py-2 z-50 max-h-96 overflow-y-auto">
                  <div className="px-3 py-1.5 border-b border-slate-100 text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                    <span>🇮🇳</span> Select Your Language
                  </div>

                  {SUPPORTED_LANGUAGES.map((langItem) => {
                    const isSelected = language === langItem.code;
                    return (
                      <button
                        key={langItem.code}
                        type="button"
                        onClick={() => {
                          setLanguage(langItem.code);
                          setLangMenuOpen(false);
                        }}
                        className={`w-full px-4 py-2.5 text-left text-sm flex items-center justify-between hover:bg-indigo-50 transition-colors ${
                          isSelected ? 'bg-indigo-50/80 font-bold text-indigo-900' : 'text-slate-700 font-medium'
                        }`}
                      >
                        <div className="flex items-center gap-2.5">
                          <span className="text-base">{langItem.flag}</span>
                          <div>
                            <span className="font-extrabold">{langItem.label}</span>
                            <span className="text-xs text-slate-500 ml-2">({langItem.englishName})</span>
                          </div>
                        </div>
                        {isSelected && <Check className="w-4 h-4 text-indigo-600" />}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

          </div>

        </div>
      </div>
    </header>
  );
}
