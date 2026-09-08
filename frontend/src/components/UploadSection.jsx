import React, { useState, useRef } from 'react';
import { UploadCloud, Film, CheckCircle2, AlertCircle, FileVideo, Sparkles } from 'lucide-react';

export default function UploadSection({ onUploadFile, onSelectSample, isAnalyzing, error }) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [validationError, setValidationError] = useState('');
  const fileInputRef = useRef(null);

  const allowedFormats = ['.mp4', '.mov', '.webm', '.mkv'];

  const validateAndSetFile = (file) => {
    setValidationError('');
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

  const handleStartAnalysis = () => {
    if (selectedFile) {
      onUploadFile(selectedFile);
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
          Analyze a successful reel and generate an original, brand-safe content concept.
        </h1>
        <p className="text-slate-600 text-base max-w-xl mx-auto leading-relaxed">
          Upload any competitor or trending agriculture reel. Organic Content OS extracts the underlying narrative structure and crafts a fresh, compliant script for <span className="font-semibold text-slate-900">Organic Journals</span>.
        </p>
      </div>

      {/* Upload Box */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center cursor-pointer transition-all duration-200 ${
          isDragOver
            ? 'border-emerald-500 bg-emerald-50/50 scale-[1.01]'
            : selectedFile
            ? 'border-emerald-400 bg-emerald-50/20'
            : 'border-slate-300 hover:border-slate-400 bg-white hover:bg-slate-50/50'
        } shadow-sm`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="video/mp4,video/quicktime,video/webm,video/x-matroska"
          className="hidden"
          onChange={handleFileChange}
        />

        <div className="flex flex-col items-center justify-center space-y-4">
          {selectedFile ? (
            <div className="w-16 h-16 rounded-2xl bg-emerald-100 flex items-center justify-center text-emerald-600 shadow-inner">
              <FileVideo className="w-8 h-8" />
            </div>
          ) : (
            <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center text-slate-500">
              <UploadCloud className="w-8 h-8" />
            </div>
          )}

          <div>
            {selectedFile ? (
              <div>
                <p className="text-sm font-semibold text-slate-900">{selectedFile.name}</p>
                <p className="text-xs text-slate-500 mt-1">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • Ready to analyze
                </p>
              </div>
            ) : (
              <div>
                <p className="text-base font-semibold text-slate-800">
                  Click to select or drag & drop video
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  Supported formats: <span className="font-medium text-slate-700">MP4, MOV, WEBM</span> (up to 120MB)
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Validation or General Error */}
      {(validationError || error) && (
        <div className="mt-4 p-4 rounded-xl bg-red-50 border border-red-200 flex items-start space-x-3 text-red-800">
          <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
          <div className="text-sm leading-snug">
            <p className="font-semibold">Analysis Notice</p>
            <p className="mt-0.5 text-red-700">{validationError || error}</p>
          </div>
        </div>
      )}

      {/* Action Button */}
      {selectedFile ? (
        <div className="mt-6 flex justify-center">
          <button
            onClick={handleStartAnalysis}
            disabled={isAnalyzing}
            className="w-full sm:w-auto px-8 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-xl shadow-md shadow-emerald-600/20 hover:shadow-lg transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-sm"
          >
            <Film className="w-4 h-4" />
            <span>Analyze Reel & Generate Content</span>
          </button>
        </div>
      ) : (
        <div className="mt-6 text-center">
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
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-1">1. Intelligence</div>
          <p className="text-xs text-slate-600">Extracts audio transcript & visual keyframe patterns</p>
        </div>
        <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-xs">
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-1">2. Originality</div>
          <p className="text-xs text-slate-600">Identifies core formula and creates an original script</p>
        </div>
        <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-xs">
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-1">3. Brand QA</div>
          <p className="text-xs text-slate-600">Verifies tone, originality, and agricultural claims</p>
        </div>
      </div>
    </div>
  );
}
