"""Destination Explorer page."""

from html import escape

import streamlit as st

from webapp.data import load_destination_monthly_data, stakeholder_anomaly_status
from webapp.ui import (
    render_anchor,
    render_hero,
    render_history_chart,
    render_metric_card,
    render_note,
    render_search_history_chart,
    render_section_heading,
)


def _select_calendar_month(month_number: int) -> None:
    """Store the stakeholder's calendar selection before the page rerenders."""
    st.session_state["seasonal_calendar_month"] = month_number
    st.session_state["guided_analysis_month"] = month_number


def _select_guided_month() -> None:
    """Keep the guided selector and seasonal calendar on one shared month."""
    st.session_state["seasonal_calendar_month"] = st.session_state[
        "guided_analysis_month"
    ]


def _select_guided_question(destination_key: str, question: str) -> None:
    """Store the selected stakeholder question before the page rerenders."""
    st.session_state[f"guided_question_{destination_key}"] = question


def _render_guided_answer_card(label: str, question: str, answer: str) -> None:
    """Render the selected answer directly below its question group."""
    st.markdown(
        f"""
        <article class="guided-answer">
            <div class="guided-answer-label">{escape(label)}</div>
            <h3>{escape(question)}</h3>
            <p>{escape(answer)}</p>
        </article>
        """,
        unsafe_allow_html=True,
    )


def _investigation_prompt(season: str, status: str, direction: str) -> str:
    """Return a cautious next question without recommending a campaign action."""
    if status == "Potential anomaly" and direction == "Above expected":
        return (
            "Which source markets, events or content themes might be contributing to "
            "the unusually strong search interest?"
        )
    if status == "Potential anomaly" and direction == "Below expected":
        return (
            "Could pricing, availability, events, competing destinations or data quality "
            "help explain the unusually weak search interest?"
        )
    if status == "Worth monitoring":
        return "Does this deviation persist, and do TikTok or review signals support it?"
    if season == "High":
        return "Do the other external signals show anything beyond normal high-season timing?"
    if season == "Low":
        return "Are there early-planning, event or niche-interest signals worth researching?"
    return "Do the other external signals support a meaningful change or normal timing?"


GUIDED_QUESTIONS = (
    "What is happening in this destination?",
    "Is the current search movement unusual or normal seasonality?",
    "Which months should I investigate?",
    "When is this destination normally strongest?",
    "Do the external signals agree or conflict?",
    "How reliable is this evidence?",
    "What can this evidence not tell me?",
    "What should I investigate next?",
)

MONTH_QUESTIONS = (
    GUIDED_QUESTIONS[0],
    GUIDED_QUESTIONS[1],
    GUIDED_QUESTIONS[4],
    GUIDED_QUESTIONS[7],
)
DESTINATION_QUESTIONS = (GUIDED_QUESTIONS[2], GUIDED_QUESTIONS[3])
EVIDENCE_QUESTIONS = (GUIDED_QUESTIONS[5], GUIDED_QUESTIONS[6])


def _prediction_level(history, row) -> str:
    """Describe the selected prediction relative to this displayed destination-year."""
    predictions = history["predicted_review_activity"].dropna()
    prediction = row["predicted_review_activity"]
    if predictions.empty or prediction != prediction:
        return "Unavailable"
    lower, upper = predictions.quantile([0.33, 0.67])
    if prediction <= lower:
        return "Low"
    if prediction >= upper:
        return "High"
    return "Typical"


