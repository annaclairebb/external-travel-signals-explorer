"""Navigator-inspired presentation styles for the Streamlit app."""

import streamlit as st


def apply_styles() -> None:
    """Apply the shared visual system without changing analytical behaviour."""
    st.markdown(
        """
        <style>
        :root {
            --navy: #07155a;
            --royal: #2447d8;
            --blue: #315cf4;
            --teal: #08d5c5;
            --pink: #f7007f;
            --ink: #101b50;
            --muted: #61709d;
            --surface: #ffffff;
            --canvas: #f5f7ff;
            --line: #dfe5fa;
        }

        html, body, [class*="css"] {
            font-family: Inter, "Avenir Next", "Segoe UI", Arial, sans-serif;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 85% 6%, rgba(8, 213, 197, 0.09), transparent 20rem),
                var(--canvas);
            color: var(--ink);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1240px;
            padding-top: 2.4rem;
            padding-bottom: 4rem;
        }

        [data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 115% 12%, rgba(49, 92, 244, 0.75), transparent 15rem),
                linear-gradient(165deg, #07155a 0%, #142caa 100%);
            border-right: 0;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.8rem;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff;
        }

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            color: rgba(255, 255, 255, 0.68);
            line-height: 1.5;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 0.75rem;
            padding: 0.3rem 0.45rem;
            transition: background 140ms ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: rgba(255, 255, 255, 0.98);
            border: 1px solid rgba(8, 213, 197, 0.55);
            border-radius: 0.75rem;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: var(--ink);
        }

        [data-testid="stSidebar"] [data-testid="stSelectbox"] input[role="combobox"] {
            color: var(--ink) !important;
            -webkit-text-fill-color: var(--ink) !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.18);
        }

        .app-sidebar-title {
            margin: 0 0 0.2rem;
            color: #ffffff;
            font-family: "Avenir Next", Inter, sans-serif;
            font-size: 1.45rem;
            font-weight: 650;
            letter-spacing: -0.035em;
        }

        .app-sidebar-subtitle {
            margin-bottom: 1.7rem;
            color: rgba(255, 255, 255, 0.67);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.13em;
            text-transform: uppercase;
        }

        .sidebar-attribution {
            color: rgba(255, 255, 255, 0.78);
            font-size: 0.72rem;
            line-height: 1.55;
        }

        .sidebar-attribution span {
            color: rgba(255, 255, 255, 0.56);
        }

        .sidebar-explore-label {
            margin: 0.2rem 0 0.5rem;
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.78rem;
            font-weight: 700;
        }

        [data-testid="stSidebar"] [data-testid="stButton"] button {
            min-height: 2rem;
            justify-content: flex-start;
            border: 0;
            border-radius: 0.4rem;
            padding: 0.28rem 0.45rem;
            background: transparent;
            color: #ffffff;
            font-size: 0.78rem;
            font-weight: 500;
            line-height: 1.35;
        }

        [data-testid="stSidebar"] [data-testid="stButton"] button > div,
        [data-testid="stSidebar"] [data-testid="stButton"] button span,
        [data-testid="stSidebar"] [data-testid="stButton"] button [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] [data-testid="stButton"] button p {
            width: 100%;
            justify-content: flex-start;
            text-align: left;
        }

        [data-testid="stSidebar"] [data-testid="stButton"] button:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
        }

        [data-testid="stSidebar"] [class*="st-key-nav_toggle_"] button {
            justify-content: center;
            padding-left: 0;
            padding-right: 0;
            color: rgba(255, 255, 255, 0.72);
        }

        [data-testid="stSidebar"] [class*="st-key-nav_toggle_"] button > div,
        [data-testid="stSidebar"] [class*="st-key-nav_toggle_"] button span,
        [data-testid="stSidebar"] [class*="st-key-nav_toggle_"] button [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] [class*="st-key-nav_toggle_"] button p {
            justify-content: center;
            text-align: center;
        }

        [data-testid="stSidebar"] [class*="st-key-nav_method_"] button {
            padding-left: 1.1rem;
        }

        [data-testid="stSidebar"] [class*="st-key-nav_method_"] button p {
            font-size: 0.875rem;
        }

        [data-testid="stSidebar"] [class*="st-key-nav_method_anchor_"] button {
            padding-left: 1.1rem;
        }

        [data-testid="stSidebar"] [class*="st-key-nav_section_"] button {
            padding-left: 1.1rem;
        }

        [data-testid="stSidebar"] [class*="st-key-nav_section_"] button p,
        [data-testid="stSidebar"] [class*="st-key-nav_subsection_"] button p {
            font-size: 0.875rem;
        }

        [data-testid="stSidebar"] [class*="st-key-nav_subsection_"] button {
            padding-left: 2rem;
        }

        [data-testid="stSidebar"] [class*="st-key-nav_method_child_"] button {
            padding-left: 2rem;
        }

        .sidebar-nav-label {
            display: block;
            padding: 0.28rem 0.45rem;
            border-radius: 0.4rem;
            color: #ffffff !important;
            font-size: 0.875rem;
            font-weight: 500;
            line-height: 1.35;
            text-decoration: none !important;
        }

        .sidebar-nav-label:link,
        .sidebar-nav-label:visited,
        .sidebar-nav-label:hover,
        .sidebar-nav-label:active {
            text-decoration: none !important;
        }

        .sidebar-nav-label:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff !important;
        }

        .sidebar-nav-level-1 {
            padding-left: 1.1rem;
        }

        .sidebar-nav-level-2 {
            padding-left: 2rem;
            color: rgba(255, 255, 255, 0.74) !important;
        }

        .page-anchor {
            display: block;
            position: relative;
            top: -0.75rem;
            visibility: hidden;
        }

        .navigator-hero {
            position: relative;
            overflow: hidden;
            margin-bottom: 1.8rem;
            padding: clamp(2rem, 5vw, 4rem);
            border-radius: 1.75rem;
            background:
                radial-gradient(circle at 91% 13%, rgba(8, 213, 197, 0.24), transparent 15rem),
                radial-gradient(circle at 70% 105%, rgba(247, 0, 127, 0.14), transparent 17rem),
                linear-gradient(128deg, #07155a 0%, #1738bd 62%, #315cf4 100%);
            box-shadow: 0 24px 60px rgba(17, 42, 142, 0.2);
        }

        .navigator-hero::after {
            content: "";
            position: absolute;
            width: 19rem;
            height: 19rem;
            right: -5rem;
            bottom: -11rem;
            border: 1px dashed rgba(255, 255, 255, 0.35);
            border-radius: 50%;
        }

        .hero-eyebrow {
            position: relative;
            z-index: 1;
            margin-bottom: 0;
            color: var(--teal);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .hero-title {
            position: relative;
            z-index: 1;
            max-width: 100%;
            margin: 4.5rem 0 0;
            color: #ffffff;
            font-family: "Avenir Next", Inter, sans-serif;
            font-size: clamp(2.15rem, 5vw, 4rem);
            font-weight: 600;
            letter-spacing: -0.045em;
            line-height: 1.05;
            # white-space: pre-line;
            -webkit-text-fill-color: #ffffff;
        }

        .hero-title .accent {
            color: var(--teal) !important;
            -webkit-text-fill-color: var(--teal);
        }

        .hero-copy {
            position: relative;
            z-index: 1;
            max-width: 720px;
            margin: 3.5rem 0 0;
            color: rgba(255, 255, 255, 0.84);
            font-size: 1.02rem;
            line-height: 1.65;
        }

        .hero-pill {
            position: relative;
            z-index: 1;
            display: inline-block;
            margin-top: 1.45rem;
            padding: 0.58rem 0.9rem;
            border: 1px solid rgba(8, 213, 197, 0.7);
            border-radius: 999px;
            color: #ffffff;
            background: rgba(8, 213, 197, 0.1);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
        }

        .section-kicker {
            margin: 1.4rem 0 0.35rem;
            color: var(--royal);
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .section-title {
            margin: 0 0 1.25rem;
            color: var(--ink);
            font-family: "Avenir Next", Inter, sans-serif;
            font-size: 1.75rem;
            font-weight: 650;
            letter-spacing: -0.035em;
        }

        .destination-card,
        .content-card {
            position: relative;
            z-index: 1;
            min-height: 150px;
            padding: 1.25rem;
            border: 1px solid var(--line);
            border-top: 4px solid var(--teal);
            border-radius: 1.1rem;
            background: var(--surface);
            box-shadow: 0 12px 30px rgba(26, 54, 155, 0.08);
        }

        .destination-card:hover {
            z-index: 100;
        }

        [data-testid="stColumn"]:has(.destination-card) {
            position: relative;
            overflow: visible;
        }

        [data-testid="stColumn"]:has(.destination-card:hover) {
            z-index: 100;
        }

        .destination-card h3,
        .content-card h3 {
            margin: 0 0 0.6rem;
            color: var(--ink);
            font-size: 1.08rem;
            font-weight: 750;
        }

        .destination-card p,
        .content-card p {
            margin: 0;
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.55;
        }

        .destination-summary-card {
            min-height: 335px;
        }

        .card-month {
            margin-bottom: 0.3rem;
            color: var(--royal);
            font-size: 0.8rem;
            font-weight: 800;
        }

        .signal-list {
            margin: 0;
        }

        .signal-list div {
            display: flex;
            justify-content: space-between;
            gap: 0.75rem;
            padding: 0.48rem 0;
            border-bottom: 1px solid #edf0fb;
        }

        .signal-list dt {
            color: var(--muted);
            font-size: 0.76rem;
        }

        .signal-list dd {
            margin: 0;
            color: var(--ink);
            font-size: 0.76rem;
            font-weight: 750;
            text-align: right;
        }

        .signal-list .anomaly-value {
            max-width: 52%;
            line-height: 1.3;
        }

        .anomaly-positive {
            color: #1256c4 !important;
        }

        .anomaly-negative {
            color: #c52b45 !important;
        }

        .anomaly-neutral {
            color: var(--muted) !important;
            font-weight: 650 !important;
        }

        .signal-tooltip {
            position: relative;
            display: inline-block;
            color: inherit;
            cursor: help;
            transition: color 120ms ease;
        }

        .signal-tooltip:hover {
            color: var(--royal);
        }

        .signal-tooltip::after {
            content: attr(data-tooltip);
            position: absolute;
            z-index: 1000;
            left: 0;
            bottom: calc(100% + 0.5rem);
            width: 220px;
            padding: 0.6rem 0.7rem;
            border-radius: 0.55rem;
            background: var(--ink);
            color: #ffffff;
            box-shadow: 0 8px 22px rgba(7, 21, 90, 0.22);
            font-size: 0.7rem;
            font-weight: 500;
            line-height: 1.4;
            opacity: 0;
            pointer-events: none;
            text-align: left;
            transform: translateY(0.25rem);
            transition: opacity 120ms ease, transform 120ms ease;
        }

        .signal-tooltip:hover::after {
            opacity: 1;
            transform: translateY(0);
        }

        .metric-card {
            min-height: 145px;
            box-sizing: border-box;
            padding: 1rem;
            border: 1px solid var(--line);
            border-radius: 1rem;
            background: var(--surface);
            box-shadow: 0 10px 24px rgba(26, 54, 155, 0.07);
        }

        .metric-card-equal-height {
            height: 235px;
        }

        .metric-card-positive {
            border-top: 4px solid #1256c4;
        }

        .metric-card-negative {
            border-top: 4px solid #d12e63;
        }

        .metric-card-monitor {
            border-top: 4px solid #f59e42;
        }

        .metric-card-typical {
            border-top: 4px solid #22b89a;
            background: #ffffff;
        }

        .metric-card-positive .metric-value { color: #1256c4; }
        .metric-card-negative .metric-value { color: #d12e63; }
        .metric-card-monitor .metric-value { color: #b76516; }
        .metric-card-typical .metric-value { color: #22b89a; }

        .metric-label {
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 750;
            line-height: 1.35;
        }

        .metric-value {
            margin-top: 0.55rem;
            color: var(--ink);
            font-size: 1.55rem;
            font-weight: 750;
            letter-spacing: -0.035em;
        }

        .metric-detail {
            margin-top: 0.4rem;
            color: var(--muted);
            font-size: 0.7rem;
            line-height: 1.4;
        }

        .season-context {
            margin-top: 1rem;
            padding: 1rem 1.1rem;
            border: 1px solid var(--line);
            border-left: 5px solid var(--royal);
            border-radius: 0.9rem;
            background: #ffffff;
            box-shadow: 0 10px 24px rgba(26, 54, 155, 0.07);
        }

        .season-context-positive {
            border-left-color: #1256c4;
        }

        .season-context-negative {
            border-left-color: #d12e63;
        }

        .season-context-monitor {
            border-left-color: #f59e42;
        }

        .season-context-typical {
            border-left-color: #22b89a;
        }

        .season-context-kicker {
            color: var(--muted);
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .season-context h3 {
            margin: 0.35rem 0 0.45rem;
            color: var(--ink);
            font-size: 1.05rem;
        }

        .season-context-monitor h3 { color: #b76516; }
        .season-context-typical h3 { color: #22b89a; }

        .season-context p,
        .confidence-line,
        .next-question {
            color: var(--muted);
            font-size: 0.78rem;
            line-height: 1.5;
        }

        .confidence-line,
        .next-question {
            margin-top: 0.55rem;
        }

        .next-question {
            padding-top: 0.55rem;
            border-top: 1px solid #edf0fb;
            color: var(--ink);
        }

        .search-finding {
            margin: 0.65rem 0;
            padding: 0.85rem 1rem;
            border: 1px solid var(--line);
            border-left: 5px solid var(--royal);
            border-radius: 0.8rem;
            background: #ffffff;
        }

        .search-finding-positive { border-left-color: #1256c4; }
        .search-finding-negative { border-left-color: #d12e63; }
        .search-finding-monitor { border-left-color: #f59e42; }

        .search-finding-month {
            color: var(--muted);
            font-size: 0.66rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .search-finding h4 {
            margin: 0.25rem 0 0.35rem;
            color: var(--ink);
            font-size: 0.95rem;
        }

        .search-finding-monitor h4 { color: #b76516; }

        .search-finding p,
        .search-finding-values,
        .search-finding-confidence {
            color: var(--muted);
            font-size: 0.75rem;
            line-height: 1.45;
        }

        .search-finding-values,
        .search-finding-confidence {
            margin-top: 0.4rem;
        }

        .guided-answer {
            margin-top: 0.75rem;
            padding: 1.35rem 1.5rem;
            border: 1px solid var(--line);
            border-left: 5px solid var(--teal);
            border-radius: 0.9rem;
            background: #ffffff;
            box-shadow: 0 10px 24px rgba(26, 54, 155, 0.07);
        }

        .guided-scope-heading {
            margin-top: 0.35rem;
            color: var(--ink);
            font-size: 0.9rem;
            font-weight: 800;
            letter-spacing: 0.035em;
            text-transform: uppercase;
        }

        .guided-scope-spacing {
            margin-top: 1.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid var(--line);
        }

        .guided-scope-copy {
            margin: 0.25rem 0 0.65rem;
            color: var(--muted);
            font-size: 0.82rem;
            line-height: 1.45;
        }

        .guided-answer-label {
            color: var(--teal);
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .guided-answer h3 {
            margin: 0.45rem 0 0.65rem;
            color: var(--ink);
            font-size: 1.3rem;
        }

        .guided-answer p {
            margin: 0;
            color: var(--muted);
            max-width: 72rem;
            font-size: 1rem;
            line-height: 1.65;
        }

        [class*="st-key-guided_questions_"] [data-testid="stButton"] button {
            height: 5.75rem;
            padding: 0.9rem 1rem;
            border-radius: 0.85rem;
        }

        [class*="st-key-guided_questions_"] [data-testid="stButton"] button p {
            font-size: 0.95rem;
            font-weight: 700;
            line-height: 1.35;
            white-space: normal;
        }

        .card-status {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.35rem 0.6rem;
            border-radius: 999px;
            background: #e9fbf9;
            color: #007e76;
            font-size: 0.7rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .navigator-note {
            margin-top: 1.5rem;
            padding: 1rem 1.15rem;
            border-left: 4px solid var(--pink);
            border-radius: 0.65rem;
            background: #ffffff;
            color: var(--muted);
            box-shadow: 0 8px 22px rgba(26, 54, 155, 0.06);
            line-height: 1.55;
        }

        .confidence-card {
            min-height: 17rem;
            padding: 1.25rem 1.35rem;
            border: 1px solid var(--line);
            border-top: 4px solid #ff4d6d;
            border-radius: 1rem;
            background: #ffffff;
            box-shadow: 0 8px 22px rgba(26, 54, 155, 0.06);
        }

        .confidence-card-search {
            border-top-color: #ff4d6d;
        }

        .confidence-card-kicker {
            margin-bottom: 0.45rem;
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .confidence-card h3 {
            margin: 0 0 0.75rem;
            color: var(--ink);
            font-size: 1.15rem;
        }

        .confidence-card p {
            margin: 0 0 0.7rem;
            color: var(--muted);
            line-height: 1.55;
        }

        @media (max-width: 760px) {
            [data-testid="stMainBlockContainer"] {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .navigator-hero {
                border-radius: 1.2rem;
            }
            .destination-summary-card,
            .metric-card,
            .confidence-card {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
