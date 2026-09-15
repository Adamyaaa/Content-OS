import React from 'react';
import { Video, ExternalLink, Clapperboard, Sparkles } from 'lucide-react';

export default function VideoGenerationCard({ generatedContent, onRenderVideo, isRenderingVideo }) {
  if (!generatedContent) return null;

  const {
    rendered_video_url,
    voiceover_engine = "Neural HD Engine",
  } = generatedContent;

  return (
    <div className="mt-6 p-5 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 text-white border border-emerald-500/50 shadow-lg relative overflow-hidden">
      {/* Tier 2 Badge */}
      <div className="absolute top-0 right-0 bg-emerald-500 text-slate-900 text-[10px] font-extrabold px-3 py-1 rounded-bl-lg uppercase tracking-wider">
        Tier 2 / Pro Feature
      </div>

      <div className="flex items-center justify-between flex-wrap gap-2 mb-4 pr-24">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center border border-emerald-500/30">
            <Video className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-sm font-bold tracking-tight text-white flex items-center space-x-2">
              <span>Rendered 9:16 Short-Form Video Reel</span>
            </h4>
            <p className="text-xs text-slate-400">
              FLUX AI Keyframes • Ken Burns Zoompan • Kinetic Subtitles • Neural Audio Mux
            </p>
          </div>
        </div>

        {rendered_video_url && (
          <a
            href={rendered_video_url}
            download="organic_journals_reel.mp4"
            className="text-xs bg-emerald-600 hover:bg-emerald-500 text-white font-semibold px-3 py-1.5 rounded-lg transition flex items-center space-x-1.5 shadow-sm mt-2 sm:mt-0"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span>Download .mp4</span>
          </a>
        )}
      </div>

      {rendered_video_url ? (
        <div className="flex flex-col sm:flex-row items-center gap-6 pt-2">
          {/* 9:16 Vertical Video Player */}
          <div className="relative w-full max-w-[260px] aspect-[9/16] rounded-2xl overflow-hidden border-2 border-emerald-500/50 bg-black shadow-2xl mx-auto sm:mx-0 shrink-0">
            <video
              src={rendered_video_url}
              controls
              playsInline
              className="w-full h-full object-cover"
            />
          </div>

          {/* Video Reel Metadata & Specs */}
          <div className="flex-1 space-y-3 text-xs text-slate-300">
            <div className="p-3.5 rounded-xl bg-white/5 border border-white/10 space-y-2">
              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 border-b border-white/5 pb-1.5">
                <span>Aspect Ratio: 9:16 (1080x1920)</span>
                <span className="text-emerald-400 font-semibold">Ready for IG / TikTok</span>
              </div>
              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 border-b border-white/5 pb-1.5">
                <span>Audio Track: {voiceover_engine || "Neural HD Audio"}</span>
                <span className="text-slate-200">Synced Audio Mux</span>
              </div>
              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span>Subtitles: Kinetic 9:16 Typography</span>
                <span className="text-emerald-400 font-semibold">Active Overlay</span>
              </div>
            </div>

            <p className="text-slate-400 leading-relaxed text-[11px]">
              This video was procedurally rendered end-to-end without paid third-party APIs. Ready to review and publish directly to Instagram Reels, TikTok, or YouTube Shorts.
            </p>

            <button
              onClick={onRenderVideo}
              disabled={isRenderingVideo}
              className="mt-2 text-xs font-semibold text-emerald-400 hover:text-emerald-300 underline transition"
            >
              {isRenderingVideo ? 'Re-rendering in progress...' : '↺ Re-render Video with Fresh Visuals'}
            </button>
          </div>
        </div>
      ) : (
        <div className="p-6 rounded-xl bg-white/5 border border-emerald-500/20 text-center space-y-4">
          <div className="max-w-md mx-auto">
            <p className="text-sm font-semibold text-emerald-300 mb-1 flex items-center justify-center gap-2">
              <Sparkles className="w-4 h-4" />
              Unlock Tier 2: Automated Video Generation
            </p>
            <p className="text-xs text-slate-400">
              Upgrade to our Tier 2 plan to instantly render this script into a ready-to-post 9:16 vertical video reel. Includes AI visuals, Ken Burns motion, kinetic subtitles, and neural voiceover.
            </p>
          </div>

          <button
            onClick={onRenderVideo}
            disabled={isRenderingVideo}
            className={`inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl font-bold text-sm shadow-md transition ${
              isRenderingVideo
                ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-600/30 ring-2 ring-emerald-500/50 ring-offset-2 ring-offset-slate-900'
            }`}
          >
            <Clapperboard className="w-4 h-4" />
            <span>
              {isRenderingVideo
                ? 'Processing Tier 2 Render...'
                : 'Try Tier 2 Render (Demo)'}
            </span>
          </button>
        </div>
      )}
    </div>
  );
}
