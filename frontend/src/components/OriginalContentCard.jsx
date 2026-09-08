import React, { useState } from 'react';
import { Film, Clock, FileText, ChevronDown, ChevronUp, Image as ImageIcon } from 'lucide-react';

export default function OriginalContentCard({ analysisResult }) {
  const [showTranscript, setShowTranscript] = useState(false);
  const [selectedFrame, setSelectedFrame] = useState(null);

  const { filename, video_duration, video_url, frame_urls, transcript } = analysisResult;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
      <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <Film className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">Original Reel Media</h3>
            <p className="text-xs text-slate-500">Source video, audio extraction, and extracted visual keyframes</p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-600">
          <span className="flex items-center space-x-1 bg-slate-100 px-2.5 py-1 rounded-md font-medium">
            <Clock className="w-3.5 h-3.5 text-slate-400" />
            <span>{video_duration}s</span>
          </span>
        </div>
      </div>

      <div className="p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Video Player Preview */}
        <div className="lg:col-span-5 flex flex-col">
          <div className="relative rounded-xl overflow-hidden bg-black/90 aspect-[9/16] max-h-[420px] mx-auto shadow-inner flex items-center justify-center">
            <video
              src={video_url}
              controls
              playsInline
              className="w-full h-full object-contain"
            >
              Your browser does not support the video tag.
            </video>
          </div>
          <p className="text-center text-xs text-slate-500 mt-2 truncate max-w-xs mx-auto">
            {filename}
          </p>
        </div>

        {/* Frames & Transcript Panel */}
        <div className="lg:col-span-7 flex flex-col space-y-4">
          {/* Keyframes Filmstrip */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center space-x-1">
                <ImageIcon className="w-3.5 h-3.5 text-slate-400" />
                <span>Extracted Keyframes ({frame_urls?.length || 0})</span>
              </span>
              <span className="text-[11px] text-slate-400">FFmpeg 0% - 90% timeline</span>
            </div>

            <div className="grid grid-cols-4 sm:grid-cols-7 gap-2">
              {frame_urls?.map((url, idx) => (
                <div
                  key={idx}
                  onClick={() => setSelectedFrame(url)}
                  className="group relative aspect-[9/16] rounded-lg overflow-hidden border border-slate-200 bg-slate-100 cursor-pointer hover:border-emerald-500 transition shadow-2xs"
                >
                  <img
                    src={url}
                    alt={`Frame ${idx + 1}`}
                    className="w-full h-full object-cover group-hover:scale-105 transition duration-200"
                  />
                  <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/80 to-transparent p-1 text-[9px] text-white font-mono text-center">
                    F{idx + 1}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Transcript Accordion */}
          <div className="border border-slate-200 rounded-xl overflow-hidden bg-slate-50/50">
            <button
              onClick={() => setShowTranscript(!showTranscript)}
              className="w-full px-4 py-3 flex items-center justify-between text-left hover:bg-slate-100/60 transition"
            >
              <div className="flex items-center space-x-2">
                <FileText className="w-4 h-4 text-emerald-600" />
                <span className="text-xs font-semibold text-slate-800">
                  Spoken Transcript ({transcript?.language?.toUpperCase() || 'EN'})
                </span>
              </div>
              {showTranscript ? (
                <ChevronUp className="w-4 h-4 text-slate-400" />
              ) : (
                <ChevronDown className="w-4 h-4 text-slate-400" />
              )}
            </button>

            {showTranscript && (
              <div className="p-4 border-t border-slate-200 bg-white text-xs leading-relaxed text-slate-700 font-sans max-h-48 overflow-y-auto">
                <p className="whitespace-pre-wrap">{transcript?.text || 'No speech detected.'}</p>
              </div>
            )}
          </div>

          {/* Key Claims Observable Preview */}
          {analysisResult.analysis?.key_claims?.length > 0 && (
            <div className="p-4 rounded-xl bg-amber-50/60 border border-amber-200/80">
              <span className="text-[11px] font-bold uppercase tracking-wider text-amber-900 block mb-1.5">
                Observable Claims Stated in Video:
              </span>
              <ul className="list-disc list-inside space-y-1 text-xs text-amber-900/90">
                {analysisResult.analysis.key_claims.map((claim, i) => (
                  <li key={i}>{claim}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Frame Preview Modal */}
      {selectedFrame && (
        <div
          onClick={() => setSelectedFrame(null)}
          className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4 backdrop-blur-xs"
        >
          <div className="relative max-w-lg w-full max-h-[85vh] rounded-xl overflow-hidden bg-black flex flex-col items-center">
            <img src={selectedFrame} alt="Enlarged Frame" className="max-h-[80vh] object-contain" />
            <p className="text-xs text-slate-300 py-2">Click anywhere to close</p>
          </div>
        </div>
      )}
    </div>
  );
}
