import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import DigitalAssistant from './pages/DigitalAssistant';
import PhysicalFormAssistant from './pages/PhysicalFormAssistant';
import ApplicationHistory from './pages/ApplicationHistory';
import { useSpeech } from './hooks/useSpeech';

export default function App() {
  const [language, setLanguage] = useState('hi'); // Default to Hindi (Pan-India)
  const speechHook = useSpeech(language);

  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 selection:bg-amber-200">
        
        {/* Navigation Bar */}
        <Navbar
          language={language}
          setLanguage={setLanguage}
          isSpeaking={speechHook.isSpeaking}
          stopSpeaking={speechHook.stopSpeaking}
        />

        {/* Main Content Pages */}
        <main className="flex-1">
          <Routes>
            <Route
              path="/"
              element={<Home language={language} onStartVoiceDemo={() => {}} />}
            />
            <Route
              path="/digital"
              element={
                <DigitalAssistant
                  language={language}
                  speechHook={speechHook}
                />
              }
            />
            <Route
              path="/physical"
              element={
                <PhysicalFormAssistant
                  language={language}
                  speechHook={speechHook}
                />
              }
            />
            <Route
              path="/history"
              element={<ApplicationHistory language={language} />}
            />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-slate-200 py-8 px-4 sm:px-6 lg:px-8 mt-12">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
            <div>
              <p className="font-extrabold text-slate-900 text-sm">
                FormSaathi — Multilingual Voice-First Citizen AI Agent for All Indians
              </p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">
                "Tell us what you need. Show us the form. FormSaathi helps you complete the rest."
              </p>
            </div>

            <div className="flex items-center gap-2 text-xs font-bold text-slate-600 bg-slate-100 px-3.5 py-1.5 rounded-full border border-slate-200">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>Available in all major Indian Languages</span>
            </div>
          </div>
        </footer>

      </div>
    </BrowserRouter>
  );
}
