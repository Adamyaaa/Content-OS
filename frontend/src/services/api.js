const API_BASE = '/api';

export async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Health check failed');
    return await res.json();
  } catch (err) {
    return {
      status: 'error',
      groq_configured: false,
      gemini_configured: false,
      ffmpeg_available: false,
      error: err.message,
    };
  }
}

export async function analyzeVideo(file, onProgressUpdate) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    let errorDetail = 'Failed to analyze video';
    try {
      const errJson = await res.json();
      errorDetail = errJson.detail || errorDetail;
    } catch {
      // Fallback
    }
    throw new Error(errorDetail);
  }

  return await res.json();
}

export async function fetchAnalysis(analysisId) {
  const res = await fetch(`${API_BASE}/analysis/${analysisId}`);
  if (!res.ok) {
    throw new Error('Analysis not found');
  }
  return await res.json();
}

export async function fetchAnalysesList() {
  try {
    const res = await fetch(`${API_BASE}/analyses`);
    if (!res.ok) throw new Error('Failed to load history');
    return await res.json();
  } catch (err) {
    console.error('Error fetching past analyses:', err);
    return [];
  }
}

export async function fetchPatterns() {
  try {
    const res = await fetch(`${API_BASE}/patterns`);
    if (!res.ok) throw new Error('Failed to load patterns');
    return await res.json();
  } catch (err) {
    console.error('Error fetching patterns:', err);
    return [];
  }
}
