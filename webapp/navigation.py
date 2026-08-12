"""Shared navigation and destination selection for the Streamlit app."""

from collections.abc import Callable
import json

import streamlit as st
from streamlit.components.v1 import html as render_html_component

from webapp.pages.destination_explorer import render as render_destination_explorer
from webapp.pages.methodology import render as render_methodology
from webapp.pages.model_explorer import render as render_model_explorer
from webapp.pages.overview import render as render_overview


DESTINATIONS = ("Marrakech", "Hanoi", "Lisbon", "Reykjavik")

PAGES: dict[str, Callable[[str], None]] = {
    "Overview": render_overview,
    "Destination Explorer": render_destination_explorer,
    "Model Explorer": render_model_explorer,
    "Method & Limitations": render_methodology,
}


def _open_page(page: str, node: str) -> None:
    """Open a page and reveal its section navigation."""
    st.session_state["selected_page"] = page
    st.session_state[f"sidebar_open_{node}"] = True
    st.session_state.pop("scroll_page_to_anchor", None)
    st.session_state["scroll_page_to_top"] = True
    st.session_state["scroll_request_id"] = st.session_state.get("scroll_request_id", 0) + 1


def _open_page_anchor(page: str, node: str, anchor: str, child_node: str = "") -> None:
    """Open a page, reveal the relevant navigation, and scroll to an anchor."""
    st.session_state["selected_page"] = page
    st.session_state[f"sidebar_open_{node}"] = True
    if child_node:
        st.session_state[f"sidebar_open_{child_node}"] = True
    st.session_state.pop("scroll_page_to_top", None)
    st.session_state["scroll_page_to_anchor"] = anchor
    st.session_state["scroll_request_id"] = st.session_state.get("scroll_request_id", 0) + 1


def _open_methodology_tab(tab: str, node: str, anchor: str) -> None:
    """Open the Methods tab and scroll to its selected section."""
    st.session_state["selected_page"] = "Method & Limitations"
    st.session_state["methodology_tab"] = tab
    st.session_state["sidebar_open_methods"] = True
    st.session_state[f"sidebar_open_{node}"] = True
    st.session_state.pop("scroll_page_to_top", None)
    st.session_state["scroll_page_to_anchor"] = anchor
    st.session_state["scroll_request_id"] = st.session_state.get("scroll_request_id", 0) + 1


def _open_methodology_anchor(anchor: str) -> None:
    """Open the Methods page and scroll to content outside the evidence tabs."""
    st.session_state["selected_page"] = "Method & Limitations"
    st.session_state["sidebar_open_methods"] = True
    st.session_state.pop("scroll_page_to_top", None)
    st.session_state["scroll_page_to_anchor"] = anchor
    st.session_state["scroll_request_id"] = st.session_state.get("scroll_request_id", 0) + 1


def _toggle_sidebar_node(node: str) -> None:
    """Expand or collapse a navigation node without changing the active page."""
    key = f"sidebar_open_{node}"
    st.session_state[key] = not st.session_state.get(key, False)


def _node_is_open(node: str, *, default: bool = False) -> bool:
    """Return the persisted expansion state for one navigation node."""
    key = f"sidebar_open_{node}"
    if key not in st.session_state:
        st.session_state[key] = default
    return bool(st.session_state[key])


def _sidebar_link(
    label: str,
    anchor: str,
    page: str,
    page_node: str,
    *,
    level: int = 1,
    child_node: str = "",
) -> None:
    """Render a section button that works both within and across pages."""
    st.sidebar.button(
        label,
        key=f"nav_{'subsection' if level == 2 else 'section'}_{anchor}",
        use_container_width=True,
        on_click=_open_page_anchor,
        args=(page, page_node, anchor, child_node),
    )


def _render_page_row(page: str, node: str, selected_page: str) -> bool:
    """Render a page label and an independent expansion chevron."""
    is_open = _node_is_open(node, default=selected_page == page)
    label_column, arrow_column = st.sidebar.columns([0.84, 0.16], gap="small")
    with label_column:
        st.button(
            page,
            key=f"nav_page_{node}",
            use_container_width=True,
            on_click=_open_page,
            args=(page, node),
        )
    with arrow_column:
        st.button(
            "⌄" if is_open else "›",
            key=f"nav_toggle_{node}",
            help=f"{'Collapse' if is_open else 'Expand'} {page} sections",
            use_container_width=True,
            on_click=_toggle_sidebar_node,
            args=(node,),
        )
    return is_open


