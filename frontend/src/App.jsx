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
import { checkHealth, analyzeVideo, fetchAnalysis, fetchAnalysesList, fetchPatterns, renderVideoReel } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('analyzer'); // 'analyzer' | 'patterns'
  const [health, setHealth] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isRenderingVideo, setIsRenderingVideo] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');
  const [historyOpen, setHistoryOpen] = useState(false);
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

  const handleSelectRun = async (analysisId) => {
    setError('');
    setIsAnalyzing(true);
    setActiveTab('analyzer');
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
            {/* 1. Original Reel & Keyframes */}
            <OriginalContentCard analysisResult={analysisResult} />

            {/* 2. Content Intelligence */}
            <ContentIntelligenceCard analysis={analysisResult.analysis} />

            {/* 3. Why It Works (Formula & Retention) */}
            <WhyItWorksCard analysis={analysisResult.analysis} />

            {/* 4. Generated Content & Storyboard (Hero with Voiceover Player & 9:16 Reel) */}
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
        ) : (
          <UploadSection
            onUploadFile={handleUploadFile}
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
            <span>Powered by Groq Whisper, Gemini 2.5 Flash & Edge Neural Audio</span>
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
    </div>
  );
}
