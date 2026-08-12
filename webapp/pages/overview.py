"""Overview page."""

import streamlit as st

from webapp.data import load_destination_monthly_data, overview_anomaly_status
from webapp.ui import (
    render_anchor,
    render_destination_summary_card,
    render_hero,
    render_note,
    render_section_heading,
)


def render(selected_destination: str) -> None:
    """Render the four-destination overview shell."""
    del selected_destination  # Overview will compare all destinations.

    render_hero(
        eyebrow="Overview",
        accent="What are the external travel signals",
        title="telling us?",
        copy=(
            "Compare TikTok visibility, observed and predicted Google Maps review activity, and "
            "travel-search behaviour across Marrakech, Hanoi, Lisbon and "
            "Reykjavik. See whether signals align, conflict or reflect normal "
            "seasonality."
        ),
    )

    monthly = load_destination_monthly_data()
    latest_month = monthly["month"].max()
    latest = monthly.loc[monthly["month"].eq(latest_month)].set_index("destination")

    render_anchor("overview-latest-evidence")
    render_section_heading("Four case studies", "Latest external evidence")
    st.caption(
        "The TikTok sample contains scraped posts from which specific mentioned "
        "locations were identified. Google Maps reviews were then collected for "
        "those locations."
    )
    columns = st.columns(4)
    for column, destination in zip(
        columns,
        ("Marrakech", "Hanoi", "Lisbon", "Reykjavik"),
    ):
        with column:
            row = latest.loc[destination.lower()]
            anomaly_status, anomaly_tone = overview_anomaly_status(row)
            render_destination_summary_card(
                destination=destination,
                month_label=latest_month.strftime("%B %Y"),
                season=str(row["season"]),
                tiktok_posts=f"{row['tiktok_post_count']:,.0f}",
                average_views=f"{row['average_tiktok_views']:,.0f}",
                review_activity=f"{row['actual_review_activity']:,.0f}",
                predicted_review_activity=f"{row['predicted_review_activity']:,.0f}",
                anomaly_status=anomaly_status,
                anomaly_tone=anomaly_tone,
            )

    render_note(
        "These signals indicate online attention and engagement. They do not "
        "measure bookings, revenue, or marketing effectiveness. Potential anomalies "
        "are prompts for investigation, not recommendations to change campaign spending."
    )