def _render_expandable_link_row(
    label: str,
    anchor: str,
    node: str,
    page: str,
    page_node: str,
    *,
    level: int = 1,
) -> bool:
    """Render a section link with a separate subsection chevron."""
    is_open = _node_is_open(node)
    label_column, arrow_column = st.sidebar.columns([0.84, 0.16], gap="small")
    with label_column:
        st.button(
            label,
            key=f"nav_section_{anchor}",
            use_container_width=True,
            on_click=_open_page_anchor,
            args=(page, page_node, anchor, node),
        )
    with arrow_column:
        st.button(
            "⌄" if is_open else "›",
            key=f"nav_toggle_{node}",
            help=f"{'Collapse' if is_open else 'Expand'} {label} subsections",
            use_container_width=True,
            on_click=_toggle_sidebar_node,
            args=(node,),
        )
    return is_open


def _render_method_row(label: str, node: str, anchor: str) -> bool:
    """Render a Methods tab label with an independent subsection chevron."""
    is_open = _node_is_open(node)
    label_column, arrow_column = st.sidebar.columns([0.84, 0.16], gap="small")
    with label_column:
        st.button(
            label,
            key=f"nav_method_{node}",
            use_container_width=True,
            on_click=_open_methodology_tab,
            args=(label, node, anchor),
        )
    with arrow_column:
        st.button(
            "⌄" if is_open else "›",
            key=f"nav_toggle_{node}",
            help=f"{'Collapse' if is_open else 'Expand'} {label} subsections",
            use_container_width=True,
            on_click=_toggle_sidebar_node,
            args=(node,),
        )
    return is_open


def _render_method_child_links(
    tab: str,
    node: str,
    items: tuple[tuple[str, str], ...],
) -> None:
    """Render subsection buttons that also select their containing Methods tab."""
    for label, anchor in items:
        st.sidebar.button(
            label,
            key=f"nav_method_child_{anchor}",
            use_container_width=True,
            on_click=_open_methodology_tab,
            args=(tab, node, anchor),
        )


def _render_method_anchor_button(label: str, anchor: str) -> None:
    """Render a Methods section button outside the evidence tabs."""
    st.sidebar.button(
        label,
        key=f"nav_method_anchor_{anchor}",
        use_container_width=True,
        on_click=_open_methodology_anchor,
        args=(anchor,),
    )


def _render_child_links(
    items: tuple[tuple[str, str], ...],
    page: str,
    page_node: str,
    *,
    level: int = 2,
    child_node: str = "",
) -> None:
    """Render the children of an expanded section."""
    for label, anchor in items:
        _sidebar_link(
            label, anchor, page, page_node, level=level, child_node=child_node
        )


