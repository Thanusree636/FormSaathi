import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Custom React hook for Voice-First Interaction across ALL Major Indian Languages:
 * Hindi, English, Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia.
 */
export const LANGUAGE_LOCALE_MAP = {
  hi: 'hi-IN',
  en: 'en-IN',
  te: 'te-IN',
  ta: 'ta-IN',
  kn: 'kn-IN',
  ml: 'ml-IN',
  mr: 'mr-IN',
  bn: 'bn-IN',
  gu: 'gu-IN',
  pa: 'pa-IN',
  or: 'or-IN'
};

export const useSpeech = (defaultLang = 'hi') => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      setSpeechSupported(true);
      const recog = new SpeechRecognition();
      recog.continuous = false;
      recog.interimResults = true;
      recog.maxAlternatives = 1;

      recog.onresult = (event) => {
        let currentTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          currentTranscript += event.results[i][0].transcript;
        }
        setTranscript(currentTranscript);
      };

      recog.onerror = (event) => {
        console.warn('[Speech] Recognition error:', event.error);
        setIsListening(false);
      };

      recog.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recog;
    } else {
      console.warn('[Speech] Web Speech API not supported in this browser.');
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const getLocale = (lang) => LANGUAGE_LOCALE_MAP[lang] || 'en-IN';

  const startListening = useCallback((lang = defaultLang) => {
    if (!recognitionRef.current) return;
    setTranscript('');
    try {
      recognitionRef.current.lang = getLocale(lang);
      recognitionRef.current.start();
      setIsListening(true);
    } catch (e) {
      console.warn('[Speech] Could not start speech recognition:', e);
    }
  }, [defaultLang]);

  const stopListening = useCallback(() => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  }, [isListening]);

  const speak = useCallback((text, lang = defaultLang) => {
    if (!('speechSynthesis' in window) || !text) return;

    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[*#_`]/g, ''); // strip markdown formatting for cleaner speech
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = getLocale(lang);
    utterance.rate = 0.95; // comfortable, natural pace for citizens
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  }, [defaultLang]);

  const stopSpeaking = useCallback(() => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  }, []);

  return {
    isListening,
    transcript,
    setTranscript,
    startListening,
    stopListening,
    isSpeaking,
    speak,
    stopSpeaking,
    speechSupported
  };
};
