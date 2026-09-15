import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import UploadSection from './components/UploadSection';
import ProcessingTracker from './components/ProcessingTracker';
import OriginalContentCard from './components/OriginalContentCard';
import ContentIntelligenceCard from './components/ContentIntelligenceCard';
import WhyItWorksCard from './components/WhyItWorksCard';
import GeneratedContentCard from './components/GeneratedContentCard';
import BrandQACard from './components/BrandQACard';
import HistoryDrawer from './components/HistoryDrawer';
import PatternLibraryView from './components/PatternLibraryView';
import SettingsModal from './components/SettingsModal';
import VideoGenerationCard from './components/VideoGenerationCard';
import { checkHealth, analyzeVideo, fetchAnalysis, fetchAnalysesList, fetchPatterns, renderVideoReel } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('analyzer'); // 'analyzer' | 'patterns'
  const [resultTab, setResultTab] = useState('tier1'); // 'tier1' | 'tier2'
  const [health, setHealth] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isRenderingVideo, setIsRenderingVideo] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');
  const [historyOpen, setHistoryOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [pastRuns, setPastRuns] = useState([]);
  const [patterns, setPatterns] = useState([]);

  // Load health, history, and pattern library on mount
  useEffect(() => {
    async function init() {
      const h = await checkHealth();
      setHealth(h);
      const runs = await fetchAnalysesList();
      setPastRuns(runs);
      const pats = await fetchPatterns();
      setPatterns(pats);
    }
    init();
  }, []);

  const refreshData = async () => {
    const runs = await fetchAnalysesList();
    setPastRuns(runs);
    const pats = await fetchPatterns();
    setPatterns(pats);
  };

  const handleUploadFile = async (file) => {
    setError('');
    setIsAnalyzing(true);
    setAnalysisResult(null);
    setResultTab('tier1');

    try {
      const result = await analyzeVideo(file);
      setAnalysisResult(result);
      await refreshData();
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'An unexpected error occurred during processing.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleUploadUrl = async (url) => {
    setError('');
    setIsAnalyzing(true);
    setAnalysisResult(null);
    setResultTab('tier1');

    try {
      const response = await fetch('https://organic-content-os-backend.onrender.com/api/analyze-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to analyze URL');
      }
      const result = await response.json();
      setAnalysisResult(result);
      await refreshData();
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'An unexpected error occurred during processing.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSelectRun = async (analysisId) => {
    setError('');
    setIsAnalyzing(true);
    setActiveTab('analyzer');
    setResultTab('tier1');
    try {
      const result = await fetchAnalysis(analysisId);
      setAnalysisResult(result);
    } catch (err) {
      setError('Failed to load selected analysis.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setError('');
    setIsAnalyzing(false);
    setIsRenderingVideo(false);
    setActiveTab('analyzer');
    setResultTab('tier1');
  };

  const handleRenderVideo = async () => {
    if (!analysisResult?.analysis_id) return;
    setIsRenderingVideo(true);
    setError('');

    try {
      const renderRes = await renderVideoReel(analysisResult.analysis_id);
      const videoUrl = renderRes.rendered_video_url || renderRes.video_url;
      if (videoUrl) {
        setAnalysisResult((prev) => ({
          ...prev,
          generated_content: {
            ...prev.generated_content,
            rendered_video_url: videoUrl,
          },
        }));
        await refreshData();
      }
    } catch (err) {
      console.error('Video render error:', err);
      setError(err.message || 'Failed to render 9:16 video reel.');
    } finally {
      setIsRenderingVideo(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      {/* Top Navigation */}
      <Header
        health={health}
        onOpenHistory={() => setHistoryOpen(true)}
        historyCount={pastRuns.length}
        onReset={handleReset}
        activeTab={activeTab}
        onTabChange={setActiveTab}
        onOpenSettings={() => setSettingsOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'patterns' ? (
          <PatternLibraryView
            patterns={patterns}
            onSelectPatternDemo={() => handleSelectRun('sample_demo')}
          />
        ) : isAnalyzing ? (
          <ProcessingTracker />
        ) : analysisResult ? (
          <div className="space-y-8 animate-fadeIn">
            {/* 1. Original Reel & Keyframes (Always visible context) */}
            <OriginalContentCard analysisResult={analysisResult} />

            {/* Sub-Tabs for Results */}
            <div className="border-b border-slate-200 mt-8">
              <nav className="-mb-px flex space-x-8" aria-label="Tabs">
                <button
                  onClick={() => setResultTab('tier1')}
                  className={`${
                    resultTab === 'tier1'
                      ? 'border-emerald-500 text-emerald-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                  } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2`}
                >
                  Tier 1: Content Idea & Intelligence
                </button>
                <button
                  onClick={() => setResultTab('tier2')}
                  className={`${
                    resultTab === 'tier2'
                      ? 'border-slate-300 text-slate-600'
                      : 'border-transparent text-slate-400 hover:text-slate-600 hover:border-slate-200'
                  } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2`}
                >
                  Tier 2: Automated Video Generation
                </button>
              </nav>
            </div>

            {/* Tab Contents */}
            {resultTab === 'tier1' && (
              <div className="space-y-8 animate-fadeIn">
                {/* 2. Content Intelligence */}
                <ContentIntelligenceCard analysis={analysisResult.analysis} />

                {/* 3. Why It Works (Formula & Retention) */}
                <WhyItWorksCard analysis={analysisResult.analysis} />

                {/* 4. Generated Content & Storyboard (Hero with Voiceover Player) */}
                <GeneratedContentCard
                  generatedContent={analysisResult.generated_content}
                  onRenderVideo={handleRenderVideo}
                  isRenderingVideo={isRenderingVideo}
                />

                {/* 5. Brand QA & Compliance Critic */}
                <BrandQACard
                  qaResult={analysisResult.qa_result}
                  productionReadiness={analysisResult.production_readiness}
                  onReset={handleReset}
                />
              </div>
            )}

            {resultTab === 'tier2' && (
              <div className="space-y-8 animate-fadeIn">
                <VideoGenerationCard
                  generatedContent={analysisResult.generated_content}
                  onRenderVideo={handleRenderVideo}
                  isRenderingVideo={isRenderingVideo}
                />
              </div>
            )}
          </div>
        ) : (
          <UploadSection
            onUploadFile={handleUploadFile}
            onUploadUrl={handleUploadUrl}
            onSelectSample={() => handleSelectRun('sample_demo')}
            isAnalyzing={isAnalyzing}
            error={error}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-2">
          <p>© 2026 Organic Journals • Client Demo Prototype</p>
          <p className="flex items-center space-x-2">
            <span>Powered by Groq Whisper, Gemini 3.6 Flash & Studio Audio Engine</span>
          </p>
        </div>
      </footer>

      {/* History Slide-out Drawer */}
      <HistoryDrawer
        isOpen={historyOpen}
        onClose={() => setHistoryOpen(false)}
        pastRuns={pastRuns}
        onSelectRun={handleSelectRun}
      />

      {/* Settings & API Key Manager Modal */}
      <SettingsModal
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        onSettingsUpdated={async () => {
          const h = await checkHealth();
          setHealth(h);
        }}
      />
    </div>
  );
}
