import React, { useState, useEffect } from 'react';
import { History, Download, Printer, FileText, CheckCircle, ExternalLink, Calendar, User } from 'lucide-react';
import { api } from '../services/api';
import { translations } from '../utils/translations';

export default function ApplicationHistory({ language }) {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const t = translations[language] || translations.en;

  useEffect(() => {
    loadApplications();
  }, []);

  const loadApplications = async () => {
    try {
      setLoading(true);
      const data = await api.getApplications();
      setApplications(data);
    } catch (e) {
      console.error("Load applications error:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <span className="text-xs font-black uppercase tracking-wider text-indigo-700 bg-indigo-50 border border-indigo-200 px-3 py-1 rounded-full">
            History & Records
          </span>
          <h1 className="text-3xl sm:text-4xl font-black text-slate-900 mt-2">
            {t.navHistory}
          </h1>
          <p className="text-sm text-slate-500 font-medium mt-1">
            Access, download, or re-print completed physical and digital applications
          </p>
        </div>

        <button
          onClick={loadApplications}
          className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-colors self-start sm:self-auto"
        >
          Refresh History
        </button>
      </div>

      {loading ? (
        <div className="text-center py-16">
          <div className="w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-500 text-sm font-semibold">Loading applications...</p>
        </div>
      ) : applications.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border border-slate-200 max-w-lg mx-auto shadow-xs">
          <div className="w-16 h-16 rounded-2xl bg-slate-100 text-slate-400 mx-auto flex items-center justify-center mb-4">
            <History className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-black text-slate-800 mb-2">No Applications Yet</h3>
          <p className="text-sm text-slate-500 mb-6 font-medium">
            Complete a Digital Scholarship application or Physical Bank Form to see it stored here.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {applications.map((app, idx) => (
            <div
              key={app.application_id || idx}
              className="bg-white rounded-3xl p-6 shadow-md border border-slate-200 hover:border-indigo-300 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className={`text-[11px] font-black uppercase px-2.5 py-0.5 rounded-full ${
                    app.mode === 'physical'
                      ? 'bg-amber-100 text-amber-900 border border-amber-300'
                      : 'bg-indigo-100 text-indigo-900 border border-indigo-200'
                  }`}>
                    {app.mode === 'physical' ? 'Paper Form' : 'Digital Form'}
                  </span>
                  <span className="text-xs text-slate-400 font-bold">
                    {app.application_id}
                  </span>
                </div>

                <h3 className="text-lg font-black text-slate-900 mb-2 line-clamp-2">
                  {app.service_name}
                </h3>

                <div className="space-y-1.5 text-xs text-slate-600 mb-4">
                  <div className="flex items-center gap-2">
                    <User className="w-3.5 h-3.5 text-slate-400" />
                    <span>Applicant: <b>{app.applicant_name}</b></span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="w-3.5 h-3.5 text-slate-400" />
                    <span>Date: {app.saved_at ? new Date(app.saved_at).toLocaleDateString() : 'Today'}</span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 border-t border-slate-100 flex items-center gap-2">
                {app.pdf_url && (
                  <a
                    href={app.pdf_url}
                    download={`${app.application_id}.pdf`}
                    className="flex-1 py-2 px-3 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl flex items-center justify-center gap-1.5 transition-colors"
                  >
                    <Download className="w-3.5 h-3.5" /> PDF
                  </a>
                )}

                {app.filled_image_url && (
                  <a
                    href={app.filled_image_url}
                    target="_blank"
                    rel="noreferrer"
                    className="py-2 px-3 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold rounded-xl flex items-center gap-1 transition-colors"
                    title="View Image"
                  >
                    <ExternalLink className="w-3.5 h-3.5" /> Image
                  </a>
                )}
              </div>

            </div>
          ))}
        </div>
      )}

    </div>
  );
}
