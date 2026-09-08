import React from 'react';
import { Sprout, History, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';

export default function Header({ health, onOpenHistory, historyCount, onReset }) {
  const isHealthy = health && health.groq_configured && health.gemini_configured;

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand & Logo */}
        <div 
          onClick={onReset}
          className="flex items-center space-x-3 cursor-pointer group"
          title="Return to Home"
        >
          <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center text-white shadow-md shadow-emerald-500/20 group-hover:bg-emerald-700 transition">
            <Sprout className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-slate-900 text-lg tracking-tight">
                Organic Content OS
              </span>
              <span className="text-[11px] font-semibold uppercase tracking-wider bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full">
                Organic Journals
              </span>
            </div>
            <p className="text-xs text-slate-500 font-medium hidden sm:block">
              AI-powered content intelligence and generation
            </p>
          </div>
        </div>

        {/* Right Actions: System Status & History */}
        <div className="flex items-center space-x-3">
          {/* Health Status Pill */}
          <div 
            className={`hidden md:flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-medium border ${
              isHealthy
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : 'bg-amber-50 text-amber-700 border-amber-200'
            }`}
            title={
              isHealthy
                ? 'Groq Whisper & Gemini 2.5 Flash connected'
                : 'Configure GROQ_API_KEY and GEMINI_API_KEY in .env'
            }
          >
            {isHealthy ? (
              <>
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span>AI Pipeline Connected</span>
              </>
            ) : (
              <>
                <AlertCircle className="w-3.5 h-3.5 text-amber-500" />
                <span>API Keys Pending</span>
              </>
            )}
          </div>

          {/* Past Analyses Button */}
          <button
            onClick={onOpenHistory}
            className="flex items-center space-x-2 px-3.5 py-1.5 text-xs font-semibold text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200/80 rounded-lg transition"
          >
            <History className="w-4 h-4 text-slate-500" />
            <span>Past Runs</span>
            {historyCount > 0 && (
              <span className="bg-slate-300 text-slate-800 px-1.5 py-0.2 rounded-full text-[10px]">
                {historyCount}
              </span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
