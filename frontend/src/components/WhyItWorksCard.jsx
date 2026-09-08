import React from 'react';
import { Lightbulb, CheckCircle2, TrendingUp, Layers, Camera } from 'lucide-react';

export default function WhyItWorksCard({ analysis }) {
  if (!analysis) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
      <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
            <Lightbulb className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Why It Works</h3>
            <p className="text-xs text-slate-500">The psychological formula and retention mechanics</p>
          </div>
        </div>
        <span className="text-[11px] font-semibold text-amber-800 bg-amber-100/60 px-2.5 py-1 rounded-md">
          Algorithm & Psychology
        </span>
      </div>

      <div className="p-6 space-y-6">
        {/* Core Underlying Content Pattern */}
        <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200">
          <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800 block mb-1">
            Abstracted Content Pattern Formula:
          </span>
          <p className="text-sm font-bold text-emerald-950">
            {analysis.content_pattern}
          </p>
        </div>

        {/* Narrative Flow & Visual Pacing */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Narrative Structure */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <div className="flex items-center space-x-2 mb-3">
              <Layers className="w-4 h-4 text-emerald-600" />
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                Narrative Progression
              </span>
            </div>
            <div className="space-y-2">
              {analysis.narrative_structure?.map((step, idx) => (
                <div key={idx} className="flex items-center space-x-2.5 text-xs text-slate-800 font-medium">
                  <span className="w-5 h-5 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center font-bold text-[10px] shrink-0">
                    {idx + 1}
                  </span>
                  <span>{step}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Visual Pacing & Style */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <div className="flex items-center space-x-2 mb-3">
              <Camera className="w-4 h-4 text-emerald-600" />
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                Visual Mechanics
              </span>
            </div>
            <div className="space-y-2 text-xs text-slate-700">
              <div>
                <span className="font-semibold text-slate-900">Style: </span>
                {analysis.visual_style}
              </div>
              <div>
                <span className="font-semibold text-slate-900">Pattern: </span>
                {analysis.visual_pattern}
              </div>
            </div>
          </div>
        </div>

        {/* Retention Drivers & Strengths */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Strengths */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <div className="flex items-center space-x-2 mb-2 text-emerald-700">
              <CheckCircle2 className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">Content Strengths</span>
            </div>
            <ul className="space-y-1.5 text-xs text-slate-700">
              {analysis.content_strengths?.map((str, i) => (
                <li key={i} className="flex items-start space-x-2">
                  <span className="text-emerald-500 font-bold">•</span>
                  <span>{str}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Why it might work */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <div className="flex items-center space-x-2 mb-2 text-amber-700">
              <TrendingUp className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">Virality & Retention Factors</span>
            </div>
            <ul className="space-y-1.5 text-xs text-slate-700">
              {analysis.why_it_might_work?.map((reason, i) => (
                <li key={i} className="flex items-start space-x-2">
                  <span className="text-amber-500 font-bold">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
