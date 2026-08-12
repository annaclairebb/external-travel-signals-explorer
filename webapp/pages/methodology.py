"""Method and limitations page."""

from pathlib import Path
import re

import streamlit as st

from webapp.ui import render_anchor, render_hero, render_section_heading


CONTENT_PATH = Path(__file__).resolve().parents[2] / "WEB_APP_EVIDENCE_CONTENT.md"
SECTION_MARKERS = (
    "## 1. XGBoost, TikTok visibility and sampled Google Maps review activity",
    "## 2. Destination-specific travel-search seasonality",
    "## 3. Travel-search anomaly investigation",
)
FOOTER_MARKER = "## Overall app conclusion"
TAB_LABELS = ("XGBoost & linked sample", "Search seasonality", "Search anomalies")
TAB_PREFIXES = ("methods-xgboost", "methods-seasonality", "methods-anomalies")


def _anchor_subheadings(section: str, prefix: str) -> str:
    """Add unique anchors without adding visible in-page navigation controls."""
    anchored = section
    for heading in re.findall(r"^### (.+)$", section, flags=re.MULTILINE):
        slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
        anchored = anchored.replace(
            f"### {heading}",
            f'<span id="{prefix}-{slug}"></span>\n\n### {heading}',
            1,
        )
    return anchored


def _load_methodology_content() -> tuple[str, tuple[str, str, str], str]:
    """Load and split the approved Markdown source into its three evidence layers."""
    content = CONTENT_PATH.read_text(encoding="utf-8")
    if not all(marker in content for marker in SECTION_MARKERS):
        raise ValueError(
            "WEB_APP_EVIDENCE_CONTENT.md must contain all three approved evidence sections."
        )

    introduction, remaining = content.split(SECTION_MARKERS[0], maxsplit=1)
    first, remaining = remaining.split(SECTION_MARKERS[1], maxsplit=1)
    second, third_and_footer = remaining.split(SECTION_MARKERS[2], maxsplit=1)
    if FOOTER_MARKER not in third_and_footer:
        raise ValueError(
            "WEB_APP_EVIDENCE_CONTENT.md must contain the overall app conclusion."
        )
    third, footer = third_and_footer.split(FOOTER_MARKER, maxsplit=1)

    introduction_lines = introduction.strip().splitlines()
    if introduction_lines and introduction_lines[0].startswith("# "):
        introduction_lines = introduction_lines[1:]

    return (
        "\n".join(introduction_lines).strip(),
        (
            f"{SECTION_MARKERS[0]}\n{first.strip()}",
            f"{SECTION_MARKERS[1]}\n{second.strip()}",
            f"{SECTION_MARKERS[2]}\n{third.strip()}",
        ),
        f"{FOOTER_MARKER}\n{footer.strip()}",
    )


def render(selected_destination: str) -> None:
    """Render the approved evidence, methods and limitations content."""
    del selected_destination  # Methodology applies to the complete prototype.

    render_hero(
        eyebrow="Method & Limitations",
        accent="How should we interpret",
        title="the evidence?",
        copy=(
            "Understand how XGBoost predictions, destination seasonality and "
            "travel-search anomalies are calculated and interpreted and what "
            "their limitations are."
        ),
    )
    render_anchor("methods-evidence-framework")
    render_section_heading("Evidence framework", "Three distinct analytical layers")
    introduction, sections, footer = _load_methodology_content()
    st.markdown(introduction)

    if st.session_state.get("methodology_tab") not in TAB_LABELS:
        st.session_state["methodology_tab"] = TAB_LABELS[0]
    selected_tab = st.radio(
        "Evidence layer",
        options=TAB_LABELS,
        key="methodology_tab",
        label_visibility="collapsed",
        horizontal=True,
    )
    selected_index = TAB_LABELS.index(selected_tab or TAB_LABELS[0])
    selected_section = sections[selected_index]
    selected_prefix = TAB_PREFIXES[selected_index]
    render_anchor(selected_prefix)
    st.markdown(
        _anchor_subheadings(selected_section, selected_prefix),
        unsafe_allow_html=True,
    )

    st.divider()
    anchored_footer = footer.replace(
        "## Overall app conclusion",
        '<span id="methods-overall-conclusion"></span>\n\n## Overall app conclusion',
        1,
    ).replace(
        "## About this prototype",
        '<span id="methods-about-prototype"></span>\n\n## About this prototype',
        1,
    )
    st.markdown(anchored_footer, unsafe_allow_html=True)
