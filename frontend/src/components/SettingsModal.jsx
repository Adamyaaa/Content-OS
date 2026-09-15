import React, { useState, useEffect } from 'react';
import {
  X,
  Key,
  CheckCircle2,
  AlertCircle,
  Eye,
  EyeOff,
  Sparkles,
  Zap,
  Volume2,
  Video,
  ShieldCheck,
  Save,
  HelpCircle
} from 'lucide-react';

export default function SettingsModal({ isOpen, onClose, onSettingsUpdated }) {
  const [loading, setLoading] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [settingsData, setSettingsData] = useState(null);
  const [showKeys, setShowKeys] = useState({});
  const [testResults, setTestResults] = useState({});
  const [testingProvider, setTestingProvider] = useState(null);

  const [formKeys, setFormKeys] = useState({
    groq_api_key: '',
    gemini_api_key: '',
    openai_api_key: '',
    elevenlabs_api_key: '',
    piapi_key: '',
    rapidapi_key: ''
  });

  useEffect(() => {
    if (isOpen) {
      fetchSettings();
      setSaveSuccess(false);
      setTestResults({});
    }
  }, [isOpen]);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/settings');
      if (res.ok) {
        const data = await res.json();
        setSettingsData(data);
      }
    } catch (err) {
      console.error('Failed to load settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleShowKey = (field) => {
    setShowKeys((prev) => ({ ...prev, [field]: !prev[field] }));
  };

  const handleTestKey = async (provider, keyVal, fieldName) => {
    const keyToTest = keyVal.trim() || (settingsData?.masked_keys?.[provider] ? 'USE_EXISTING' : '');
    if (!keyToTest) {
      setTestResults((prev) => ({
        ...prev,
        [provider]: { ok: false, message: 'Please enter a key to test.' }
      }));
      return;
    }

    setTestingProvider(provider);
    try {
      // If testing existing masked key, we submit an empty string or the field value
      const res = await fetch('/api/settings/test-key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider,
          key: keyVal.trim()
        })
      });
      const data = await res.json();
      setTestResults((prev) => ({
        ...prev,
        [provider]: data
      }));
    } catch (err) {
      setTestResults((prev) => ({
        ...prev,
        [provider]: { ok: false, message: `Network error: ${err.message}` }
      }));
    } finally {
      setTestingProvider(null);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {};
      Object.entries(formKeys).forEach(([k, v]) => {
        if (v && v.trim()) {
          payload[k] = v.trim();
        }
      });

      const res = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        setSaveSuccess(true);
        await fetchSettings();
        if (onSettingsUpdated) onSettingsUpdated();
        setTimeout(() => setSaveSuccess(false), 3000);
      }
    } catch (err) {
      console.error('Save failed:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const keyConfig = [
    {
      provider: 'groq',
      field: 'groq_api_key',
      label: 'Groq API Key',
      icon: <Zap className="w-4 h-4 text-amber-500" />,
      purpose: 'Whisper High-Speed Video Audio Transcription',
      placeholder: settingsData?.masked_keys?.groq || 'gsk_...',
      isConfigured: settingsData?.groq_configured,
      docsUrl: 'https://console.groq.com/keys',
      badge: 'Transcription Engine'
    },
    {
      provider: 'gemini',
      field: 'gemini_api_key',
      label: 'Google Gemini API Key',
      icon: <Sparkles className="w-4 h-4 text-blue-500" />,
      purpose: 'Multimodal Video Intelligence, Script Generation & Brand QA (Gemini 3.6-flash)',
      placeholder: settingsData?.masked_keys?.gemini || 'AQ.... or AIzaSy...',
      isConfigured: settingsData?.gemini_configured,
      docsUrl: 'https://aistudio.google.com/',
      badge: 'Core Intelligence'
    },
    {
      provider: 'elevenlabs',
      field: 'elevenlabs_api_key',
      label: 'ElevenLabs API Key (Secret Key)',
      icon: <Volume2 className="w-4 h-4 text-emerald-500" />,
      purpose: 'Ultra-Realistic Human Voiceovers (Requires Secret Key starting with "sk_")',
      placeholder: settingsData?.masked_keys?.elevenlabs || 'sk_...',
      isConfigured: settingsData?.elevenlabs_configured,
      docsUrl: 'https://elevenlabs.io/app/settings/api-keys',
      badge: 'Studio Voiceover',
      warning: 'Important: Use the Secret Key starting with "sk_", NOT the Key ID.'
    },
    {
      provider: 'openai',
      field: 'openai_api_key',
      label: 'OpenAI API Key',
      icon: <ShieldCheck className="w-4 h-4 text-purple-500" />,
      purpose: 'OpenAI Studio TTS (Onyx / Nova) & Alternative Scripting',
      placeholder: settingsData?.masked_keys?.openai || 'sk-proj-...',
      isConfigured: settingsData?.openai_configured,
      docsUrl: 'https://platform.openai.com/api-keys',
      badge: 'Alternative TTS'
    },
    {
      provider: 'piapi',
      field: 'piapi_key',
      label: 'PiAPI Key',
      icon: <Video className="w-4 h-4 text-rose-500" />,
      purpose: 'FLUX 8K Macro Keyframes & Kling AI Video Generation',
      placeholder: settingsData?.masked_keys?.piapi || '3e95...',
      isConfigured: settingsData?.piapi_configured,
      docsUrl: 'https://piapi.ai/',
      badge: 'AI Video Engine'
    },
    {
      provider: 'rapidapi',
      field: 'rapidapi_key',
      label: 'RapidAPI Key',
      icon: <Video className="w-4 h-4 text-cyan-500" />,
      purpose: 'Download videos directly from Instagram, TikTok, and YouTube URLs',
      placeholder: settingsData?.masked_keys?.rapidapi || '...',
      isConfigured: settingsData?.rapidapi_configured,
      docsUrl: 'https://rapidapi.com/',
      badge: 'Social Media Downloader'
    }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full border border-slate-200 overflow-hidden my-8 animate-in fade-in zoom-in-95 duration-150">
        {/* Modal Header */}
        <div className="bg-slate-900 px-6 py-4 text-white flex items-center justify-between border-b border-slate-800">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center border border-emerald-500/30">
              <Key className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">API Keys & Engine Settings</h3>
              <p className="text-xs text-slate-400">Configure credentials with live connection testing & hot-reload</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <form onSubmit={handleSave} className="p-6 space-y-5 max-h-[75vh] overflow-y-auto">
          {saveSuccess && (
            <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center space-x-2 animate-in fade-in">
              <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600" />
              <span><strong>Success!</strong> API keys updated and active across the pipeline. No restart required.</span>
            </div>
          )}

          <div className="space-y-4">
            {keyConfig.map((item) => {
              const testRes = testResults[item.provider];
              const isTesting = testingProvider === item.provider;

              return (
                <div key={item.provider} className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2.5">
                  <div className="flex items-center justify-between flex-wrap gap-1">
                    <div className="flex items-center space-x-2">
                      {item.icon}
                      <span className="text-xs font-bold text-slate-900">{item.label}</span>
                      <span className="text-[10px] font-semibold text-slate-600 bg-slate-200/80 px-2 py-0.5 rounded-full">
                        {item.badge}
                      </span>
                    </div>

                    <div className="flex items-center space-x-2">
                      {item.isConfigured ? (
                        <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-100/80 px-2 py-0.5 rounded-full flex items-center space-x-1">
                          <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                          <span>Configured</span>
                        </span>
                      ) : (
                        <span className="text-[11px] font-semibold text-slate-500 bg-slate-200 px-2 py-0.5 rounded-full">
                          Not Set
                        </span>
                      )}

                      <a
                        href={item.docsUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="text-[11px] text-emerald-600 hover:underline flex items-center space-x-0.5"
                      >
                        <span>Get Key</span>
                      </a>
                    </div>
                  </div>

                  <p className="text-[11px] text-slate-500">{item.purpose}</p>

                  {item.warning && (
                    <div className="text-[11px] text-amber-700 bg-amber-50/80 border border-amber-200/70 p-2 rounded-lg flex items-center space-x-1.5">
                      <HelpCircle className="w-3.5 h-3.5 shrink-0 text-amber-600" />
                      <span>{item.warning}</span>
                    </div>
                  )}

                  {/* Input & Test Button */}
                  <div className="flex items-center space-x-2">
                    <div className="relative flex-1">
                      <input
                        type={showKeys[item.field] ? 'text' : 'password'}
                        value={formKeys[item.field]}
                        onChange={(e) =>
                          setFormKeys((prev) => ({ ...prev, [item.field]: e.target.value }))
                        }
                        placeholder={item.placeholder}
                        className="w-full text-xs font-mono px-3 py-2 pr-9 bg-white border border-slate-300 rounded-lg focus:outline-hidden focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                      />
                      <button
                        type="button"
                        onClick={() => toggleShowKey(item.field)}
                        className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                      >
                        {showKeys[item.field] ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                      </button>
                    </div>

                    <button
                      type="button"
                      disabled={isTesting || (!formKeys[item.field] && !item.isConfigured)}
                      onClick={() => handleTestKey(item.provider, formKeys[item.field], item.field)}
                      className={`px-3 py-2 text-xs font-semibold rounded-lg border transition shrink-0 ${
                        isTesting
                          ? 'bg-slate-100 text-slate-400 border-slate-200'
                          : 'bg-white hover:bg-slate-100 text-slate-700 border-slate-300'
                      }`}
                    >
                      {isTesting ? 'Testing...' : 'Test Key'}
                    </button>
                  </div>

                  {/* Live Diagnostic Message */}
                  {testRes && (
                    <div
                      className={`text-xs p-2.5 rounded-lg border flex items-start space-x-1.5 ${
                        testRes.ok
                          ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                          : 'bg-amber-50 text-amber-800 border-amber-200'
                      }`}
                    >
                      {testRes.ok ? (
                        <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600 mt-0.5" />
                      ) : (
                        <AlertCircle className="w-4 h-4 shrink-0 text-amber-600 mt-0.5" />
                      )}
                      <span className="text-[11px] leading-relaxed">{testRes.message}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div className="p-3.5 rounded-xl bg-slate-100 border border-slate-200 text-[11px] text-slate-600 space-y-1">
            <p>
              <strong>Smart Multi-Tier Pipeline:</strong> When ElevenLabs or OpenAI have active keys and balance, they are used automatically for voiceover. If credits run out, the engine seamlessly falls back to high-grade Neural HD Audio so creation never stops.
            </p>
          </div>

          {/* Modal Actions */}
          <div className="pt-2 border-t border-slate-200 flex items-center justify-end space-x-2.5">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-xl transition"
            >
              Close
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex items-center space-x-1.5 px-5 py-2 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-md shadow-emerald-600/20 transition disabled:opacity-50"
            >
              <Save className="w-3.5 h-3.5" />
              <span>{loading ? 'Saving...' : 'Save & Apply Keys'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
