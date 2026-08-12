"""Reusable stakeholder-facing presentation components."""

from html import escape
from typing import List, Mapping, Optional

import altair as alt
import pandas as pd
import streamlit as st


HISTORICAL_MONTHS = pd.date_range("2025-08-01", "2026-07-01", freq="MS")


def _historical_month_axis(*, alternate_ticks: bool = False) -> alt.X:
    """Keep every historical chart on the same explicit Aug 2025–Jul 2026 axis."""
    displayed_months = HISTORICAL_MONTHS[::2] if alternate_ticks else HISTORICAL_MONTHS
    month_ticks = [month.to_pydatetime() for month in displayed_months]
    return alt.X(
        "month:T",
        title=None,
        axis=alt.Axis(
            format="%b %Y",
            labelAngle=-35,
            labelOverlap=False,
            values=month_ticks,
        ),
        scale=alt.Scale(
            domain=[pd.Timestamp("2025-07-20"), pd.Timestamp("2026-07-12")],
            nice=False,
        ),
    )


def render_hero(
    *,
    eyebrow: str,
    title: str,
    accent: str,
    copy: str,
) -> None:
    """Render the Navigator-inspired page introduction."""
    st.markdown(
        f"""
        <section class="navigator-hero">
            <div class="hero-eyebrow">{escape(eyebrow)}</div>
            <h1 class="hero-title">
                <span class="accent">{escape(accent)}</span> {escape(title)}
            </h1>
            <p class="hero-copy">{escape(copy)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_heading(kicker: str, title: str) -> None:
    """Render a compact section heading."""
    st.markdown(
        f"""
        <div class="section-kicker">{escape(kicker)}</div>
        <h2 class="section-title">{escape(title)}</h2>
        """,
        unsafe_allow_html=True,
    )


def render_anchor(anchor: str) -> None:
    """Add a stable in-page target for sidebar section navigation."""
    st.markdown(
        f'<span id="{escape(anchor)}" class="page-anchor"></span>',
        unsafe_allow_html=True,
    )


def render_placeholder_card(title: str, copy: str) -> None:
    """Render a branded placeholder card for the current shell stage."""
    st.markdown(
        f"""
        <article class="destination-card">
            <h3>{escape(title)}</h3>
            <p>{escape(copy)}</p>
            <span class="card-status">Data connection next</span>
        </article>
        """,
        unsafe_allow_html=True,
    )


def render_destination_summary_card(
    *,
    destination: str,
    month_label: str,
    season: str,
    tiktok_posts: str,
    average_views: str,
    review_activity: str,
    predicted_review_activity: str,
    anomaly_status: str,
    anomaly_tone: str,
) -> None:
    """Render a factual latest-month summary without model interpretation."""
    st.markdown(
        f"""
        <article class="destination-card destination-summary-card">
            <div class="card-month">{escape(month_label)}</div>
            <h3>{escape(destination)}</h3>
            <dl class="signal-list">
                <div>
                    <dt><span class="signal-tooltip" data-tooltip="The destination’s normal Low, Mid or High search season for this month.">Season</span></dt>
                    <dd>{escape(season)}</dd>
                </div>
                <div>
                    <dt><span class="signal-tooltip" data-tooltip="Scraped posts associated with locations mentioned in the TikTok data.">TikTok posts</span></dt>
                    <dd>{escape(tiktok_posts)}</dd>
                </div>
                <div>
                    <dt><span class="signal-tooltip" data-tooltip="Total views divided by the number of scraped posts associated with the identified locations.">Average views</span></dt>
                    <dd>{escape(average_views)}</dd>
                </div>
                <div>
                    <dt><span class="signal-tooltip" data-tooltip="Sampled Google Maps review count × average review rating, summed across locations with available observations.">Observed review activity</span></dt>
                    <dd>{escape(review_activity)}</dd>
                </div>
                <div>
                    <dt><span class="signal-tooltip" data-tooltip="XGBoost estimate based on TikTok visibility and the time of year, predicted for each sampled location and combined for the destination-month.">Predicted review activity</span></dt>
                    <dd>{escape(predicted_review_activity)}</dd>
                </div>
                <div>
                    <dt><span class="signal-tooltip" data-tooltip="Only potential anomalies—search activity substantially above or below seasonal expectations—are highlighted on this page.">Travel-search anomaly</span></dt>
                    <dd class="anomaly-value anomaly-{escape(anomaly_tone)}">{escape(anomaly_status)}</dd>
                </div>
            </dl>
        </article>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(
    label: str,
    value: str,
    detail: str,
    tone: Optional[str] = None,
    equal_height: bool = False,
    context_label: Optional[str] = None,
) -> None:
    """Render one concise evidence metric with its unit or limitation."""
    tone_class = f" metric-card-{escape(tone)}" if tone else ""
    height_class = " metric-card-equal-height" if equal_height else ""
    context_markup = (
        f'<div class="metric-context">{escape(context_label)}</div>'
        if context_label
        else ""
    )
    st.markdown(
        (
            f'<article class="metric-card{tone_class}{height_class}">'
            f'{context_markup}'
            f'<div class="metric-label">{escape(label)}</div>'
            f'<div class="metric-value">{escape(value)}</div>'
            f'<div class="metric-detail">{escape(detail)}</div>'
            "</article>"
        ),
        unsafe_allow_html=True,
    )


def render_history_chart(
    data: pd.DataFrame,
    *,
    series: Mapping[str, str],
    y_title: str,
    value_format: str = ",.0f",
    colors: Optional[List[str]] = None,
    stack_legend_labels: bool = False,
    alternate_month_ticks: bool = False,
) -> None:
    """Render comparable monthly series while preserving missing-value gaps."""
    chart_data = data[["month", *series.values()]].rename(columns={value: key for key, value in series.items()})
    chart_data = chart_data.melt(
        id_vars="month",
        value_vars=list(series),
        var_name="Series",
        value_name="Value",
    )
    palette = colors or ["#2447d8", "#08a99e", "#f7007f"]
    legend = (
        alt.Legend(
            title=None,
            orient="top",
            direction="vertical",
            columns=1,
            labelLimit=0,
        )
        if stack_legend_labels
        else alt.Legend(title=None)
    )
    chart = (
        alt.Chart(chart_data)
        .mark_line(
            point=alt.OverlayMarkDef(size=55),
            strokeWidth=3,
            invalid="break-paths-show-domains",
        )
        .encode(
            x=_historical_month_axis(alternate_ticks=alternate_month_ticks),
            y=alt.Y("Value:Q", title=y_title, scale=alt.Scale(zero=False)),
            color=alt.Color(
                "Series:N",
                legend=legend,
                scale=alt.Scale(domain=list(series), range=palette[: len(series)]),
            ),
            tooltip=[
                alt.Tooltip("month:T", title="Month", format="%B %Y"),
                alt.Tooltip("Series:N", title="Measure"),
                alt.Tooltip("Value:Q", title="Value", format=value_format),
            ],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)


def render_search_history_chart(data: pd.DataFrame) -> None:
    """Compare search indices and mark only stakeholder-relevant deviations."""
    line_data = data[
        ["month", "observed_seasonal_index", "expected_seasonal_index"]
    ].rename(
        columns={
            "observed_seasonal_index": "Observed seasonal index",
            "expected_seasonal_index": "Expected seasonal index",
        }
    )
    line_data = line_data.melt(
        id_vars="month",
        var_name="Series",
        value_name="Value",
    )
    lines = (
        alt.Chart(line_data)
        .mark_line(point=alt.OverlayMarkDef(size=55), strokeWidth=3)
        .encode(
            x=_historical_month_axis(),
            y=alt.Y("Value:Q", title="Travel-search seasonal index", scale=alt.Scale(zero=False)),
            color=alt.Color(
                "Series:N",
                legend=alt.Legend(title=None, orient="top"),
                scale=alt.Scale(
                    domain=["Observed seasonal index", "Expected seasonal index"],
                    range=["#08A99E", "#9AA4C1"],
                ),
            ),
            strokeDash=alt.StrokeDash(
                "Series:N",
                legend=None,
                scale=alt.Scale(
                    domain=["Observed seasonal index", "Expected seasonal index"],
                    range=[[1, 0], [6, 4]],
                ),
            ),
            tooltip=[
                alt.Tooltip("month:T", title="Month", format="%B %Y"),
                alt.Tooltip("Series:N", title="Measure"),
                alt.Tooltip("Value:Q", title="Index", format=".1f"),
            ],
        )
    )
    marker_data = data.loc[
        data["stakeholder_anomaly_status"].ne("Within expected range")
    ].copy()
    markers = (
        alt.Chart(marker_data)
        .mark_point(filled=True, shape="diamond", size=170)
        .encode(
            x=_historical_month_axis(),
            y=alt.Y("observed_seasonal_index:Q", title="Travel-search seasonal index"),
            color=alt.Color(
                "anomaly_marker_label:N",
                title=None,
                legend=alt.Legend(
                    orient="top",
                    direction="vertical",
                    columns=1,
                    labelLimit=0,
                ),
                scale=alt.Scale(
                    domain=[
                        "Potential positive anomaly",
                        "Potential negative anomaly",
                        "Worth monitoring",
                    ],
                    range=["#1256C4", "#D12E63", "#F59E42"],
                ),
            ),
            tooltip=[
                alt.Tooltip("month:T", title="Month", format="%B %Y"),
                alt.Tooltip("stakeholder_anomaly_status:N", title="Status"),
                alt.Tooltip("anomaly_direction:N", title="Direction"),
                alt.Tooltip("actual_vs_expected:Q", title="Gap", format="+.1f"),
                alt.Tooltip("standardised_difference:Q", title="Standardised difference", format="+.2f"),
                alt.Tooltip("confidence_note:N", title="Confidence"),
            ],
        )
    )
    chart = (lines + markers).resolve_scale(color="independent").properties(height=340)
    st.altair_chart(chart, use_container_width=True)


def render_note(text: str) -> None:
    """Render a visible evidence limitation note."""
    st.markdown(
        f'<div class="navigator-note">{escape(text)}</div>',
        unsafe_allow_html=True,
    )
