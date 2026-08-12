"""XGBoost Model Explorer page."""

import calendar
from html import escape

import streamlit as st

from webapp.data import (
    build_xgboost_features,
    load_destination_monthly_data,
    load_model_input_ranges,
    predict_hypothetical_location,
    stakeholder_anomaly_status,
)
from webapp.ui import render_anchor, render_hero, render_metric_card, render_section_heading


def render(selected_destination: str) -> None:
    """Render the controlled one-location XGBoost scenario playground."""
    render_hero(
        eyebrow="XGBoost Model Explorer",
        accent="Explore expected activity",
        title=f"with {selected_destination} context",
        copy=(
            "Test how TikTok visibility and the time of year relate to sampled "
            "Google Maps review activity, then interpret the estimate alongside "
            "separate destination seasonality and travel-search evidence."
        ),
    )

    render_anchor("model-hypothetical-scenario")
    render_section_heading("Hypothetical scenario", "Set the TikTok visibility and month")
    st.caption(
        "The playground represents one hypothetical sampled location-month. The "
        "destination selector supplies context only and is not passed into XGBoost."
    )
    input_columns = st.columns(3)
    with input_columns[0]:
        selected_month = st.selectbox(
            "Month",
            options=tuple(range(1, 13)),
            index=6,
            format_func=lambda month: calendar.month_name[month],
            key="model_scenario_month",
        )
    with input_columns[1]:
        tiktok_post_count = st.number_input(
            "TikTok post count",
            min_value=0,
            value=3,
            step=1,
            key="model_tiktok_post_count",
            help="Number of scraped TikTok posts associated with the hypothetical location.",
        )
    with input_columns[2]:
        average_tiktok_views = st.number_input(
            "Average TikTok views",
            min_value=0.0,
            value=16_300.0,
            step=1_000.0,
            key="model_average_tiktok_views",
            help="Total views divided by the sampled posts for the hypothetical location.",
        )

    input_ranges = load_model_input_ranges()
    outside_ranges = []
    post_min, post_max = input_ranges["tiktok_post_count"]
    view_min, view_max = input_ranges["average_tiktok_views"]
    if not post_min <= tiktok_post_count <= post_max:
        outside_ranges.append(f"TikTok posts ({post_min:,.0f}–{post_max:,.0f})")
    if not view_min <= average_tiktok_views <= view_max:
        outside_ranges.append(f"average views ({view_min:,.0f}–{view_max:,.0f})")
    if outside_ranges:
        xgboost_range_status = "Outside the observed range"
        st.warning(
            "This scenario is outside the model's observed range for: "
            + ", ".join(outside_ranges)
            + ". Interpret the estimate with additional caution. Tree-based XGBoost "
            "does not extrapolate smoothly beyond its learned splits, so increasingly "
            "extreme inputs may produce the same estimate rather than a reliable forecast."
        )
    else:
        xgboost_range_status = "Within the observed range"
        st.caption(
            f"Both TikTok inputs are within the observed modelling ranges: "
            f"{post_min:,.0f}–{post_max:,.0f} posts and "
            f"{view_min:,.0f}–{view_max:,.0f} average views."
        )

    prediction = predict_hypothetical_location(
        float(tiktok_post_count),
        float(average_tiktok_views),
        int(selected_month),
    )
    context = load_destination_monthly_data().loc[
        lambda frame: frame["destination"].eq(selected_destination.lower())
        & frame["month_number"].eq(int(selected_month))
    ].iloc[0]
    anomaly_status, anomaly_tone, anomaly_explanation = stakeholder_anomaly_status(context)

    render_anchor("model-xgboost-estimate")
    render_section_heading("XGBoost estimate", "One hypothetical sampled location-month")
    st.caption(
        "XGBoost uses TikTok visibility and the time of year to estimate sampled "
        "Google Maps review activity. It predicts activity for one sampled location "
        "in this playground; historical destination totals combine location-level results."
    )
    result_columns = st.columns(4)
    results = (
        (
            "Predicted review activity",
            f"{prediction:,.0f}",
            "One hypothetical sampled location-month",
        ),
        ("Scenario month", calendar.month_name[int(selected_month)], "Passed as annual timing"),
        (
            f"{selected_destination} season",
            str(context["season"]),
            "Destination-specific context; not a model feature",
        ),
        (
            "Historical search status",
            anomaly_status,
            context["month"].strftime("%B %Y"),
        ),
    )
    for column, (label, value, detail) in zip(result_columns, results):
        with column:
            render_metric_card(label, value, detail)

    st.markdown(
        f"""
        <article class="season-context season-context-{escape(anomaly_tone)}">
            <div class="season-context-kicker">Separate destination context · {escape(context['month'].strftime('%B %Y'))}</div>
            <h3>{escape(anomaly_status)} · {escape(str(context['anomaly_direction']))}</h3>
            <p>{escape(anomaly_explanation)}</p>
            <div class="confidence-line"><strong>Confidence:</strong> {escape(str(context['confidence_note']))}</div>
        </article>
        """,
        unsafe_allow_html=True,
    )

    render_anchor("model-confidence")
    render_section_heading("Confidence", "How certain should I be?")
    confidence_columns = st.columns(2)
    with confidence_columns[0]:
        st.markdown(
            f"""
            <article class="confidence-card confidence-card-model">
                <div class="confidence-card-kicker">XGBoost estimate</div>
                <h3>{escape(xgboost_range_status)}</h3>
                <p>Reliability depends on whether the TikTok inputs resemble the modelling data, the small and uneven location sample, and missing or sparse observations.</p>
                <p>Historical error also varied: mean validation MAE was 73.05, while July test MAE was 251.60. No confidence interval is available for this individual estimate.</p>
            </article>
            """,
            unsafe_allow_html=True,
        )
    with confidence_columns[1]:
        st.markdown(
            f"""
            <article class="confidence-card confidence-card-search">
                <div class="confidence-card-kicker">Travel-search context</div>
                <h3>Separate destination-month evidence</h3>
                <p>{escape(str(context['confidence_note']))}</p>
                <p>This confidence depends on the number and variability of complete baseline years. Greater historical variability makes the seasonal expectation less precise.</p>
            </article>
            """,
            unsafe_allow_html=True,
        )

    st.caption(
        "These confidence explanations are not combined into one score: confidence in "
        "the travel-search baseline does not validate the XGBoost estimate, and an "
        "in-range XGBoost scenario does not validate the search evidence."
    )

    st.divider()
    render_anchor("model-features")
    render_section_heading("Model features", "What does XGBoost use?")
    with st.expander("See the four features passed to XGBoost"):
        features = build_xgboost_features(
            float(tiktok_post_count),
            float(average_tiktok_views),
            int(selected_month),
        )
        st.dataframe(features, hide_index=True, width="stretch")
        st.caption(
            "Destination, Low/Mid/High seasonality and travel-search anomaly evidence "
            "are not included in this feature frame."
        )
