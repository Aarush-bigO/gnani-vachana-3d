# ADR 0003: Indic Unicode Matra Preservation

## Status
Accepted

## Context
Standard Python string tokenizers and regexes like `re.findall(r"\w+", text)` only match ASCII letters/digits and underscore. In Indic scripts (Devanagari, Kannada, Telugu, Tamil, Malayalam, etc.), dependent vowel marks (*matras*) and conjunct markers (*viramas*) fall outside ASCII word characters, causing composite words to be shredded into meaningless fragments.

## Decision
Explicitly incorporate the Unicode block range `\u0900-\u0D7F` in all regular expressions across `backend/reasoning_engine.py` and `backend/massive_db.py`:
`re.sub(r"[^\w\s\u0900-\u0D7F]", " ", raw_text.lower())`

## Consequences
* **Positive:** Preserves native Devanagari (Hindi, Marathi), Kannada, and other scripts intact.
* **Positive:** Enables 100% deterministic keyword matching for grassroots agricultural (Mandi) and civic queries.
