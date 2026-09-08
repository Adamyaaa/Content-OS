import React from 'react';
import { Brain, Sparkles, Target, Flame, Megaphone, LayoutList, Eye } from 'lucide-react';

export default function ContentIntelligenceCard({ analysis }) {
  if (!analysis) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
      <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <Brain className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Content Intelligence</h3>
            <p className="text-xs text-slate-500">Deconstructed social media mechanics of the source video</p>
          </div>
        </div>
        <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md">
          Multimodal Reasoning
        </span>
      </div>

      <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Topic Card */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
          <div className="flex items-center space-x-2 text-slate-500 mb-1.5">
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-700">Topic</span>
          </div>
          <p className="text-sm font-semibold text-slate-900">{analysis.topic}</p>
        </div>

        {/* Hook Card */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 md:col-span-2">
          <div className="flex items-center justify-between mb-1.5">
            <div className="flex items-center space-x-2 text-slate-500">
              <Eye className="w-4 h-4 text-emerald-600" />
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-700">
                Hook (0-3s Opening)
              </span>
            </div>
            <span className="text-[10px] font-semibold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full">
              {analysis.hook_type}
            </span>
          </div>
          <p className="text-sm font-medium text-slate-900 italic">"{analysis.hook}"</p>
        </div>

        {/* Content Format */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
          <div className="flex items-center space-x-2 text-slate-500 mb-1.5">
            <LayoutList className="w-4 h-4 text-emerald-600" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-700">Content Format</span>
          </div>
          <p className="text-sm font-medium text-slate-900">{analysis.content_format}</p>
        </div>

        {/* Target Audience */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
          <div className="flex items-center space-x-2 text-slate-500 mb-1.5">
            <Target className="w-4 h-4 text-emerald-600" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-700">Target Audience</span>
          </div>
          <p className="text-sm font-medium text-slate-900">{analysis.target_audience}</p>
        </div>

        {/* Emotional Trigger */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
          <div className="flex items-center space-x-2 text-slate-500 mb-1.5">
            <Flame className="w-4 h-4 text-amber-500" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-700">Emotional Trigger</span>
          </div>
          <p className="text-sm font-medium text-slate-900">{analysis.emotional_trigger}</p>
        </div>

        {/* CTA */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 md:col-span-2 lg:col-span-3">
          <div className="flex items-center space-x-2 text-slate-500 mb-1.5">
            <Megaphone className="w-4 h-4 text-emerald-600" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-700">Call To Action (CTA)</span>
          </div>
          <p className="text-sm font-medium text-slate-800">{analysis.cta || 'Implicit engagement call'}</p>
        </div>
      </div>
    </div>
  );
}
