"""Regression tests for the app's display-data contract."""

import unittest

import numpy as np
import pandas as pd

from webapp.data import (
    DataValidationError,
    INVESTIGATION_MONTHS,
    SUPPORTED_DESTINATIONS,
    XGBOOST_FEATURES,
    build_xgboost_features,
    load_destination_monthly_data,
    load_historical_predictions,
    load_modelling_data,
    load_xgboost_model,
    overview_anomaly_status,
    predict_hypothetical_location,
    stakeholder_anomaly_status,
)


class DestinationMonthlyDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_modelling_data()
        cls.monthly = load_destination_monthly_data()

    def test_complete_context_grid(self) -> None:
        self.assertEqual(len(self.monthly), 48)
        self.assertEqual(set(self.monthly["destination"]), set(SUPPORTED_DESTINATIONS))
        self.assertTrue(
            self.monthly.groupby("destination").size().eq(12).all()
        )
        for _, rows in self.monthly.groupby("destination"):
            self.assertTrue(
                pd.DatetimeIndex(rows["month"].sort_values()).equals(INVESTIGATION_MONTHS)
            )
            self.assertEqual(
                rows["season"].value_counts().to_dict(),
                {"Mid": 6, "Low": 3, "High": 3},
            )

    def test_missing_modelling_months_remain_missing(self) -> None:
        missing = self.monthly.loc[
            self.monthly["destination"].eq("marrakech")
            & self.monthly["month"].eq(pd.Timestamp("2025-08-01"))
        ].iloc[0]
        self.assertTrue(pd.isna(missing["tiktok_post_count"]))
        self.assertTrue(pd.isna(missing["actual_review_activity"]))
        self.assertFalse(pd.isna(missing["season"]))
        self.assertFalse(pd.isna(missing["search_interest"]))

    def test_latest_aggregation_reconciles_to_source(self) -> None:
        source = self.raw.loc[
            self.raw["destination"].eq("marrakech")
            & self.raw["month"].eq(pd.Timestamp("2026-07-01"))
        ]
        result = self.monthly.loc[
            self.monthly["destination"].eq("marrakech")
            & self.monthly["month"].eq(pd.Timestamp("2026-07-01"))
        ].iloc[0]
        self.assertEqual(result["tiktok_post_count"], source["total_tiktok_count"].sum())
        self.assertEqual(
            result["actual_review_activity"],
            source["sampled_review_activity_score"].sum(),
        )
        expected_average = (
            source["total_tiktok_play_count"].sum()
            / source["total_tiktok_count"].sum()
        )
        self.assertAlmostEqual(result["average_tiktok_views"], expected_average)

    def test_review_activity_formula_reconciles_to_source(self) -> None:
        expected = self.raw["sampled_reviews_count"] * self.raw["avg_reviews_rating"]
        self.assertTrue(
            np.allclose(
                self.raw["sampled_review_activity_score"],
                expected,
                rtol=1e-9,
                atol=1e-9,
            )
        )

    def test_xgboost_feature_contract_remains_separate(self) -> None:
        model = load_xgboost_model()
        self.assertEqual(tuple(model.feature_names_in_), XGBOOST_FEATURES)
        self.assertNotIn("destination", XGBOOST_FEATURES)
        sample = self.raw.loc[[self.raw.index[0]], list(XGBOOST_FEATURES)]
        prediction = np.asarray(model.predict(sample), dtype=float)
        self.assertEqual(prediction.size, 1)
        self.assertTrue(np.isfinite(prediction).all())

    def test_historical_predictions_cover_and_reconcile_to_monthly_data(self) -> None:
        predicted_rows = load_historical_predictions()
        self.assertEqual(len(predicted_rows), len(self.raw))
        self.assertTrue(np.isfinite(predicted_rows["predicted_review_activity"]).all())
        self.assertTrue(predicted_rows["predicted_review_activity"].ge(0).all())

        expected = (
            predicted_rows.groupby(["destination", "month"])[
                "predicted_review_activity"
            ]
            .sum()
            .sort_index()
        )
        actual = (
            self.monthly.dropna(subset=["predicted_review_activity"])
            .set_index(["destination", "month"])["predicted_review_activity"]
            .sort_index()
        )
        self.assertTrue(np.allclose(actual, expected))

    def test_hypothetical_features_match_notebook_transformations(self) -> None:
        for month in range(1, 13):
            features = build_xgboost_features(3, 16_300, month).iloc[0]
            self.assertAlmostEqual(features["log_tiktok_count"], np.log1p(3))
            self.assertAlmostEqual(
                features["log_avg_tiktok_play_count"],
                np.log1p(16_300),
            )
            self.assertAlmostEqual(
                features["month_sin"],
                np.sin(2 * np.pi * month / 12),
            )
            self.assertAlmostEqual(
                features["month_cos"],
                np.cos(2 * np.pi * month / 12),
            )
            self.assertEqual(tuple(features.index), XGBOOST_FEATURES)

    def test_hypothetical_prediction_safeguards(self) -> None:
        zero_prediction = predict_hypothetical_location(0, 0, 1)
        extreme_prediction = predict_hypothetical_location(1_000_000, 1_000_000_000, 12)
        self.assertTrue(np.isfinite([zero_prediction, extreme_prediction]).all())
        with self.assertRaises(DataValidationError):
            build_xgboost_features(-1, 100, 1)
        with self.assertRaises(DataValidationError):
            build_xgboost_features(1, -100, 1)
        with self.assertRaises(DataValidationError):
            build_xgboost_features(1, 100, 13)

    def test_hypothetical_prediction_has_no_destination_input(self) -> None:
        first = predict_hypothetical_location(3, 16_300, 7)
        second = predict_hypothetical_location(3, 16_300, 7)
        self.assertEqual(first, second)

    def test_stakeholder_anomaly_labels_and_directions(self) -> None:
        self.assertEqual(
            self.monthly["stakeholder_anomaly_status"].value_counts().to_dict(),
            {
                "Potential anomaly": 5,
                "Worth monitoring": 10,
                "Within expected range": 33,
            },
        )
        self.assertTrue(
            self.monthly.apply(
                lambda row: stakeholder_anomaly_status(row)[0]
                == row["stakeholder_anomaly_status"],
                axis=1,
            ).all()
        )
        self.assertTrue(
            self.monthly.loc[self.monthly["actual_vs_expected"].gt(0), "anomaly_direction"]
            .eq("Above expected")
            .all()
        )
        self.assertTrue(
            self.monthly.loc[self.monthly["actual_vs_expected"].lt(0), "anomaly_direction"]
            .eq("Below expected")
            .all()
        )
        self.assertEqual(
            self.monthly["anomaly_marker_label"].ne("Within expected range").sum(),
            15,
        )

    def test_every_anomaly_row_matches_the_documented_edge_conditions(self) -> None:
        absolute_z = self.monthly["standardised_difference"].abs()
        absolute_gap = self.monthly["actual_vs_expected"].abs()
        expected_anomaly = absolute_z.ge(2) & absolute_gap.ge(10)
        expected_monitoring = ~expected_anomaly & (absolute_z.ge(1.5) | absolute_gap.ge(10))

        self.assertTrue(
            self.monthly["anomaly_flag"].astype(bool).equals(expected_anomaly)
        )
        self.assertTrue(
            self.monthly["anomaly_strength"]
            .eq("Notable deviation")
            .equals(expected_monitoring)
        )
        self.assertTrue(
            self.monthly.loc[
                ~(expected_anomaly | expected_monitoring),
                "stakeholder_anomaly_status",
            ].eq("Within expected range").all()
        )

    def test_anomaly_presentation_handles_positive_negative_and_typical_edges(self) -> None:
        cases = (
            (
                pd.Series(
                    {
                        "anomaly_direction": "Above expected",
                        "anomaly_flag": True,
                        "actual_vs_expected": 10.0,
                        "anomaly_strength": "Potential anomaly",
                    }
                ),
                ("Potential anomaly", "positive"),
                ("Potential positive anomaly", "positive"),
            ),
            (
                pd.Series(
                    {
                        "anomaly_direction": "Below expected",
                        "anomaly_flag": True,
                        "actual_vs_expected": -10.0,
                        "anomaly_strength": "Potential anomaly",
                    }
                ),
                ("Potential anomaly", "negative"),
                ("Potential negative anomaly", "negative"),
            ),
            (
                pd.Series(
                    {
                        "anomaly_direction": "Above expected",
                        "anomaly_flag": False,
                        "actual_vs_expected": 10.0,
                        "anomaly_strength": "Notable deviation",
                    }
                ),
                ("Worth monitoring", "monitor"),
                ("No strong departure from seasonal expectations", "neutral"),
            ),
            (
                pd.Series(
                    {
                        "anomaly_direction": "At expected",
                        "anomaly_flag": False,
                        "actual_vs_expected": 0.0,
                        "anomaly_strength": "Within expected range",
                    }
                ),
                ("Within expected range", "typical"),
                ("No strong departure from seasonal expectations", "neutral"),
            ),
        )
        for row, stakeholder_expected, overview_expected in cases:
            stakeholder = stakeholder_anomaly_status(row)
            self.assertEqual(stakeholder[:2], stakeholder_expected)
            self.assertTrue(stakeholder[2].strip())
            self.assertEqual(overview_anomaly_status(row), overview_expected)

    def test_anomaly_baselines_follow_the_investigation_period_rules(self) -> None:
        aug_to_dec = self.monthly.loc[self.monthly["month"].dt.year.eq(2025)]
        jan_to_jul = self.monthly.loc[self.monthly["month"].dt.year.eq(2026)]

        self.assertTrue(aug_to_dec["baseline_year_count"].eq(3).all())
        self.assertTrue(aug_to_dec["baseline_years_used"].eq("2022, 2023, 2024").all())
        self.assertTrue(~aug_to_dec["baseline_years_used"].str.contains("2025").all())
        self.assertTrue(jan_to_jul["baseline_year_count"].eq(4).all())
        self.assertTrue(
            jan_to_jul["baseline_years_used"].eq("2022, 2023, 2024, 2025").all()
        )
        self.assertTrue(~jan_to_jul["baseline_years_used"].str.contains("2026").all())

    def test_each_destination_has_complete_search_context_and_expected_labels(self) -> None:
        expected = {
            "hanoi": {"Potential anomaly": 0, "Worth monitoring": 2, "Within expected range": 10},
            "lisbon": {"Potential anomaly": 2, "Worth monitoring": 5, "Within expected range": 5},
            "marrakech": {"Potential anomaly": 2, "Worth monitoring": 1, "Within expected range": 9},
            "reykjavik": {"Potential anomaly": 1, "Worth monitoring": 2, "Within expected range": 9},
        }
        core_fields = [
            "search_interest",
            "observed_seasonal_index",
            "expected_seasonal_index",
            "expected_seasonal_std",
            "actual_vs_expected",
            "standardised_difference",
            "confidence_note",
        ]
        for destination, rows in self.monthly.groupby("destination"):
            self.assertFalse(rows[core_fields].isna().any().any(), destination)
            actual = rows["stakeholder_anomaly_status"].value_counts().to_dict()
            actual.setdefault("Potential anomaly", 0)
            self.assertEqual(actual, expected[destination])

    def test_overview_surfaces_only_potential_anomalies(self) -> None:
        labels = self.monthly.apply(lambda row: overview_anomaly_status(row)[0], axis=1)
        self.assertFalse(labels.str.contains("Worth monitoring").any())
        self.assertEqual(labels.str.startswith("Potential").sum(), 5)
        latest = self.monthly.loc[self.monthly["month"].eq(self.monthly["month"].max())]
        latest_labels = latest.apply(lambda row: overview_anomaly_status(row)[0], axis=1)
        self.assertTrue(
            latest_labels.eq("No strong departure from seasonal expectations").all()
        )


if __name__ == "__main__":
    unittest.main()
