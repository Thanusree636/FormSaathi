import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Send, Sparkles } from 'lucide-react';
import { translations } from '../utils/translations';

export default function VoiceControl({
  onSendMessage,
  isListening,
  startListening,
  stopListening,
  transcript,
  setTranscript,
  language = 'te',
  disabled = false,
  quickSuggestions = []
}) {
  const [inputText, setInputText] = useState('');
  const t = translations[language] || translations.en;

  useEffect(() => {
    if (transcript) {
      setInputText(transcript);
    }
  }, [transcript]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (inputText.trim() && !disabled) {
      onSendMessage(inputText.trim());
      setInputText('');
      setTranscript('');
      if (isListening) stopListening();
    }
  };

  const toggleMic = () => {
    if (isListening) {
      stopListening();
      if (inputText.trim()) {
        handleSubmit();
      }
    } else {
      startListening(language);
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-lg border-2 border-indigo-100 p-4 sm:p-6 transition-all">
      
      {/* Voice Status Indicator Banner */}
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <div className={`w-3.5 h-3.5 rounded-full ${isListening ? 'bg-red-500 animate-ping' : 'bg-emerald-500'}`} />
          <span className="text-sm font-bold text-slate-700">
            {isListening ? t.listening : t.clickToSpeak}
          </span>
        </div>

        {isListening && (
          <div className="flex items-center gap-1">
            <span className="w-1.5 h-6 bg-red-500 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
            <span className="w-1.5 h-8 bg-red-600 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
            <span className="w-1.5 h-10 bg-red-500 rounded-full animate-bounce"></span>
            <span className="w-1.5 h-7 bg-red-600 rounded-full animate-bounce [animation-delay:-0.2s]"></span>
          </div>
        )}
      </div>

      {/* Main Input Form */}
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 items-center">
        
        {/* Large Accessible Mic Button */}
        <button
          type="button"
          onClick={toggleMic}
          disabled={disabled}
          className={`w-16 h-16 sm:w-20 sm:h-20 rounded-2xl flex flex-col items-center justify-center shrink-0 transition-all duration-300 transform active:scale-95 shadow-md ${
            isListening
              ? 'bg-red-600 text-white pulse-ring'
              : 'bg-gradient-to-tr from-indigo-600 to-indigo-800 text-white hover:shadow-indigo-200 hover:shadow-xl'
          } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
          title={isListening ? "Stop listening" : "Start speaking"}
        >
          {isListening ? <MicOff className="w-8 h-8" /> : <Mic className="w-8 h-8" />}
          <span className="text-[10px] uppercase font-black tracking-wider mt-1">
            {isListening ? 'STOP' : 'SPEAK'}
          </span>
        </button>

        {/* Text Input Box */}
        <div className="flex-1 w-full relative">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={disabled}
            placeholder={isListening ? t.listening : t.typePlaceholder}
            className={`w-full py-4 pl-5 pr-14 rounded-2xl border-2 text-base sm:text-lg focus:outline-hidden transition-all ${
              isListening
                ? 'border-red-400 bg-red-50/30'
                : 'border-slate-200 focus:border-indigo-600 bg-slate-50/50 focus:bg-white'
            }`}
          />

          <button
            type="submit"
            disabled={disabled || !inputText.trim()}
            className="absolute right-2.5 top-1/2 -translate-y-1/2 p-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            title={t.send}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>

      {/* Quick Suggestions for Hackathon Demos */}
      {quickSuggestions.length > 0 && (
        <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold text-slate-500 flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            Quick answers:
          </span>
          {quickSuggestions.map((item, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setInputText(item);
                onSendMessage(item);
              }}
              className="text-xs bg-slate-100 hover:bg-indigo-50 hover:text-indigo-700 hover:border-indigo-200 border border-slate-200 px-3 py-1.5 rounded-full font-semibold transition-all"
            >
              {item}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
