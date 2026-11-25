import React, { useState } from 'react';
import { AlertTriangle, CheckCircle, Edit3, ArrowRight } from 'lucide-react';
import { translations } from '../utils/translations';

export default function ConflictBanner({ conflicts = [], onResolve, language = 'te' }) {
  const [customEditingField, setCustomEditingField] = useState(null);
  const [customValue, setCustomValue] = useState('');
  const t = translations[language] || translations.en;

  if (!conflicts || conflicts.length === 0) return null;

  return (
    <div className="bg-amber-50 border-2 border-amber-300 rounded-3xl p-5 sm:p-6 mb-6 shadow-md transition-all">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-2xl bg-amber-500 text-white flex items-center justify-center shrink-0 shadow-md">
          <AlertTriangle className="w-7 h-7" />
        </div>

        <div className="flex-1">
          <h3 className="text-lg font-black text-amber-950 flex items-center gap-2">
            {t.conflictTitle}
          </h3>
          <p className="text-sm text-amber-800 mt-1 font-medium">
            {t.conflictSubtitle}
          </p>

          <div className="mt-4 space-y-4">
            {conflicts.map((conflict, idx) => {
              const isEditing = customEditingField === conflict.field_id;

              return (
                <div
                  key={conflict.field_id || idx}
                  className="bg-white border-2 border-amber-200 rounded-2xl p-4 shadow-xs"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                    <span className="font-extrabold text-slate-800 text-base">
                      {conflict[`label_${language}`] || conflict.label_hi || conflict.label_te || conflict.label_en}
                    </span>
                    <span className="text-xs bg-amber-100 text-amber-900 font-bold px-2.5 py-1 rounded-full border border-amber-300 self-start sm:self-auto">
                      Source: {conflict.document_source}
                    </span>
                  </div>

                  <p className="text-xs sm:text-sm text-slate-700 font-semibold mb-4 bg-amber-50/50 p-2.5 rounded-xl border border-amber-100">
                    {conflict.warning_message || conflict[`warning_message_${language}`] || conflict.warning_message_hi || conflict.warning_message_en}
                  </p>

                  {/* Choice Buttons */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                    
                    {/* Choice 1: Entered Value */}
                    <button
                      type="button"
                      onClick={() => onResolve(conflict.field_id, conflict.user_value, 'user')}
                      className="flex flex-col p-3 rounded-xl border-2 border-slate-200 hover:border-indigo-600 bg-slate-50 hover:bg-indigo-50/50 text-left transition-all group"
                    >
                      <span className="text-xs text-slate-500 font-bold flex items-center gap-1">
                        <CheckCircle className="w-3.5 h-3.5 text-slate-400 group-hover:text-indigo-600" />
                        {t.useEntered}
                      </span>
                      <span className="text-sm font-extrabold text-slate-900 mt-1">
                        {conflict.user_value}
                      </span>
                    </button>

                    {/* Choice 2: Document OCR Value */}
                    <button
                      type="button"
                      onClick={() => onResolve(conflict.field_id, conflict.document_value, 'document')}
                      className="flex flex-col p-3 rounded-xl border-2 border-emerald-300 hover:border-emerald-600 bg-emerald-50/40 hover:bg-emerald-50 text-left transition-all group"
                    >
                      <span className="text-xs text-emerald-700 font-bold flex items-center gap-1">
                        <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                        {t.useDocument}
                      </span>
                      <span className="text-sm font-extrabold text-emerald-950 mt-1">
                        {conflict.document_value}
                      </span>
                    </button>

                    {/* Choice 3: Custom Edit */}
                    <button
                      type="button"
                      onClick={() => {
                        setCustomEditingField(isEditing ? null : conflict.field_id);
                        setCustomValue(conflict.user_value);
                      }}
                      className="flex flex-col p-3 rounded-xl border-2 border-slate-200 hover:border-slate-400 bg-slate-50 hover:bg-slate-100 text-left transition-all"
                    >
                      <span className="text-xs text-slate-500 font-bold flex items-center gap-1">
                        <Edit3 className="w-3.5 h-3.5" />
                        {t.editCustom}
                      </span>
                      <span className="text-xs font-semibold text-slate-600 mt-1">
                        {isEditing ? "Cancel edit" : "Type different value"}
                      </span>
                    </button>
                  </div>

                  {/* Inline Custom Edit Input */}
                  {isEditing && (
                    <div className="mt-3 pt-3 border-t border-slate-100 flex gap-2">
                      <input
                        type="text"
                        value={customValue}
                        onChange={(e) => setCustomValue(e.target.value)}
                        placeholder="Enter corrected value"
                        className="flex-1 px-3 py-2 text-sm border-2 border-indigo-300 rounded-xl focus:outline-hidden focus:border-indigo-600"
                      />
                      <button
                        type="button"
                        onClick={() => {
                          if (customValue.trim()) {
                            onResolve(conflict.field_id, customValue.trim(), 'custom');
                            setCustomEditingField(null);
                          }
                        }}
                        className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-xs font-bold hover:bg-indigo-700 transition-colors flex items-center gap-1"
                      >
                        Save <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  )}

                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
