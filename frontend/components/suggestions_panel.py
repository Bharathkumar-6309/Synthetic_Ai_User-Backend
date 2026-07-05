import html
import streamlit as st


def render_user_wants_summary(summary: str):
    """Plain-English 'what users want' takeaway, styled as a highlighted band."""
    if not summary:
        return
    st.markdown(
        f"""
        <div class="insight-summary-band">
            <span class="im-summary-label">What Users Want</span>
            <p>{html.escape(summary)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_suggestions(suggestions: list[dict]):
    """Ranked, scannable list of concrete suggestions with priority + category + who raised it."""
    if not suggestions:
        st.info("No suggestions yet — run an interview or survey first, then recalculate insights.")
        return

    cards = []
    for i, s in enumerate(suggestions, start=1):
        priority = (s.get("priority") or "low").lower()
        if priority not in ("high", "medium", "low"):
            priority = "low"
        category = html.escape(s.get("category", "General"))
        suggestion_text = html.escape(s.get("suggestion", ""))
        personas = s.get("personas") or []
        mentioned = f"Raised by {', '.join(html.escape(p) for p in personas)}" if personas else ""

        cards.append(
            f"""
            <div class="suggestion-card">
                <div class="suggestion-rank">{i:02d}</div>
                <div class="suggestion-body">
                    <div class="suggestion-title">{suggestion_text}</div>
                    <div class="suggestion-meta">
                        <span class="priority-badge priority-{priority}">{priority}</span>
                        <span class="category-pill">{category}</span>
                        {f'<span class="mentioned-by">{mentioned}</span>' if mentioned else ''}
                    </div>
                </div>
            </div>
            """
        )

    st.markdown(
        f'<div class="suggestion-list">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )
