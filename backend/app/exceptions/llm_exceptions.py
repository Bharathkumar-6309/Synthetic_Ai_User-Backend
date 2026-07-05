class LLMError(Exception):
    """Base class for all LLM-layer failures."""


class LLMTimeoutError(LLMError):
    """Raised when the LLM provider does not respond within LLM_TIMEOUT_SECONDS."""


class LLMRateLimitError(LLMError):
    """Raised when the LLM provider returns a 429 / rate-limit response."""


class LLMResponseParsingError(LLMError):
    """Raised when the LLM response cannot be parsed into the expected structured schema."""


class LLMUnavailableError(LLMError):
    """Raised when no LLM provider (Gemini, Ollama) is reachable/configured."""
