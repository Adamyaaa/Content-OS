import React from 'react';
import { Database, TrendingUp, Sparkles, Flame, CheckCircle2, Bookmark, ArrowRight, ShieldCheck } from 'lucide-react';

export default function PatternLibraryView({ patterns, onSelectPatternDemo }) {
  const avgRetention = patterns?.length
    ? (patterns.reduce((sum, p) => sum + (p.avg_retention_score || 85), 0) / patterns.length).toFixed(1)
    : '86.5';

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 space-y-8 animate-fadeIn">
      {/* Top Banner */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-emerald-950 rounded-3xl p-8 text-white shadow-xl relative overflow-hidden">
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold uppercase tracking-wider mb-4 border border-emerald-500/30">
            <Database className="w-3.5 h-3.5" />
            <span>Compounding Intelligence Moat (TRD Spec)</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">
            Organic Content Pattern Library
          </h1>
          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            Every analyzed reel contributes to your brand's proprietary formula library. The system indexes viral hook structures, retention metrics, and psychological drivers to weight and validate future generations.
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-6 pt-6 border-t border-slate-700/60">
            <div>
              <span className="text-xs text-slate-400 font-medium block">Accumulated Patterns</span>
              <span className="text-2xl font-black text-white">{patterns?.length || 0}</span>
            </div>
            <div>
              <span className="text-xs text-slate-400 font-medium block">Avg View Retention</span>
              <span className="text-2xl font-black text-emerald-400">{avgRetention}%</span>
            </div>
            <div className="col-span-2 sm:col-span-1">
              <span className="text-xs text-slate-400 font-medium block">Deduplication Gate</span>
              <span className="text-xs font-bold text-slate-200 bg-white/10 px-2.5 py-1 rounded-md mt-1 inline-block">
                &lt; 70% Cosine Threshold
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Pattern Cards Grid */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-bold text-slate-900 tracking-tight flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>Active High-Retention Formulas</span>
          </h2>
          <span className="text-xs text-slate-500 font-medium">
            Ranked by Historical Performance
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {patterns?.map((pat) => (
            <div
              key={pat.id}
              className="bg-white rounded-2xl border border-slate-200 hover:border-emerald-500/80 p-6 shadow-xs hover:shadow-md transition-all duration-200 flex flex-col justify-between"
            >
              <div>
                {/* Card Header */}
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div className="flex-1">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md mb-1.5 inline-block">
                      {pat.source}
                    </span>
                    <h3 className="text-base font-bold text-slate-900 leading-snug">
                      {pat.pattern_name}
                    </h3>
                  </div>

                  <div className="text-right shrink-0">
                    <div className="text-xs font-bold text-emerald-700 bg-emerald-100/70 border border-emerald-200 px-2.5 py-1 rounded-lg">
                      {pat.avg_retention_score}% Ret.
                    </div>
                    <span className="text-[10px] text-slate-400 block mt-0.5">
                      {pat.usage_count} uses
                    </span>
                  </div>
                </div>

                {/* Hook Blueprint */}
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 mb-4">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-600 block mb-1">
                    Hook Blueprint:
                  </span>
                  <p className="text-xs text-slate-800 font-medium italic">
                    "{pat.hook_structure}"
                  </p>
                </div>

                {/* Tags */}
                <div className="space-y-2 text-xs text-slate-600">
                  <div className="flex items-start space-x-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                    <span><strong className="text-slate-800">Best for:</strong> {pat.best_for}</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <Flame className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
                    <span><strong className="text-slate-800">Emotional driver:</strong> {pat.emotional_driver}</span>
                  </div>
                </div>
              </div>

              {/* Action */}
              <div className="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[11px] text-slate-400">Formula ID: {pat.id}</span>
                <button
                  onClick={() => onSelectPatternDemo(pat)}
                  className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 flex items-center space-x-1 group"
                >
                  <span>View Example Analysis</span>
                  <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
