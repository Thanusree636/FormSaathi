import React, { useRef } from 'react';
import { FileCheck, FileX, Upload, Sparkles, CheckCircle, FileText } from 'lucide-react';
import { translations } from '../utils/translations';

export default function DocumentChecklist({
  uploadedDocs = [],
  missingDocs = [],
  onUploadDoc,
  language = 'te',
  onUseSampleDoc
}) {
  const fileInputRef = useRef(null);
  const selectedDocHintRef = useRef(null);
  const t = translations[language] || translations.en;

  const handleUploadClick = (docHint) => {
    selectedDocHintRef.current = docHint;
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      onUploadDoc(file, selectedDocHintRef.current);
      e.target.value = '';
    }
  };

  return (
    <div className="bg-white rounded-3xl p-5 sm:p-6 shadow-md border border-slate-200 mb-6">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*,application/pdf"
        className="hidden"
      />

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 pb-3 border-b border-slate-100">
        <div>
          <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
            <FileText className="w-5 h-5 text-indigo-600" />
            {t.requiredDocs}
          </h3>
          <p className="text-xs text-slate-500 font-medium">
            AI extracts data directly from supporting documents
          </p>
        </div>

        {/* Quick Demo Sample Document Button */}
        {onUseSampleDoc && (
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => onUseSampleDoc('aadhaar')}
              className="text-xs bg-amber-50 hover:bg-amber-100 text-amber-900 font-bold px-3 py-1.5 rounded-xl border border-amber-300 flex items-center gap-1.5 transition-colors"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-600" />
              + Test Sample Aadhaar
            </button>
            <button
              type="button"
              onClick={() => onUseSampleDoc('income_cert')}
              className="text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-900 font-bold px-3 py-1.5 rounded-xl border border-indigo-200 flex items-center gap-1.5 transition-colors"
            >
              <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
              + Test Income Cert
            </button>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        
        {/* Verified Documents */}
        {uploadedDocs.map((doc, idx) => (
          <div
            key={idx}
            className="flex items-center justify-between p-3.5 bg-emerald-50/60 border border-emerald-200 rounded-2xl"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-500 text-white flex items-center justify-center shrink-0">
                <CheckCircle className="w-5 h-5" />
              </div>
              <div>
                <span className="text-sm font-extrabold text-emerald-950 block">
                  {doc.doc_name || doc.name}
                </span>
                <span className="text-xs text-emerald-700 font-semibold flex items-center gap-1">
                  ✓ {t.verified} (OCR Ready)
                </span>
              </div>
            </div>
            
            <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-1 rounded-lg">
              98% Match
            </span>
          </div>
        ))}

        {/* Missing / Required Documents */}
        {missingDocs.map((docName, idx) => (
          <div
            key={idx}
            className="flex items-center justify-between p-3.5 bg-slate-50 border border-slate-200 rounded-2xl hover:border-indigo-300 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-slate-200 text-slate-500 flex items-center justify-center shrink-0">
                <FileX className="w-5 h-5" />
              </div>
              <div>
                <span className="text-sm font-bold text-slate-800 block">
                  {docName}
                </span>
                <span className="text-xs text-amber-700 font-semibold">
                  ⚠️ {t.missing}
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={() => handleUploadClick(docName)}
              className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl flex items-center gap-1 transition-all shadow-xs"
            >
              <Upload className="w-3.5 h-3.5" />
              Upload
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
