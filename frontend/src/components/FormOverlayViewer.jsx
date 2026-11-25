import React, { useState } from 'react';
import { Eye, Download, Printer, CheckCircle, ZoomIn, ZoomOut, AlertCircle, FileCheck } from 'lucide-react';
import { translations } from '../utils/translations';

export default function FormOverlayViewer({
  filledImageUrl,
  originalImageUrl,
  pdfUrl,
  formData = {},
  fieldsSchema = [],
  onConfirmAndGenerate,
  language = 'te',
  isGenerated = false
}) {
  const [zoom, setZoom] = useState(1);
  const [viewMode, setViewMode] = useState('filled'); // 'filled' or 'original'
  const t = translations[language] || translations.en;

  const handlePrint = () => {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    } else if (filledImageUrl) {
      const printWin = window.open('');
      printWin.document.write(`<img src="${filledImageUrl}" style="width:100%" onload="window.print();window.close()"/>`);
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden mb-8">
      
      {/* Top Action Bar */}
      <div className="bg-slate-900 text-white p-4 sm:p-5 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-500 text-slate-950 flex items-center justify-center font-bold">
            <Eye className="w-6 h-6" />
          </div>
          <div>
            <h4 className="font-extrabold text-base sm:text-lg">
              {viewMode === 'filled' ? 'Filled Form Preview (Layout Preserved)' : 'Original Uploaded Form'}
            </h4>
            <p className="text-xs text-slate-400">
              High-resolution document canvas matching official layout
            </p>
          </div>
        </div>

        {/* View Toggle & Zoom */}
        <div className="flex items-center gap-2">
          <div className="bg-slate-800 p-1 rounded-xl flex items-center border border-slate-700">
            <button
              onClick={() => setViewMode('filled')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
                viewMode === 'filled' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'
              }`}
            >
              Filled Form
            </button>
            <button
              onClick={() => setViewMode('original')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
                viewMode === 'original' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'
              }`}
            >
              Original Blank
            </button>
          </div>

          <div className="flex items-center bg-slate-800 rounded-xl border border-slate-700 p-1">
            <button
              onClick={() => setZoom(Math.max(0.6, zoom - 0.2))}
              className="p-1.5 text-slate-300 hover:text-white"
              title="Zoom out"
            >
              <ZoomOut className="w-4 h-4" />
            </button>
            <span className="text-xs font-bold px-1 text-slate-300">{Math.round(zoom * 100)}%</span>
            <button
              onClick={() => setZoom(Math.min(1.8, zoom + 0.2))}
              className="p-1.5 text-slate-300 hover:text-white"
              title="Zoom in"
            >
              <ZoomIn className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Manual Signature Warning Banner */}
      <div className="bg-amber-50 border-b border-amber-200 p-3.5 px-6 flex items-center gap-3">
        <AlertCircle className="w-5 h-5 text-amber-600 shrink-0" />
        <span className="text-xs sm:text-sm font-bold text-amber-900">
          {t.signatureNotice}
        </span>
      </div>

      {/* Main Image Canvas */}
      <div className="bg-slate-100 p-4 sm:p-8 flex justify-center overflow-auto max-h-[650px]">
        <div
          className="transition-transform duration-200 origin-top shadow-2xl rounded-lg overflow-hidden border border-slate-300 bg-white"
          style={{ transform: `scale(${zoom})` }}
        >
          <img
            src={viewMode === 'filled' ? (filledImageUrl || originalImageUrl) : originalImageUrl}
            alt="Physical Form"
            className="max-w-[800px] w-full object-contain"
          />
        </div>
      </div>

      {/* Bottom Action Footer */}
      <div className="p-4 sm:p-6 bg-white border-t border-slate-200 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
          <span className="text-xs font-bold text-slate-600">
            {isGenerated ? '✓ Ready for Physical Submission' : 'Verification Complete'}
          </span>
        </div>

        <div className="flex items-center gap-3">
          {pdfUrl && (
            <>
              <a
                href={pdfUrl}
                download="FormSaathi_Application.pdf"
                className="px-4 py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-sm font-bold flex items-center gap-2 shadow-xs transition-colors"
              >
                <Download className="w-4 h-4" />
                {t.downloadPdf}
              </a>

              <button
                type="button"
                onClick={handlePrint}
                className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-sm font-bold flex items-center gap-2 shadow-xs transition-colors"
              >
                <Printer className="w-4 h-4" />
                {t.printPdf}
              </button>
            </>
          )}

          {!isGenerated && onConfirmAndGenerate && (
            <button
              type="button"
              onClick={onConfirmAndGenerate}
              className="px-6 py-2.5 bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-700 hover:to-indigo-900 text-white rounded-xl text-sm font-bold flex items-center gap-2 shadow-md transition-all transform active:scale-95"
            >
              <FileCheck className="w-5 h-5" />
              {t.confirmAndGenerate}
            </button>
          )}
        </div>
      </div>

    </div>
  );
}
