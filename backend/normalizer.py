"""
BhashaSwarm 3D — Indic Text Normalizer & PII Sanitizer
========================================================
GUARDRAIL #5: Normalizes LLM output before Gnani Timbre v3.0 TTS synthesis.
GUARDRAIL #6: Scrubs accidental real PII (phone, Aadhaar, PAN) for contest compliance.

Sits between the LLM and TTS in the Pipecat pipeline as a FrameProcessor.
"""
import re
import logging
from typing import List, Set

logger = logging.getLogger("bhashaswarm.normalizer")

# ── Gnani Timbre v3.0 Expressive Audio Tags ─────────────────────────────────
ALLOWED_AUDIO_TAGS: Set[str] = {"<laugh>", "<chuckle>", "<sigh>", "<gasp>"}

# ── Indian Number Words (for currency expansion) ────────────────────────────
INDIAN_UNITS = [
    "", "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten", "eleven", "twelve", "thirteen",
    "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
]
INDIAN_TENS = [
    "", "", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety",
]


def _number_to_indian_words(n: int) -> str:
    """Convert integer to Indian English words (lakh/crore system)."""
    if n == 0:
        return "zero"
    if n < 0:
        return "minus " + _number_to_indian_words(-n)

    parts = []

    # Crores (1,00,00,000+)
    if n >= 10_000_000:
        crores = n // 10_000_000
        parts.append(_number_to_indian_words(crores) + " crore")
        n %= 10_000_000

    # Lakhs (1,00,000+)
    if n >= 100_000:
        lakhs = n // 100_000
        parts.append(_number_to_indian_words(lakhs) + " lakh")
        n %= 100_000

    # Thousands
    if n >= 1_000:
        thousands = n // 1_000
        parts.append(_number_to_indian_words(thousands) + " thousand")
        n %= 1_000

    # Hundreds
    if n >= 100:
        hundreds = n // 100
        parts.append(INDIAN_UNITS[hundreds] + " hundred")
        n %= 100

    # Tens and units
    if n >= 20:
        parts.append(INDIAN_TENS[n // 10])
        if n % 10:
            parts.append(INDIAN_UNITS[n % 10])
    elif n > 0:
        parts.append(INDIAN_UNITS[n])

    return " ".join(parts)


def _parse_indian_number(s: str) -> int:
    """Parse an Indian-formatted number string like '1,25,000' or '45000'."""
    return int(s.replace(",", ""))


class PIISanitizer:
    """
    GUARDRAIL #6: Masks real PII patterns for contest compliance.
    Gnani's challenge rules strictly prohibit real personal data in demos.
    """

    # 10-digit Indian mobile (starts with 6-9)
    PHONE_RE = re.compile(r"\b[6-9]\d{9}\b")
    # 12-digit Aadhaar (with optional spaces)
    AADHAAR_RE = re.compile(r"\b(\d{4})\s?(\d{4})\s?(\d{4})\b")
    # PAN card pattern: ABCDE1234F
    PAN_RE = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")
    # Bank account (8-18 digits)
    BANK_ACCOUNT_RE = re.compile(r"\b\d{8,18}\b")

    @staticmethod
    def sanitize(text: str) -> str:
        """Replace any accidental PII with synthetic demo tokens."""
        # Phone numbers → synthetic
        text = PIISanitizer.PHONE_RE.sub("SYN-DEMO-PHONE", text)
        # Aadhaar → synthetic (check before generic bank account)
        text = PIISanitizer.AADHAAR_RE.sub("SYN-DEMO-AADHAAR", text)
        # PAN → synthetic
        text = PIISanitizer.PAN_RE.sub("SYN-DEMO-PAN", text)
        return text


class IndicTextNormalizer:
    """
    Normalizes LLM output for optimal Gnani Timbre v3.0 TTS pronunciation:

    1. Scrubs accidental PII (phone, Aadhaar, PAN) → synthetic tokens
    2. Protects Timbre v3.0 expressive Audio Tags (<laugh>, <chuckle>, etc.)
    3. Strips markdown formatting (*, #, `, ~, _, >) so TTS doesn't read them
    4. Expands Indian currency (₹1,25,000 → "one lakh twenty five thousand rupees")
    5. Spaces out ticket/batch codes for digit-by-digit pronunciation
    6. Cleans excessive whitespace
    """

    def __init__(self):
        self._pii = PIISanitizer()

    @staticmethod
    def normalize_for_tts(text: str) -> str:
        """
        Full normalization pipeline for TTS input text.
        Thread-safe, stateless, can be called from any context.
        """
        if not text or not text.strip():
            return ""

        # ── Step 1: PII Sanitization (Contest Compliance) ────────────────
        text = PIISanitizer.sanitize(text)

        # ── Step 2: Temporarily tokenize valid Timbre v3.0 audio tags ────
        placeholders = {}
        for idx, tag in enumerate(ALLOWED_AUDIO_TAGS):
            token = f"__AUDIOTAG_{idx}__"
            if tag in text:
                placeholders[token] = tag
                text = text.replace(tag, token)

        # ── Step 3: Strip Markdown formatting symbols ────────────────────
        # Remove bold/italic markers
        text = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", text)
        # Remove headers
        text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
        # Remove inline code
        text = re.sub(r"`([^`]+)`", r"\1", text)
        # Remove strikethrough
        text = re.sub(r"~~(.+?)~~", r"\1", text)
        # Remove blockquotes
        text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
        # Remove remaining isolated markdown symbols
        text = re.sub(r"[~]+", "", text)
        # Remove bullet points
        text = re.sub(r"^[-*+]\s+", "", text, flags=re.MULTILINE)

        # ── Step 4: Expand Indian currency ───────────────────────────────
        def _expand_rupees(match):
            try:
                amount = _parse_indian_number(match.group(1))
                return _number_to_indian_words(amount) + " rupees"
            except (ValueError, IndexError):
                return match.group(0)

        text = re.sub(r"₹\s*(\d[\d,]*)", _expand_rupees, text)
        text = re.sub(
            r"\bRs\.?\s*(\d[\d,]*)", _expand_rupees, text, flags=re.IGNORECASE
        )

        # ── Step 5: Space out ticket/batch codes for clear pronunciation ─
        def _space_code(match):
            code = match.group(1)
            return "ID " + " ".join(list(code))

        # Matches #SYN402, #ABC1234, etc.
        text = re.sub(r"#([A-Z0-9\-]{3,12})", _space_code, text)

        # ── Step 6: Expand standalone large numbers ──────────────────────
        def _expand_large_number(match):
            try:
                num = _parse_indian_number(match.group(0))
                if num >= 1000:
                    return _number_to_indian_words(num)
            except ValueError:
                pass
            return match.group(0)

        text = re.sub(r"\b\d{1,2}(?:,\d{2})*,\d{3}\b", _expand_large_number, text)

        # ── Step 7: Expand date formats (DD/MM/YYYY) ────────────────────
        def _expand_date(match):
            day, month, year = match.group(1), match.group(2), match.group(3)
            months = {
                "01": "January", "02": "February", "03": "March",
                "04": "April", "05": "May", "06": "June",
                "07": "July", "08": "August", "09": "September",
                "10": "October", "11": "November", "12": "December",
            }
            month_name = months.get(month, month)
            return f"{int(day)} {month_name} {year}"

        text = re.sub(
            r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", _expand_date, text
        )

        # ── Step 8: Restore valid Timbre v3.0 expressive audio tags ──────
        for token, tag in placeholders.items():
            text = text.replace(token, tag)

        # ── Step 9: Clean up whitespace ──────────────────────────────────
        text = re.sub(r"\s+", " ", text).strip()

        return text


# ── Convenience singleton ───────────────────────────────────────────────────
normalizer = IndicTextNormalizer()

