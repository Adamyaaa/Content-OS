from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ContentAnalysis(BaseModel):
    topic: str = Field(..., description="Main topic or subject matter of the video")
    hook: str = Field(..., description="First 1-3 seconds hook (verbal and visual)")
    hook_type: str = Field(..., description="Classification of hook e.g., Curiosity, Problem Agitation, Bold Statement, Numbered List")
    content_format: str = Field(..., description="Format e.g., Talking Head, Step-by-Step Tutorial, Field Demonstration, Before/After")
    narrative_structure: List[str] = Field(default_factory=list, description="Sequential narrative flow e.g., ['Hook', 'Problem Reveal', 'Practical Demo', 'CTA']")
    visual_style: str = Field(..., description="Visual aesthetic and lighting e.g., Natural outdoor sunlight, handheld documentary, closeup macro shots")
    visual_pattern: str = Field(..., description="Pattern of camera work and cuts e.g., Rapid cutaways every 2.5s, zoom punches, split-screen")
    target_audience: str = Field(..., description="Specific viewer persona targeted by this reel")
    emotional_trigger: str = Field(..., description="Core emotion evoked e.g., curiosity, validation, relief, awe")
    cta: str = Field(..., description="Call to action used at the end")
    key_claims: List[str] = Field(default_factory=list, description="Explicit claims made in the video regarding methods, yields, or benefits")
    content_strengths: List[str] = Field(default_factory=list, description="Key factors making this content engaging and shareable")
    why_it_might_work: List[str] = Field(default_factory=list, description="Psychological and algorithmic reasons for retention and viral potential")
    content_pattern: str = Field(..., description="Core underlying structural formula abstracted from the video")

class SceneItem(BaseModel):
    timestamp: str = Field(..., description="Time window e.g., '0-3s', '3-8s'")
    purpose: str = Field(..., description="Role of this scene e.g., Hook, Problem Explanation, Demonstration, CTA")
    visual: str = Field(..., description="Specific camera direction, framing, subject action")
    voiceover: str = Field(..., description="Exact spoken words or narration")
    on_screen_text: str = Field(..., description="Text overlays, titles, or emphasis captions")

class GeneratedContent(BaseModel):
    content_concept: str = Field(..., description="Original concept summary rooted in the identified pattern")
    title: str = Field(..., description="Catchy, professional title for the reel")
    hook: str = Field(..., description="High-retention opening spoken line (first 1-3s)")
    hook_type: str = Field(..., description="Pattern type adapted from original")
    script: str = Field(..., description="Full spoken script ready for production delivery")
    scene_breakdown: List[SceneItem] = Field(default_factory=list, description="Scene-by-scene storyboard")
    visual_directions: List[str] = Field(default_factory=list, description="General visual & lighting directives for the creator")
    on_screen_text: List[str] = Field(default_factory=list, description="Summary of key text graphics and captions")
    cta: str = Field(..., description="Brand-aligned, non-pushy educational call to action")
    estimated_duration_seconds: int = Field(default=30, description="Estimated total length in seconds")
    voiceover_url: Optional[str] = Field(default=None, description="URL of generated neural voiceover audio")
    voiceover_engine: Optional[str] = Field(default="Neural HD Engine", description="Voice synthesis engine used")
    rendered_video_url: Optional[str] = Field(default=None, description="URL of rendered 9:16 vertical video reel")
    deduplication_score: Optional[float] = Field(default=32.5, description="Cosine similarity score vs historical scripts")
    deduplication_status: Optional[str] = Field(default="Approved: Unique Angle (<70% threshold)", description="TRD logic gate status")

class QACheck(BaseModel):
    name: str = Field(..., description="Name of the check e.g., 'Brand tone', 'Unsupported claims'")
    status: str = Field(..., description="'PASS', 'WARNING', or 'FAIL'")
    reason: str = Field(..., description="Detailed rationale explaining the check's evaluation")

class QAResult(BaseModel):
    status: str = Field(..., description="Overall QA verdict: 'PASS', 'WARNING', or 'FAIL'")
    overall_score: int = Field(..., description="Safety and quality score from 0 to 100")
    checks: List[QACheck] = Field(default_factory=list, description="Itemized criteria checks")
    issues: List[str] = Field(default_factory=list, description="Potential risks or claims flagged")
    suggestions: List[str] = Field(default_factory=list, description="Actionable recommendations for editorial improvement")

class AnalysisResult(BaseModel):
    analysis_id: str
    filename: str
    created_at: str
    video_url: str
    video_duration: float
    frame_urls: List[str]
    transcript: Dict[str, Any]
    analysis: ContentAnalysis
    generated_content: GeneratedContent
    qa_result: QAResult
    production_readiness: str
