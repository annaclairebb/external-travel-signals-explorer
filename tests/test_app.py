"""Streamlit rendering smoke tests for the evidence pages."""

import unittest

from streamlit.testing.v1 import AppTest

from webapp.data import load_destination_monthly_data
from webapp.pages.destination_explorer import GUIDED_QUESTIONS, _guided_answer


class AppRenderingTests(unittest.TestCase):
    @staticmethod
    def _open_page(app: AppTest, label: str) -> AppTest:
        button = next(
            control
            for control in app.button
            if control.label == label and str(control.key).startswith("nav_page_")
        )
        button.click().run()
        return app

    def test_guided_answers_cover_every_destination_month_and_question(self) -> None:
        monthly = load_destination_monthly_data()
        for destination_key, history in monthly.groupby("destination"):
            destination = str(destination_key).title()
            for _, row in history.iterrows():
                for question in GUIDED_QUESTIONS:
                    answer = _guided_answer(question, destination, history, row)
                    self.assertTrue(answer.strip(), (destination, row["month"], question))
                    self.assertNotIn("should increase", answer.lower())
                    self.assertNotIn("should decrease", answer.lower())

    def test_sidebar_page_and_cross_page_section_navigation(self) -> None:
        app = AppTest.from_file("app.py", default_timeout=30).run()

        initial_request = 0
        self._open_page(app, "Overview")
        self.assertEqual(app.session_state["selected_page"], "Overview")
        self.assertGreater(app.session_state["scroll_request_id"], initial_request)

        next(
            control for control in app.button if control.key == "nav_toggle_destination"
        ).click().run()
        next(
            control
            for control in app.button
            if control.key == "nav_section_destination-seasonal-calendar"
        ).click().run()
        self.assertEqual(app.session_state["selected_page"], "Destination Explorer")
        destination_markdown = " ".join(element.value for element in app.markdown)
        self.assertIn("destination-seasonal-calendar", destination_markdown)

        next(
            control for control in app.button if control.key == "nav_toggle_model"
        ).click().run()
        next(
            control
            for control in app.button
            if control.key == "nav_section_model-confidence"
        ).click().run()
        self.assertEqual(app.session_state["selected_page"], "Model Explorer")
        model_markdown = " ".join(element.value for element in app.markdown)
        self.assertIn("model-confidence", model_markdown)

    def test_overview_and_all_destination_explorers_render(self) -> None:
        app = AppTest.from_file("app.py", default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        overview_markdown = " ".join(element.value for element in app.markdown)
        self.assertIn("Developed by Anna Claire Breuss-Burgess", overview_markdown)
        self.assertIn("Navigator internship project · 2026", overview_markdown)
        self.assertNotIn("Latest available month", overview_markdown)
        self.assertNotIn("Evidence shown for July 2026", overview_markdown)
        self.assertEqual(overview_markdown.count("July 2026"), 4)

        destination_arrow = next(
            control for control in app.button if control.key == "nav_toggle_destination"
        )
        destination_arrow.click().run()
        self.assertEqual(app.session_state["selected_page"], "Overview")
        self.assertTrue(
            any(
                control.key == "nav_section_destination-seasonal-calendar"
                for control in app.button
            )
        )

        self._open_page(app, "Destination Explorer")
        for destination in ("Marrakech", "Hanoi", "Lisbon", "Reykjavik"):
            destination_control = next(
                control
                for control in app.selectbox
                if control.label == "Case-study destination"
            )
            destination_control.set_value(destination).run()
            self.assertFalse(app.exception, destination)
            self.assertFalse(app.error, destination)
            self.assertEqual(len(app.tabs), 3)
            self.assertGreaterEqual(len(app.button), 20)
            destination_markdown = " ".join(element.value for element in app.markdown)
            self.assertNotIn("Latest available month", destination_markdown)
            self.assertEqual(destination_markdown.count("Evidence shown for July 2026"), 1)
            self.assertIn("Latest external evidence", destination_markdown)
            self.assertNotIn("Latest external evidence for July 2026", destination_markdown)
            expected_highlights = int(
                load_destination_monthly_data()
                .loc[lambda frame: frame["destination"].eq(destination.lower())]
                ["stakeholder_anomaly_status"]
                .ne("Within expected range")
                .sum()
            )
            self.assertEqual(
                destination_markdown.count('<article class="search-finding '),
                expected_highlights,
                destination,
            )

        guided_month_control = next(
            control for control in app.selectbox if control.label == "Month to analyse"
        )
        guided_month_control.set_value(8).run()
        self.assertEqual(app.session_state["guided_analysis_month"], 8)
        self.assertEqual(app.session_state["seasonal_calendar_month"], 8)

    def test_model_playground_and_destination_context_render(self) -> None:
        app = AppTest.from_file("app.py", default_timeout=30).run()
        self._open_page(app, "Model Explorer")

        destination_control = next(
            control for control in app.selectbox if control.label == "Case-study destination"
        )
        month_control = next(control for control in app.selectbox if control.label == "Month")
        for destination in ("Marrakech", "Hanoi", "Lisbon", "Reykjavik"):
            destination_control.set_value(destination).run()
            self.assertFalse(app.exception, destination)
            self.assertFalse(app.error, destination)

        month_control = next(control for control in app.selectbox if control.label == "Month")
        month_control.set_value(12).run()
        post_control = next(
            control for control in app.number_input if control.label == "TikTok post count"
        )
        view_control = next(
            control for control in app.number_input if control.label == "Average TikTok views"
        )
        post_control.set_value(0).run()
        view_control = next(
            control for control in app.number_input if control.label == "Average TikTok views"
        )
        view_control.set_value(0.0).run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertEqual(len(app.warning), 1)
        self.assertEqual(
            sum(
                expander.label == "See the four features passed to XGBoost"
                for expander in app.expander
            ),
            1,
        )
        rendered_markdown = " ".join(element.value for element in app.markdown)
        self.assertIn("Outside the observed range", rendered_markdown)
        self.assertIn("XGBoost estimate", rendered_markdown)
        self.assertIn("Travel-search context", rendered_markdown)
        self.assertIn("No confidence interval is available", rendered_markdown)
        self.assertNotIn("The XGBoost result reflects the hypothetical TikTok scenario", rendered_markdown)

        post_control = next(
            control for control in app.number_input if control.label == "TikTok post count"
        )
        view_control = next(
            control for control in app.number_input if control.label == "Average TikTok views"
        )
        post_control.set_value(3).run()
        view_control = next(
            control for control in app.number_input if control.label == "Average TikTok views"
        )
        view_control.set_value(16_300.0).run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertEqual(len(app.warning), 0)
        self.assertEqual(len(app.code), 0)
        rendered_markdown = " ".join(element.value for element in app.markdown)
        self.assertIn("Within the observed range", rendered_markdown)
        self.assertIn("Model features", rendered_markdown)
        self.assertIn("What does XGBoost use?", rendered_markdown)

    def test_methodology_page_renders_approved_markdown_sections(self) -> None:
        app = AppTest.from_file("app.py", default_timeout=30).run()
        self._open_page(app, "Method & Limitations")

        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertEqual(len(app.tabs), 0)
        self.assertEqual(len(app.radio), 1)
        self.assertEqual(
            tuple(app.radio[0].options),
            ("XGBoost & linked sample", "Search seasonality", "Search anomalies"),
        )
        rendered_markdown = " ".join(element.value for element in app.markdown)
        self.assertIn("Scraped-data coverage", rendered_markdown)
        self.assertIn("XGBoost and linked-sample limitations", rendered_markdown)
        self.assertIn("About this prototype", rendered_markdown)
        self.assertIn(
            "should not be interpreted as an official Navigator forecasting or campaign-planning product",
            rendered_markdown,
        )

        next(
            button for button in app.button if button.label == "Search seasonality"
        ).click().run()
        rendered_markdown = " ".join(element.value for element in app.markdown)
        self.assertIn("Destination-specific travel-search seasonality", rendered_markdown)

        next(
            button for button in app.button if button.label == "Search anomalies"
        ).click().run()
        rendered_markdown = " ".join(element.value for element in app.markdown)
        self.assertIn("Travel-search anomaly investigation", rendered_markdown)


if __name__ == "__main__":
    unittest.main()
