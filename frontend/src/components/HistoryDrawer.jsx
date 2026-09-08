import React from 'react';
import { X, Calendar, ArrowRight, Film, ShieldCheck } from 'lucide-react';

export default function HistoryDrawer({ isOpen, onClose, pastRuns, onSelectRun }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div 
        onClick={onClose}
        className="absolute inset-0 bg-black/40 backdrop-blur-xs transition-opacity"
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white shadow-2xl flex flex-col">
          {/* Drawer Header */}
          <div className="p-6 border-b border-slate-200 flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">Analysis History</h2>
              <p className="text-xs text-slate-500">Previously analyzed reels & concepts</p>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* List of Runs */}
          <div className="flex-1 overflow-y-auto p-6 space-y-3">
            {(!pastRuns || pastRuns.length === 0) ? (
              <div className="text-center py-12 text-slate-400">
                <Film className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-xs">No previous analyses saved yet.</p>
              </div>
            ) : (
              pastRuns.map((run) => (
                <div
                  key={run.analysis_id}
                  onClick={() => {
                    onSelectRun(run.analysis_id);
                    onClose();
                  }}
                  className="p-4 rounded-xl border border-slate-200 hover:border-emerald-500 hover:bg-emerald-50/20 cursor-pointer transition group shadow-2xs"
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs font-bold text-slate-900 group-hover:text-emerald-700 transition line-clamp-1">
                      {run.generated_title || run.topic || run.filename}
                    </span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700 shrink-0">
                      QA: {run.qa_score}/100
                    </span>
                  </div>

                  <p className="text-xs text-slate-500 line-clamp-1 mb-2">
                    Topic: {run.topic}
                  </p>

                  <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-100">
                    <span className="flex items-center space-x-1">
                      <Calendar className="w-3 h-3" />
                      <span>{new Date(run.created_at).toLocaleDateString()}</span>
                    </span>
                    <span className="text-emerald-600 font-medium flex items-center space-x-0.5 group-hover:translate-x-1 transition">
                      <span>View</span>
                      <ArrowRight className="w-3 h-3" />
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
