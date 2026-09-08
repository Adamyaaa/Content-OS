import React from 'react';
import { ShieldCheck, CheckCircle2, AlertTriangle, XCircle, ArrowRight, RefreshCw, FileCode } from 'lucide-react';

export default function BrandQACard({ qaResult, productionReadiness, onReset }) {
  if (!qaResult) return null;

  const { status, overall_score, checks, issues, suggestions } = qaResult;

  const getStatusColor = (st) => {
    switch (st?.toUpperCase()) {
      case 'PASS':
        return 'text-emerald-700 bg-emerald-50 border-emerald-200';
      case 'WARNING':
        return 'text-amber-700 bg-amber-50 border-amber-200';
      case 'FAIL':
        return 'text-red-700 bg-red-50 border-red-200';
      default:
        return 'text-slate-700 bg-slate-50 border-slate-200';
    }
  };

  const getScoreBadgeColor = (score) => {
    if (score >= 80) return 'text-emerald-600 border-emerald-500 bg-emerald-50/50';
    if (score >= 60) return 'text-amber-600 border-amber-500 bg-amber-50/50';
    return 'text-red-600 border-red-500 bg-red-50/50';
  };

  const isReady = productionReadiness === 'Ready for production';

  return (
    <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Brand QA & Compliance Critic
            </h3>
            <p className="text-xs text-slate-500">
              Independent guardrail audit enforcing tone, originality, and agricultural claims
            </p>
          </div>
        </div>

        {/* Production Readiness Status */}
        <span
          className={`px-3 py-1 rounded-full text-xs font-bold border ${
            isReady
              ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
              : 'bg-amber-100 text-amber-800 border-amber-300'
          }`}
        >
          {productionReadiness}
        </span>
      </div>

      <div className="p-6 space-y-6">
        {/* Score & Verdict Banner */}
        <div className="flex flex-col sm:flex-row items-center justify-between p-5 rounded-2xl bg-slate-50 border border-slate-200/80 gap-4">
          <div className="flex items-center space-x-4">
            {/* Score Ring */}
            <div
              className={`w-16 h-16 rounded-full border-4 flex flex-col items-center justify-center font-extrabold ${getScoreBadgeColor(
                overall_score
              )}`}
            >
              <span className="text-xl leading-none">{overall_score}</span>
              <span className="text-[10px] uppercase font-semibold text-slate-400">/ 100</span>
            </div>

            <div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-bold text-slate-900">Compliance Verdict:</span>
                <span
                  className={`text-xs font-bold px-2 py-0.5 rounded-md border ${getStatusColor(
                    status
                  )}`}
                >
                  {status}
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-0.5">
                Validated against Organic Journals guardrails & evidence policies.
              </p>
            </div>
          </div>

          <button
            onClick={onReset}
            className="w-full sm:w-auto px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-semibold flex items-center justify-center space-x-1.5 transition shadow-xs"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Analyze Another Reel</span>
          </button>
        </div>

        {/* Itemized Checks */}
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3">
            Itemized Audit Criteria:
          </h4>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {checks?.map((chk, i) => {
              const isPass = chk.status === 'PASS';
              const isWarning = chk.status === 'WARNING';

              return (
                <div
                  key={i}
                  className="p-3.5 rounded-xl border border-slate-200/80 bg-white flex flex-col justify-between"
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs font-bold text-slate-800">{chk.name}</span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-md border flex items-center space-x-1 ${getStatusColor(
                        chk.status
                      )}`}
                    >
                      {isPass ? (
                        <CheckCircle2 className="w-3 h-3" />
                      ) : isWarning ? (
                        <AlertTriangle className="w-3 h-3" />
                      ) : (
                        <XCircle className="w-3 h-3" />
                      )}
                      <span>{chk.status}</span>
                    </span>
                  </div>

                  <p className="text-xs text-slate-600 leading-relaxed">{chk.reason}</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Flagged Issues */}
        {issues?.length > 0 && (
          <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200">
            <span className="text-xs font-bold uppercase tracking-wider text-amber-900 block mb-1.5">
              Flagged Claims / Review Points:
            </span>
            <ul className="space-y-1 text-xs text-amber-900">
              {issues.map((iss, i) => (
                <li key={i} className="flex items-start space-x-2">
                  <span className="text-amber-600 font-bold">•</span>
                  <span>{iss}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Editorial Suggestions */}
        {suggestions?.length > 0 && (
          <div className="p-4 rounded-xl bg-emerald-50/50 border border-emerald-200/80">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-900 block mb-1.5">
              Editorial Suggestions for Production:
            </span>
            <ul className="space-y-1 text-xs text-slate-700">
              {suggestions.map((sug, i) => (
                <li key={i} className="flex items-start space-x-2">
                  <span className="text-emerald-600 font-bold">✓</span>
                  <span>{sug}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
