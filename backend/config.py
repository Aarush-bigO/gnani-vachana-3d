"""
Gnani Vachana 3D — Configuration & Voice-Model Validation
========================================================
Strict validation for Gnani Vachana credentials, model-voice compatibility,
language candidate arrays, and STT keyword sanitization.
"""
import os
from typing import Dict, List, Tuple

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

# ── Gnani Timbre v3.0 Validated Voice Registry ──────────────────────────────
TIMBRE_V30_VOICES: List[str] = [
    "Riyaa", "Avinash", "Shubham", "Chetana", "Devansh",
    "Harshad", "Kalpana", "Lakshmi", "Prakash", "Shivani",
    "Tarika", "Vasudha", "Yashraj",
]

TIMBRE_V25_VOICES: List[str] = [
    "Pranav", "Nalini", "Kaveri", "Asmita", "Deepak",
    "Pooja", "Ranjani", "Kishore", "Lata",
]

VOICE_MODEL_REGISTRY: Dict[str, List[str]] = {
    "timbre-v3.0": TIMBRE_V30_VOICES,
    "timbre-v2.5": TIMBRE_V25_VOICES,
}

# 3D Avatar Character -> Gnani Timbre Voice Mapping (Gen-Z Indian Avatars)
CHARACTER_VOICE_ALIASES: Dict[str, str] = {
    "Riya": "Riyaa",
    "Chetana": "Chetana",
    "Kabir": "Avinash",
    "Shubham": "Shubham",
    "Kalpana": "Kalpana",
    "riya": "Riyaa",
    "chetana": "Chetana",
    "kabir": "Avinash",
    "shubham": "Shubham",
    "kalpana": "Kalpana",
    # Legacy aliases
    "Julia": "Riyaa",
    "Jenny": "Chetana",
    "Harri": "Avinash",
    "Avaturn": "Shubham",
    "MPFB": "Kalpana",
    "Brunette": "Riyaa",
    "VRoid": "Chetana",
    "AvatarSDK": "Avinash",
}

SUPPORTED_LANGUAGES: Dict[str, str] = {
    "hi-IN": "Hindi / Hinglish (Code-Mix)",
    "en-IN": "Indian English",
    "ta-IN": "Tamil / Tanglish",
    "te-IN": "Telugu",
    "kn-IN": "Kannada / Kanglish",
    "ml-IN": "Malayalam",
    "mr-IN": "Marathi",
    "bn-IN": "Bengali",
    "gu-IN": "Gujarati",
    "pa-IN": "Punjabi",
}

# Maximum 4 language candidates for Prisma v3.0 indic-auto detection
DEFAULT_LANGUAGE_CANDIDATES: List[str] = ["hi-IN", "en-IN", "ta-IN", "bn-IN"]

# Gnani Timbre v3.0 supported expressive Audio Tags
VALID_EXPRESSIVE_TAGS: List[str] = ["<laugh>", "<chuckle>", "<sigh>", "<gasp>"]

# Tokens that cause HTTP 400 in STT context/keywords
BANNED_STT_TOKENS: List[str] = ["<|", "|>"]


def sanitize_stt_keywords(keywords: List[str]) -> List[str]:
    """
    GUARDRAIL #3: Strip prompt-injection delimiters that trigger HTTP 400.
    Gnani Prisma v3.0 rejects any keyword or context containing '<|' or '|>'.
    """
    sanitized = []
    for kw in keywords:
        clean = kw
        for token in BANNED_STT_TOKENS:
            clean = clean.replace(token, "")
        clean = clean.strip()
        if clean:
            sanitized.append(clean)
    return sanitized


class Settings(BaseSettings):
    """
    Application settings loaded from environment with strict Gnani validation.
    """
    # ── Gnani Vachana API Credentials ────────────────────────────────────
    gnani_api_key: str = os.getenv("GNANI_API_KEY", "")
    gnani_stt_ws_url: str = os.getenv(
        "GNANI_STT_WS_URL", "wss://api.vachana.ai/stt/v3/stream"
    )
    gnani_tts_ws_url: str = os.getenv(
        "GNANI_TTS_WS_URL", "wss://api.vachana.ai/api/v1/tts"
    )
    gnani_tts_sse_url: str = os.getenv(
        "GNANI_TTS_SSE_URL", "https://api.vachana.ai/api/v1/tts/sse"
    )
    gnani_tts_rest_url: str = os.getenv(
        "GNANI_TTS_REST_URL", "https://api.vachana.ai/api/v1/tts/inference"
    )

    # ── LLM Configuration (Evon or OpenAI-compatible) ───────────────────
    llm_api_key: str = os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    llm_base_url: str = os.getenv("EVON_BASE_URL", "https://api.openai.com/v1")
    llm_model: str = os.getenv("EVON_MODEL", "gpt-4o-mini")

    # ── TTS Defaults ────────────────────────────────────────────────────
    default_tts_model: str = os.getenv("DEFAULT_TTS_MODEL", "timbre-v3.0")
    default_tts_voice: str = os.getenv("DEFAULT_TTS_VOICE", "Riyaa")
    default_language: str = os.getenv("DEFAULT_LANGUAGE", "hi-IN")
    sample_rate: int = 16000
    pcm_frame_size: int = 1024  # bytes per STT frame (512 samples × 2 bytes)

    # ── Server ──────────────────────────────────────────────────────────
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    frontend_port: int = int(os.getenv("FRONTEND_PORT", "3000"))

    def validate_voice_model(self, model: str, voice: str) -> Tuple[str, str]:
        """
        GUARDRAIL #4: Enforce voice-model compatibility.
        - timbre-v2.0 is permanently retired by Gnani.ai.
        - Character aliases mapped to Gnani Timbre voices.
        - Enforces valid voice-model pairing with safe defaults.
        """
        if model == "timbre-v2.0":
            raise ValueError(
                "timbre-v2.0 is permanently retired by Gnani.ai. "
                "Use 'timbre-v3.0' (recommended) or 'timbre-v2.5'."
            )
        if model not in VOICE_MODEL_REGISTRY:
            model = "timbre-v3.0"

        if voice in CHARACTER_VOICE_ALIASES:
            voice = CHARACTER_VOICE_ALIASES[voice]

        # Check if voice belongs to the requested model
        valid_voices = VOICE_MODEL_REGISTRY[model]
        if voice in valid_voices:
            return model, voice

        # If voice belongs to the other model, auto-adjust model
        other_model = "timbre-v2.5" if model == "timbre-v3.0" else "timbre-v3.0"
        if voice in VOICE_MODEL_REGISTRY[other_model]:
            return other_model, voice

        # Fallback to default voice of current model
        return model, valid_voices[0]

    def get_stt_auth_headers(self) -> Dict[str, str]:
        """Returns authentication headers for Gnani Vachana STT WebSocket."""
        return {
            "Authorization": f"Bearer {self.gnani_api_key}",
            "Content-Type": "application/json",
        }

    def get_tts_auth_headers(self) -> Dict[str, str]:
        """Returns authentication headers for Gnani Vachana TTS endpoints."""
        return {
            "Authorization": f"Bearer {self.gnani_api_key}",
            "Content-Type": "application/json",
        }


settings = Settings()

