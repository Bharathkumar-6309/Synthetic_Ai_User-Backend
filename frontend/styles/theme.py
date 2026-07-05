"""
Theme constants and Plotly template for the "Signal" (Modern SaaS) visual identity.
Import PLOTLY_LAYOUT and apply it to every chart via fig.update_layout(**PLOTLY_LAYOUT)
so all visualizations share one consistent look.
"""

# ── Core palette (kept in sync with styles/custom.css) ───────────────────────
BG = "#F7F7FC"
BG_ALT = "#F0EFFB"
INK = "#14141F"
INK_SOFT = "#62627A"
VIOLET = "#6D4FF2"
VIOLET_DARK = "#4B33C7"
VIOLET_TINT = "#ECE7FE"
TEAL = "#0FBF9F"
TEAL_DARK = "#0A9A81"
TEAL_TINT = "#DFF9F3"
CORAL = "#F2554F"
CORAL_TINT = "#FDE4E2"
CARD_BG = "#FFFFFF"
BORDER = "#E7E6F3"

FONT_DISPLAY = "Sora, -apple-system, sans-serif"
FONT_BODY = "Inter, -apple-system, sans-serif"
FONT_MONO = "JetBrains Mono, SFMono-Regular, monospace"

# Sentiment / status colors used across dashboard + charts
SENTIMENT_COLORS = {
    "Positive": TEAL,
    "Neutral": VIOLET,
    "Negative": CORAL,
}

SCORE_TIER_COLORS = {
    "high": TEAL,    # >= 7
    "mid": VIOLET,   # 4 - 6.9
    "low": CORAL,    # < 4
}

# Discrete colorway used for multi-series/categorical charts
COLORWAY = [VIOLET, TEAL, CORAL, VIOLET_DARK, "#9B87F5", "#5BD8BE"]

# Continuous scale used for adoption-score bar charts
CONTINUOUS_SCALE = [[0, CORAL_TINT], [0.5, VIOLET_TINT], [1, TEAL_TINT]]

# Shared Plotly layout — spread this into fig.update_layout(**PLOTLY_LAYOUT)
PLOTLY_LAYOUT = dict(
    paper_bgcolor=CARD_BG,
    plot_bgcolor=CARD_BG,
    font=dict(family=FONT_BODY, color=INK, size=13),
    title_font=dict(family=FONT_DISPLAY, color=INK, size=17),
    colorway=COLORWAY,
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)


def score_tier(score: float) -> str:
    """Returns 'high' | 'mid' | 'low' for a 0-10 adoption score."""
    if score >= 7:
        return "high"
    if score >= 4:
        return "mid"
    return "low"


def load_css(path: str = "styles/custom.css") -> str:
    """Load the CSS file.

    Resolves relative to this file's own directory (styles/) rather than the
    process's current working directory, since Streamlit Cloud runs the app
    with the repo root as cwd, not the folder containing the main script —
    a plain relative path like "styles/custom.css" silently fails there.
    """
    import os

    filename = os.path.basename(path)
    here = os.path.dirname(os.path.abspath(__file__))
    resolved = os.path.join(here, filename)
    try:
        with open(resolved, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
