/**
 * FormSaathi API Service Client
 */

const API_BASE = '/api';

export const api = {
  // Session
  createSession: async (mode = 'digital', language = 'te', serviceId = null) => {
    const res = await fetch(`${API_BASE}/session/create?mode=${mode}&language=${language}${serviceId ? `&service_id=${serviceId}` : ''}`, {
      method: 'POST'
    });
    return res.json();
  },

  getSession: async (sessionId) => {
    const res = await fetch(`${API_BASE}/session/${sessionId}`);
    return res.json();
  },

  // Conversational Chat
  sendMessage: async (userInput, language = 'te', sessionId = null) => {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_input: userInput,
        language,
        session_id: sessionId
      })
    });
    return res.json();
  },

  // Physical Form Upload
  uploadPhysicalForm: async (sessionId, file, language = 'te') => {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('language', language);
    formData.append('file', file);

    const res = await fetch(`${API_BASE}/forms/upload-physical`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  },

  // Supporting Document Upload & OCR
  uploadDocument: async (sessionId, file, docHint = null, language = 'te') => {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('language', language);
    if (docHint) formData.append('doc_hint', docHint);
    formData.append('file', file);

    const res = await fetch(`${API_BASE}/documents/upload-doc`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  },

  // Conflict Resolution
  resolveConflict: async (sessionId, fieldId, selectedValue, sourceChoice = 'custom') => {
    const res = await fetch(`${API_BASE}/validation/resolve-conflict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        field_id: fieldId,
        selected_value: selectedValue,
        source_choice: sourceChoice
      })
    });
    return res.json();
  },

  // Physical Form Overlay & PDF
  fillPhysicalForm: async (sessionId) => {
    const formData = new FormData();
    formData.append('session_id', sessionId);

    const res = await fetch(`${API_BASE}/forms/fill-physical`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  },

  // Digital Form PDF
  generateDigitalPdf: async (sessionId) => {
    const formData = new FormData();
    formData.append('session_id', sessionId);

    const res = await fetch(`${API_BASE}/forms/generate-digital-pdf`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  },

  // Services & Applications
  getServices: async () => {
    const res = await fetch(`${API_BASE}/services`);
    return res.json();
  },

  getApplications: async () => {
    const res = await fetch(`${API_BASE}/applications/history`);
    return res.json();
  }
};
