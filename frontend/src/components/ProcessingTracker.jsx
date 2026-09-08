import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, Circle, Sparkles, Brain, Cpu, ShieldCheck } from 'lucide-react';

export default function ProcessingTracker({ currentStep = 1 }) {
  // We define the logical progression stages
  const stages = [
    { id: 1, label: 'Video uploaded & verified', icon: CheckCircle2 },
    { id: 2, label: 'Audio extracted with FFmpeg', icon: Cpu },
    { id: 3, label: 'Spoken transcript generated via Groq Whisper', icon: Brain },
    { id: 4, label: 'Representative keyframes extracted (FFmpeg)', icon: Cpu },
    { id: 5, label: 'Multimodal content intelligence analysis (Gemini)', icon: Sparkles },
    { id: 6, label: 'Generating original concept & scene script', icon: Sparkles },
    { id: 7, label: 'Running independent Brand QA Critic audit', icon: ShieldCheck },
  ];

  // Simulates realistic progress milestone checkpoints while the backend request is active
  const [activeStage, setActiveStage] = useState(1);

  useEffect(() => {
    // Incrementally step through stages over realistic network intervals
    const timers = [
      setTimeout(() => setActiveStage(2), 1200),
      setTimeout(() => setActiveStage(3), 2800),
      setTimeout(() => setActiveStage(4), 4500),
      setTimeout(() => setActiveStage(5), 6500),
      setTimeout(() => setActiveStage(6), 11000),
      setTimeout(() => setActiveStage(7), 16000),
    ];

    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <div className="max-w-xl mx-auto py-16 px-4 sm:px-6">
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-emerald-100 flex items-center justify-center text-emerald-600 mx-auto mb-3 shadow-inner">
            <Loader2 className="w-6 h-6 animate-spin" />
          </div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            Analyzing your content...
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Running video transcription, visual frame extraction, and brand compliance
          </p>
        </div>

        {/* Stage List */}
        <div className="space-y-4">
          {stages.map((stage) => {
            const isCompleted = activeStage > stage.id;
            const isCurrent = activeStage === stage.id;

            return (
              <div
                key={stage.id}
                className={`flex items-center space-x-3.5 p-3 rounded-xl transition-all duration-300 ${
                  isCurrent
                    ? 'bg-emerald-50/80 border border-emerald-200 shadow-xs'
                    : isCompleted
                    ? 'bg-slate-50/50'
                    : 'opacity-40'
                }`}
              >
                <div className="shrink-0">
                  {isCompleted ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                  ) : isCurrent ? (
                    <Loader2 className="w-5 h-5 text-emerald-600 animate-spin" />
                  ) : (
                    <Circle className="w-5 h-5 text-slate-300" />
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  <p
                    className={`text-sm font-medium leading-snug ${
                      isCurrent
                        ? 'text-emerald-950 font-semibold'
                        : isCompleted
                        ? 'text-slate-800'
                        : 'text-slate-400'
                    }`}
                  >
                    {stage.label}
                  </p>
                </div>

                {isCurrent && (
                  <span className="text-[11px] font-medium text-emerald-700 bg-emerald-100/60 px-2 py-0.5 rounded-md">
                    Processing
                  </span>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