def _guided_answer(question: str, destination: str, history, row) -> str:
    """Build a traceable plain-language answer from existing evidence only."""
    month = row["month"].strftime("%B %Y")
    season = str(row["season"])
    status, _, status_explanation = stakeholder_anomaly_status(row)
    direction = str(row["anomaly_direction"])
    prediction_level = _prediction_level(history, row)

    if question == GUIDED_QUESTIONS[0]:
        tiktok_context = (
            f"The collected sample contained {row['tiktok_post_count']:,.0f} TikTok posts "
            f"averaging {row['average_tiktok_views']:,.0f} views."
            if row["tiktok_post_count"] == row["tiktok_post_count"]
            and row["average_tiktok_views"] == row["average_tiktok_views"]
            else "TikTok evidence is unavailable for this month."
        )
        review_context = (
            f"Observed Google Maps review activity was {row['actual_review_activity']:,.0f}, "
            f"compared with an XGBoost estimate of {row['predicted_review_activity']:,.0f}."
            if row["actual_review_activity"] == row["actual_review_activity"]
            and row["predicted_review_activity"] == row["predicted_review_activity"]
            else "Google Maps review evidence is unavailable for this month."
        )
        return (
            f"In {month}, {destination} was in its normal {season} search season. "
            f"Travel search was classified as {status.lower()} and was "
            f"{direction.lower()} by {abs(float(row['actual_vs_expected'])):.1f} seasonal-index points. "
            f"{tiktok_context} {review_context} These are external activity signals, not evidence of bookings or campaign impact."
        )

    if question == GUIDED_QUESTIONS[1]:
        return (
            f"{month} is normally a {season} search month for {destination}. "
            f"{status_explanation} The seasonal classification describes the normal pattern; "
            "the anomaly status separately tests whether this month's search activity departed from it."
        )

    if question == GUIDED_QUESTIONS[2]:
        potential = history.loc[
            history["stakeholder_anomaly_status"].eq("Potential anomaly"), "month"
        ].dt.strftime("%B %Y").tolist()
        monitoring = history.loc[
            history["stakeholder_anomaly_status"].eq("Worth monitoring"), "month"
        ].dt.strftime("%B %Y").tolist()
        potential_text = ", ".join(potential) if potential else "none"
        monitoring_text = ", ".join(monitoring) if monitoring else "none"
        return (
            f"Potential anomalies: {potential_text}. Worth monitoring: {monitoring_text}. "
            "Treat these months as prompts to investigate markets, events, pricing, availability, "
            "content themes or data quality—not as instructions to change campaign spending."
        )

    if question == GUIDED_QUESTIONS[3]:
        strongest = history.loc[history["season"].eq("High"), "month_name"].drop_duplicates().tolist()
        return (
            f"{destination}'s High search-season months in the historical profile are "
            f"{', '.join(strongest)}. High means relatively stronger normal search interest; "
            "it does not mean that activity in those months is automatically unusual."
        )

    if question == GUIDED_QUESTIONS[4]:
        if prediction_level == "Unavailable":
            return (
                f"The search signal for {month} is {status.lower()}, but modelling records are "
                "unavailable for this month. Signal agreement therefore cannot be assessed."
            )
        search_is_positive = float(row["actual_vs_expected"]) > 0
        notable = status in {"Potential anomaly", "Worth monitoring"}
        aligned = (search_is_positive and prediction_level == "High") or (
            not search_is_positive and prediction_level == "Low"
        )
        opposed = (search_is_positive and prediction_level == "Low") or (
            not search_is_positive and prediction_level == "High"
        )
        if notable and aligned:
            interpretation = "The search and modelled review-activity signals broadly align."
        elif notable and opposed:
            interpretation = "The signals are mixed: search and modelled review activity point in different directions."
        elif status == "Within expected range" and prediction_level in {"High", "Low"}:
            interpretation = (
                "Search remained within its expected range, so the modelled review-activity level "
                "is not supported by an unusual wider-search signal."
            )
        else:
            interpretation = "The available signals are inconclusive rather than clearly aligned or conflicting."
        return (
            f"For {month}, search was {status.lower()} and the XGBoost prediction was {prediction_level.lower()} "
            f"relative to this destination's displayed months. {interpretation} This comparison does not establish causation."
        )

    if question == GUIDED_QUESTIONS[5]:
        return (
            "Reliability differs across the evidence layers. Travel-search confidence depends on the "
            "number and variability of complete baseline years. XGBoost estimates depend on the scraped "
            "location sample and observed input ranges, and are less reliable for extreme or out-of-range "
            "scenarios. Confidence in one evidence layer does not validate the others."
        )

    if question == GUIDED_QUESTIONS[6]:
        return (
            "The evidence cannot establish that TikTok caused searches or Google Maps review activity, "
            "and it does not measure total TikTok activity, total destination reviews, visitors, bookings, "
            "revenue or marketing effectiveness. It should support further investigation, not automatically "
            "increase or decrease campaign spending."
        )

    return (
        f"For {month}, the next useful question is: "
        f"{_investigation_prompt(season, status, direction)} "
        "Check the relevant source markets, events, content themes, pricing, availability and data quality "
        "before drawing a campaign conclusion."
    )