def _render_expandable_navigation(selected_page: str) -> None:
    """Render Codex-style page rows with independently controlled chevrons."""
    st.sidebar.markdown(
        '<div class="sidebar-explore-label">Explore</div>',
        unsafe_allow_html=True,
    )

    if _render_page_row("Overview", "overview", selected_page):
        _sidebar_link(
            "Latest external evidence", "overview-latest-evidence", "Overview", "overview"
        )

    if _render_page_row("Destination Explorer", "destination", selected_page):
        _sidebar_link("Latest external evidence", "destination-latest-evidence", "Destination Explorer", "destination")
        _sidebar_link("Seasonal calendar", "destination-seasonal-calendar", "Destination Explorer", "destination")
        _sidebar_link("Historical evidence", "destination-historical-evidence", "Destination Explorer", "destination")
        if _render_expandable_link_row(
            "Guided questions", "destination-guided-questions", "destination_guided",
            "Destination Explorer", "destination"
        ):
            _render_child_links(
                (
                    ("Selected month", "destination-selected-month"),
                    ("Destination pattern", "destination-pattern"),
                    ("Understanding the evidence", "destination-understanding-evidence"),
                ),
                "Destination Explorer",
                "destination",
                child_node="destination_guided",
            )

    if _render_page_row("Model Explorer", "model", selected_page):
        _render_child_links(
            (
                ("Hypothetical scenario", "model-hypothetical-scenario"),
                ("XGBoost estimate", "model-xgboost-estimate"),
                ("Confidence", "model-confidence"),
                ("Model features", "model-features"),
            ),
            "Model Explorer",
            "model",
            level=1,
        )

    if _render_page_row("Method & Limitations", "methods", selected_page):
        _render_method_anchor_button("Evidence framework", "methods-evidence-framework")
        method_groups = (
            (
                "XGBoost & linked sample",
                "methods_xgboost",
                (
                    ("Purpose", "methods-xgboost-purpose"),
                    ("Linked sample", "methods-xgboost-how-the-linked-sample-was-created"),
                    ("Scraped-data coverage", "methods-xgboost-scraped-data-coverage"),
                    ("Measures", "methods-xgboost-measures-shown-in-the-app"),
                    ("Inputs", "methods-xgboost-xgboost-inputs"),
                    ("Model development", "methods-xgboost-model-development-design"),
                    ("Performance", "methods-xgboost-recorded-performance"),
                    ("Finding", "methods-xgboost-supported-finding"),
                    ("Presentation", "methods-xgboost-how-predictions-should-be-presented"),
                    ("Limitations", "methods-xgboost-xgboost-and-linked-sample-limitations"),
                ),
            ),
            (
                "Search seasonality",
                "methods_seasonality",
                (
                    ("Purpose", "methods-seasonality-purpose"),
                    ("Search data", "methods-seasonality-search-data"),
                    ("Seasonal-index calculation", "methods-seasonality-seasonal-index-calculation"),
                    ("Low/Mid/High classification", "methods-seasonality-low-mid-high-classification"),
                    ("Destination findings", "methods-seasonality-destination-seasonal-findings"),
                    ("Presentation", "methods-seasonality-how-seasonality-should-be-presented"),
                    ("Confidence and limitations", "methods-seasonality-seasonality-confidence-and-limitations"),
                ),
            ),
            (
                "Search anomalies",
                "methods_anomalies",
                (
                    ("Purpose", "methods-anomalies-purpose"),
                    ("Investigation period", "methods-anomalies-investigation-period-and-data-contract"),
                    ("Baseline method", "methods-anomalies-baseline-method"),
                    ("Calculations", "methods-anomalies-anomaly-calculations"),
                    ("Labels and thresholds", "methods-anomalies-stakeholder-labels-and-thresholds"),
                    ("Validated findings", "methods-anomalies-validated-destination-anomaly-findings"),
                    ("Marketing value", "methods-anomalies-marketing-investigation-value"),
                    ("Signal agreement", "methods-anomalies-signal-agreement-interpretation"),
                    ("Confidence and limitations", "methods-anomalies-anomaly-confidence-and-limitations"),
                ),
            ),
        )
        for label, node, subsections in method_groups:
            tab_anchor = {
                "XGBoost & linked sample": "methods-xgboost",
                "Search seasonality": "methods-seasonality",
                "Search anomalies": "methods-anomalies",
            }[label]
            if _render_method_row(label, node, tab_anchor):
                _render_method_child_links(label, node, subsections)

        _render_method_anchor_button("Overall app conclusion", "methods-overall-conclusion")
        _render_method_anchor_button("About this prototype", "methods-about-prototype")


def render_navigation() -> None:
    """Render the shared sidebar and the currently selected page."""
    st.sidebar.markdown(
        """
        <div class="app-sidebar-title">External Travel Signals Explorer</div>
        <div class="app-sidebar-subtitle">Destination intelligence prototype</div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("selected_page") not in PAGES:
        st.session_state["selected_page"] = "Overview"
    selected_page = st.session_state["selected_page"]
    _render_expandable_navigation(selected_page)

    st.sidebar.divider()
    selected_destination = st.sidebar.selectbox(
        "Case-study destination",
        options=DESTINATIONS,
        key="selected_destination",
        help=(
            "This prototype supports only the four destinations included in "
            "the underlying research."
        ),
    )

    st.sidebar.caption(
        "The destination provides context for the app. It is not an input "
        "feature in the XGBoost model."
    )

    st.sidebar.divider()
    st.sidebar.markdown(
        """
        <div class="sidebar-attribution">
            Developed by Anna Claire Breuss-Burgess<br>
            <span>Navigator internship project · 2026</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    PAGES[selected_page](selected_destination)

    scroll_request_id = st.session_state.get("scroll_request_id", 0)
    target_anchor = st.session_state.pop("scroll_page_to_anchor", None)
    if target_anchor:
        st.session_state.pop("scroll_page_to_top", None)
        encoded_anchor = json.dumps(target_anchor)
        render_html_component(
            f"""
            <script>
                // Navigation request {scroll_request_id}
                const target = window.parent.document.getElementById({encoded_anchor});
                if (target) {{
                    target.scrollIntoView({{ block: 'start', behavior: 'instant' }});
                }}
            </script>
            """,
            height=0,
            scrolling=False,
        )
    elif st.session_state.pop("scroll_page_to_top", False):
        render_html_component(
            f"""
            <script>
                // Navigation request {scroll_request_id}
                const app = window.parent.document.querySelector(
                    '[data-testid="stMain"]'
                );
                if (app) {{
                    app.scrollTo({{ top: 0, left: 0, behavior: 'instant' }});
                }} else {{
                    window.parent.scrollTo({{ top: 0, left: 0, behavior: 'instant' }});
                }}
            </script>
            """,
            height=0,
            scrolling=False,
        )
