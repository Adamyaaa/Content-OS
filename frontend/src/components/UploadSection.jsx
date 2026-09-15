import React, { useState, useRef } from 'react';
import { UploadCloud, Film, CheckCircle2, AlertCircle, FileVideo, Sparkles, Link2 } from 'lucide-react';

export default function UploadSection({ onUploadFile, onUploadUrl, onSelectSample, isAnalyzing, error }) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [validationError, setValidationError] = useState('');
  const fileInputRef = useRef(null);

  const allowedFormats = ['.mp4', '.mov', '.webm', '.mkv'];

  const validateAndSetFile = (file) => {
    setValidationError('');
    setVideoUrl(''); // Clear URL if file is selected
    if (!file) return;

    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedFormats.includes(ext)) {
      setValidationError(`Unsupported file format '${ext}'. Please upload an MP4, MOV, or WEBM video.`);
      return;
    }

    if (file.size > 120 * 1024 * 1024) {
      setValidationError('File size exceeds the 120MB demo limit.');
      return;
    }

    setSelectedFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleUrlChange = (e) => {
    setVideoUrl(e.target.value);
    setSelectedFile(null); // Clear file if URL is typed
    setValidationError('');
  };

  const handleStartAnalysis = () => {
    if (selectedFile) {
      onUploadFile(selectedFile);
    } else if (videoUrl) {
      onUploadUrl(videoUrl);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-12 px-4 sm:px-6">
      {/* Title & Subtitle */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-100/80 text-emerald-800 text-xs font-semibold uppercase tracking-wider mb-4">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Vertical-Slice Content Intelligence</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight mb-3">
          Analyze a successful reel down to its core formula and psychology.
        </h1>
        <p className="text-slate-600 text-base max-w-xl mx-auto leading-relaxed">
          Upload any trending agriculture reel. Organic Content OS extracts the underlying narrative structure, visual cadence, and hook psychology to fuel your <span className="font-semibold text-slate-900">Pattern Library</span>.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* URL Input Box */}
        <div className={`relative border-2 rounded-2xl p-6 text-center transition-all duration-200 flex flex-col justify-center ${
          videoUrl && !selectedFile
            ? 'border-emerald-400 bg-emerald-50/20 shadow-sm'
            : 'border-slate-300 hover:border-slate-400 bg-white hover:bg-slate-50/50'
        }`}>
          <div className="w-12 h-12 mx-auto rounded-xl bg-slate-100 flex items-center justify-center text-slate-500 mb-4">
            <Link2 className="w-6 h-6" />
          </div>
          <h3 className="text-base font-semibold text-slate-800 mb-2">Paste Reel URL</h3>
          <p className="text-xs text-slate-500 mb-4">Works with Instagram, TikTok, and YouTube Shorts.</p>
          <input
            type="url"
            value={videoUrl}
            onChange={handleUrlChange}
            placeholder="https://www.instagram.com/reel/..."
            className="w-full text-sm px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all"
          />
        </div>

        {/* Upload Box */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`relative border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all duration-200 flex flex-col justify-center ${
            isDragOver
              ? 'border-emerald-500 bg-emerald-50/50 scale-[1.01]'
              : selectedFile
              ? 'border-emerald-400 bg-emerald-50/20 shadow-sm'
              : 'border-slate-300 hover:border-slate-400 bg-white hover:bg-slate-50/50'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="video/mp4,video/quicktime,video/webm,video/x-matroska"
            className="hidden"
            onChange={handleFileChange}
          />

          <div className="w-12 h-12 mx-auto rounded-xl bg-slate-100 flex items-center justify-center text-slate-500 mb-4">
            {selectedFile ? <FileVideo className="w-6 h-6 text-emerald-600" /> : <UploadCloud className="w-6 h-6" />}
          </div>
          
          {selectedFile ? (
            <div>
              <p className="text-sm font-semibold text-slate-900 truncate px-2">{selectedFile.name}</p>
              <p className="text-xs text-slate-500 mt-1">
                {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • Ready
              </p>
            </div>
          ) : (
            <div>
              <h3 className="text-base font-semibold text-slate-800 mb-2">Upload MP4</h3>
              <p className="text-xs text-slate-500">
                Drag & drop or click to browse (up to 120MB)
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Validation or General Error */}
      {(validationError || error) && (
        <div className="mt-6 p-4 rounded-xl bg-red-50 border border-red-200 flex items-start space-x-3 text-red-800">
          <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
          <div className="text-sm leading-snug">
            <p className="font-semibold">Analysis Notice</p>
            <p className="mt-0.5 text-red-700">{validationError || error}</p>
          </div>
        </div>
      )}

      {/* Action Button */}
      {(selectedFile || videoUrl) ? (
        <div className="mt-8 flex justify-center">
          <button
            onClick={handleStartAnalysis}
            disabled={isAnalyzing}
            className="w-full sm:w-auto px-8 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-xl shadow-md shadow-emerald-600/20 hover:shadow-lg transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-sm"
          >
            <Film className="w-4 h-4" />
            <span>{isAnalyzing ? 'Analyzing Reel...' : 'Analyze Reel Intelligence'}</span>
          </button>
        </div>
      ) : (
        <div className="mt-8 text-center">
          <p className="text-xs text-slate-500 mb-2">Want to see how it works instantly?</p>
          <button
            onClick={onSelectSample}
            type="button"
            className="inline-flex items-center space-x-2 px-4 py-2 bg-slate-100 hover:bg-slate-200/80 text-slate-700 rounded-xl text-xs font-semibold transition border border-slate-200"
          >
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>Explore Pre-analyzed Agriculture Reel Demo</span>
          </button>
        </div>
      )}

      {/* Subtle feature pillars */}
      <div className="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
        <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-xs">
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-1">1. Multimodal AI</div>
          <p className="text-xs text-slate-600">Extracts audio transcript & visual keyframe pacing</p>
        </div>
        <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-xs">
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-1">2. Pattern Library</div>
          <p className="text-xs text-slate-600">Identifies core formula and hook psychology</p>
        </div>
        <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-xs">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">3. Content Concept (Side Feature)</div>
          <p className="text-xs text-slate-500">Drafts a fresh, compliant concept from the formula</p>
        </div>
      </div>
    </div>
  );
}