def render(selected_destination: str) -> None:
    """Render the selected destination's exploration shell."""
    render_hero(
        eyebrow="Destination Explorer",
        accent="What are the signals saying",
        title=f"about {selected_destination}?",
        copy=(
            "Explore normal seasonality, unusual travel-search behaviour, "
            f"TikTok visibility and Google Maps review activity for {selected_destination}."
        ),
    )
    destination_key = selected_destination.lower()
    history = load_destination_monthly_data().loc[
        lambda frame: frame["destination"].eq(destination_key)
    ].copy()
    latest = history.loc[history["month"].idxmax()]
    latest_search_status, latest_search_tone, _ = stakeholder_anomaly_status(latest)

    render_anchor("destination-latest-evidence")
    render_section_heading("Evidence view", "Latest external evidence")
    st.markdown(f"*Evidence shown for {latest['month'].strftime('%B %Y')}*")
    st.caption(
        "The TikTok sample contains scraped posts from which specific mentioned "
        "locations were identified. Google Maps reviews were then collected for "
        "those locations."
    )
    metric_columns = st.columns(6)
    metrics = (
        (
            "TikTok posts",
            f"{latest['tiktok_post_count']:,.0f}",
            "Posts in the collected sample",
            None,
        ),
        (
            "Average TikTok views",
            f"{latest['average_tiktok_views']:,.0f}",
            "Views per sampled post",
            None,
        ),
        (
            "Observed review activity",
            f"{latest['actual_review_activity']:,.0f}",
            "Sampled review count × average review rating · "
            f"summed across {latest['place_count']:,.0f} locations",
            None,
        ),
        (
            "Predicted review activity",
            f"{latest['predicted_review_activity']:,.0f}",
            "XGBoost destination-month estimate",
            None,
        ),
        (
            "Destination season",
            str(latest["season"]),
            f"Normal pattern for {latest['month_name']}",
            None,
        ),
        (
            "Search status",
            latest_search_status,
            f"{latest['anomaly_direction']} · {latest['actual_vs_expected']:+.1f} seasonal index points",
            latest_search_tone,
        ),
    )
    for column, (label, value, detail, tone) in zip(metric_columns, metrics):
        with column:
            render_metric_card(
                label,
                value,
                detail,
                tone=tone,
                equal_height=True,
            )

    render_note(
        "XGBoost predicts the constructed sampled score, not total reviews, visitors, "
        "bookings or marketing performance."
    )

    render_anchor("destination-seasonal-calendar")
    render_section_heading(
        "Seasonal calendar",
        f"What is {selected_destination}’s normal seasonal search pattern?",
    )
    st.caption(
        "Low, Mid and High describe the destination's normal historical travel-search "
        "pattern for each calendar month. Months are ordered by the August 2025–July "
        "2026 investigation period. The classifications are contextual evidence and "
        "are not XGBoost features. A seasonal index compares search interest with the "
        "destination's estimated annual level: 100 represents that level, values above "
        "100 indicate relatively stronger interest and values below 100 indicate "
        "relatively weaker interest. It is a relative measure, not the number of searches."
    )
    if "seasonal_calendar_month" not in st.session_state:
        st.session_state["seasonal_calendar_month"] = int(latest["month_number"])
    if "guided_analysis_month" not in st.session_state:
        st.session_state["guided_analysis_month"] = st.session_state[
            "seasonal_calendar_month"
        ]

    calendar_rows = history.sort_values("month")
    for start in (0, 6):
        month_columns = st.columns(6)
        for column, (_, calendar_row) in zip(
            month_columns,
            calendar_rows.iloc[start : start + 6].iterrows(),
        ):
            month_number = int(calendar_row["month_number"])
            month_label = calendar_row["month"].strftime("%b %y")
            season = str(calendar_row["season"])
            with column:
                st.button(
                    f"{month_label} · {season}",
                    key=f"calendar_month_{month_number}",
                    type=(
                        "primary"
                        if month_number == st.session_state["seasonal_calendar_month"]
                        else "secondary"
                    ),
                    use_container_width=True,
                    on_click=_select_calendar_month,
                    args=(month_number,),
                )

    st.caption("Low = normally quieter · Mid = moderate · High = normally stronger")
    selected_month = int(st.session_state["seasonal_calendar_month"])
    selected_row = history.loc[history["month_number"].eq(selected_month)].iloc[0]
    status, status_tone, status_explanation = stakeholder_anomaly_status(selected_row)
    selected_direction = str(selected_row["anomaly_direction"])

    calendar_metrics = st.columns(4)
    calendar_values = (
        ("Normal search season", str(selected_row["season"]), str(selected_row["month_name"])),
        (
            "Expected seasonal index",
            f"{selected_row['seasonal_index']:.1f}",
            "100 represents the destination's estimated annual level",
        ),
        (
            "Historical variability",
            f"{selected_row['seasonal_index_std']:.1f}",
            "Higher values indicate more variation between years",
        ),
        (
            "Complete baseline years",
            f"{selected_row['baseline_years']:.0f}",
            "Used for the normal seasonal profile",
        ),
    )
    for column, (label, value, detail) in zip(calendar_metrics, calendar_values):
        with column:
            render_metric_card(label, value, detail)

    investigation_month = selected_row["month"].strftime("%B %Y")
    st.markdown(
        f"""
        <article class="season-context season-context-{escape(status_tone)}">
            <div class="season-context-kicker">Observed search context · {escape(investigation_month)}</div>
            <h3>{escape(status)} · {escape(selected_direction)}</h3>
            <p>{escape(status_explanation)}</p>
            <div class="confidence-line"><strong>Confidence:</strong> {escape(str(selected_row['confidence_note']))}</div>
            <div class="next-question"><strong>Question to investigate:</strong> {escape(_investigation_prompt(str(selected_row['season']), status, selected_direction))}</div>
        </article>
        """,
        unsafe_allow_html=True,
    )

    render_anchor("destination-historical-evidence")
    render_section_heading("Historical evidence", "August 2025 to July 2026")
    tiktok_tab, review_tab, search_tab = st.tabs(
        ("TikTok visibility", "Google Maps review activity", "Travel search")
    )

    with tiktok_tab:
        st.caption(
            "TikTok visibility is based on scraped posts from which specific "
            "attractions, restaurants and other visitor locations were identified. "
            "Google Maps reviews were then collected for those mentioned locations. "
            "The sample does not represent all TikTok activity about the destination. "
            "TikTok posts and average views use separate charts because their units "
            "and scales are not directly comparable. Missing months are shown as "
            "gaps, not zero activity."
        )
        chart_columns = st.columns(2)
        with chart_columns[0]:
            st.markdown("#### Sampled TikTok posts")
            render_history_chart(
                history,
                series={"TikTok posts": "tiktok_post_count"},
                y_title="Post count",
                alternate_month_ticks=True,
            )
        with chart_columns[1]:
            st.markdown("#### Average views per sampled post")
            render_history_chart(
                history,
                series={"Average TikTok views": "average_tiktok_views"},
                y_title="Average views",
                colors=["#08a99e"],
                alternate_month_ticks=True,
            )
        missing_months = history.loc[
            history["tiktok_post_count"].isna(), "month"
        ].dt.strftime("%b %Y")
        if not missing_months.empty:
            st.caption("No modelling records: " + ", ".join(missing_months))

    with review_tab:
        # st.caption(
        #     "Google Maps reviews were collected for the locations identified from "
        #     "the TikTok data. Google Maps review activity is calculated as "
        #     "**sampled review count × average review rating**. A higher score reflects more "
        #     "sampled reviews, a higher average rating, or both. The destination-month "
        #     "value sums these scores across locations with available observations; "
        #     "it does not measure total destination reviews, visitors or bookings."
        # )
        st.caption(
            "**Google Maps review activity = "
            "sampled review count × average review rating**"
        )
        st.caption(
            "Google Maps reviews were collected for the locations identified from "
            "the TikTok data. "
            "A higher score reflects more "
            "sampled reviews, a higher average rating, or both. The destination-month "
            "value sums these scores across locations with available observations; "
            "it does not measure total destination reviews, visitors or bookings. "
            "XGBoost uses TikTok visibility and the time of year to estimate sampled "
            "Google Maps review activity. It predicts activity for each sampled "
            "location and combines the results for the destination and month."
        )
        
        # st.caption(
        #     "A higher score reflects more "
        #     "sampled reviews, a higher average rating, or both. The destination-month "
        #     "value sums these scores across locations with available observations; "
        #     "it does not measure total destination reviews, visitors or bookings."
        # )
        # st.caption(
        #     "XGBoost uses TikTok visibility and the time of year to estimate sampled "
        #     "Google Maps review activity. It predicts activity for each sampled "
        #     "location and combines the results for the destination and month."
        # )
        render_history_chart(
            history,
            series={
                "Observed Google Maps review activity": "actual_review_activity",
                "XGBoost-predicted Google Maps review activity": "predicted_review_activity",
            },
            y_title="Summed review-activity score",
            colors=["#2447d8", "#FF4D6D"],
            stack_legend_labels=True,
        )

    with search_tab:
        st.caption(
            "Both lines are seasonal indices, where 100 represents the destination's "
            "estimated annual search-interest level. Values show relative interest, "
            "not absolute search volume. Diamonds mark Potential anomalies "
            "and Worth monitoring months; normal movement is left unmarked."
        )
        render_search_history_chart(history)

        st.markdown("#### Months to investigate")
        highlighted_months = history.loc[
            history["stakeholder_anomaly_status"].ne("Within expected range")
        ].sort_values("month")
        for row_start in range(0, len(highlighted_months), 4):
            finding_row = highlighted_months.iloc[row_start : row_start + 4]
            columns_in_row = 4 if len(highlighted_months) > 4 else len(finding_row)
            finding_columns = st.columns(columns_in_row)
            for column, (_, highlighted_row) in zip(
                finding_columns, finding_row.iterrows()
            ):
                status, tone, explanation = stakeholder_anomaly_status(highlighted_row)
                with column:
                    st.markdown(
                        f"""
                        <article class="search-finding search-finding-{escape(tone)}">
                            <div class="search-finding-month">{escape(highlighted_row['month'].strftime('%B %Y'))}</div>
                            <h4>{escape(status)} · {escape(str(highlighted_row['anomaly_direction']))}</h4>
                            <p>{escape(explanation)}</p>
                            <div class="search-finding-values">Gap: {highlighted_row['actual_vs_expected']:+.1f} index points · Standardised difference: {highlighted_row['standardised_difference']:+.2f}</div>
                            <div class="search-finding-confidence"><strong>Confidence:</strong> {escape(str(highlighted_row['confidence_note']))}</div>
                        </article>
                        """,
                        unsafe_allow_html=True,
                    )

        normal_months = history.loc[
            history["stakeholder_anomaly_status"].eq("Within expected range")
        ].copy()
        with st.expander(f"See {len(normal_months)} months within the expected range"):
            normal_display = normal_months[
                ["month", "anomaly_direction", "actual_vs_expected", "standardised_difference"]
            ].copy()
            normal_display["month"] = normal_display["month"].dt.strftime("%B %Y")
            normal_display.columns = [
                "Month",
                "Direction",
                "Gap (index points)",
                "Standardised difference",
            ]
            st.dataframe(normal_display, hide_index=True, width="stretch")

    render_anchor("destination-guided-questions")
    render_section_heading("Guided questions", "What would you like to explore?")
    st.caption(
        "Questions are grouped by whether they interpret the selected month, the full "
        "destination pattern or the evidence itself."
    )
    guided_month_labels = {
        int(calendar_row["month_number"]): calendar_row["month"].strftime("%B %Y")
        for _, calendar_row in calendar_rows.iterrows()
    }
    question_state_key = f"guided_question_{destination_key}"
    if question_state_key not in st.session_state:
        st.session_state[question_state_key] = GUIDED_QUESTIONS[0]
    selected_question = st.session_state[question_state_key]
    guided_answer = _guided_answer(
        selected_question,
        selected_destination,
        history,
        selected_row,
    )
    with st.container(key=f"guided_questions_{destination_key}"):
        render_anchor("destination-selected-month")
        st.markdown(
            f"""
            <div class="guided-scope-heading">Selected month · {escape(investigation_month)}</div>
            <p class="guided-scope-copy">These questions use the month selected here or in the seasonal calendar above.</p>
            """,
            unsafe_allow_html=True,
        )
        st.selectbox(
            "Month to analyse",
            options=list(guided_month_labels),
            format_func=guided_month_labels.get,
            key="guided_analysis_month",
            on_change=_select_guided_month,
        )
        month_columns = st.columns(4)
        for column, question in zip(month_columns, MONTH_QUESTIONS):
            with column:
                st.button(
                    question,
                    key=f"guided_{destination_key}_month_{question}",
                    type="primary" if question == selected_question else "secondary",
                    use_container_width=True,
                    on_click=_select_guided_question,
                    args=(destination_key, question),
                )
        if selected_question in MONTH_QUESTIONS:
            _render_guided_answer_card(
                f"Selected month · {investigation_month}",
                selected_question,
                guided_answer,
            )

        render_anchor("destination-pattern")
        st.markdown(
            """
            <div class="guided-scope-heading guided-scope-spacing">Destination pattern · August 2025–July 2026</div>
            <p class="guided-scope-copy">These questions summarise the full investigation period for the destination.</p>
            """,
            unsafe_allow_html=True,
        )
        destination_columns = st.columns(4)
        for column, question in zip(destination_columns, DESTINATION_QUESTIONS):
            with column:
                st.button(
                    question,
                    key=f"guided_{destination_key}_destination_{question}",
                    type="primary" if question == selected_question else "secondary",
                    use_container_width=True,
                    on_click=_select_guided_question,
                    args=(destination_key, question),
                )
        if selected_question in DESTINATION_QUESTIONS:
            _render_guided_answer_card(
                f"Destination pattern · {selected_destination} · August 2025–July 2026",
                selected_question,
                guided_answer,
            )

        render_anchor("destination-understanding-evidence")
        st.markdown(
            """
            <div class="guided-scope-heading guided-scope-spacing">Understanding the evidence</div>
            <p class="guided-scope-copy">These questions explain reliability and limitations across the evidence layers.</p>
            """,
            unsafe_allow_html=True,
        )
        evidence_columns = st.columns(4)
        for column, question in zip(evidence_columns, EVIDENCE_QUESTIONS):
            with column:
                st.button(
                    question,
                    key=f"guided_{destination_key}_evidence_{question}",
                    type="primary" if question == selected_question else "secondary",
                    use_container_width=True,
                    on_click=_select_guided_question,
                    args=(destination_key, question),
                )
        if selected_question in EVIDENCE_QUESTIONS:
            _render_guided_answer_card(
                "Understanding the evidence",
                selected_question,
                guided_answer,
            )
