"""Cached data access and validation for the stakeholder web app."""

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELLING_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed-combined" / "modelling_table.csv"
)
SEASONALITY_WORKBOOK_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed-combined"
    / "destination_month_seasonality_profile.xlsx"
)
XGBOOST_MODEL_PATH = PROJECT_ROOT / "models" / "selected_xgboost_x2.joblib"

SUPPORTED_DESTINATIONS = frozenset({"marrakech", "hanoi", "lisbon", "reykjavik"})
XGBOOST_FEATURES = (
    "log_tiktok_count",
    "log_avg_tiktok_play_count",
    "month_sin",
    "month_cos",
)

MODELLING_REQUIRED_COLUMNS = {
    "month",
    "destination",
    "place_id",
    "sampled_reviews_count",
    "avg_reviews_rating",
    "sampled_review_activity_score",
    "total_tiktok_count",
    "total_tiktok_play_count",
    "avg_tiktok_play_count",
    *XGBOOST_FEATURES,
}
SEASONALITY_REQUIRED_COLUMNS = {
    "destination",
    "month_number",
    "seasonal_index",
    "seasonal_index_std",
    "baseline_years",
    "season_rank",
    "season",
    "month_name",
}
ANOMALY_REQUIRED_COLUMNS = {
    "destination",
    "month_date",
    "search_interest",
    "observed_seasonal_index",
    "expected_seasonal_index",
    "expected_seasonal_std",
    "actual_vs_expected",
    "standardised_difference",
    "anomaly_direction",
    "anomaly_strength",
    "anomaly_flag",
    "baseline_method",
    "baseline_years_used",
    "baseline_year_count",
    "confidence_note",
}


class DataValidationError(ValueError):
    """Raised when an app data source does not satisfy its expected contract."""


@dataclass(frozen=True)
class AppData:
    """The four validated evidence sources used by the web app."""

    modelling: pd.DataFrame
    xgboost_model: object
    seasonality: pd.DataFrame
    anomalies: pd.DataFrame


INVESTIGATION_MONTHS = pd.date_range("2025-08-01", "2026-07-01", freq="MS")


def _require_file(path: Path) -> None:
    if not path.is_file():
        raise DataValidationError(f"Required data source was not found: {path}")


def _require_columns(
    frame: pd.DataFrame,
    required_columns: set[str],
    source_name: str,
) -> None:
    missing = sorted(required_columns.difference(frame.columns))
    if missing:
        raise DataValidationError(
            f"{source_name} is missing required columns: {', '.join(missing)}"
        )


def _normalise_destinations(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["destination"] = result["destination"].astype("string").str.strip().str.lower()
    return result


def _validate_destinations(frame: pd.DataFrame, source_name: str) -> None:
    actual = frozenset(frame["destination"].dropna().unique())
    if actual != SUPPORTED_DESTINATIONS:
        raise DataValidationError(
            f"{source_name} destinations must be exactly "
            f"{sorted(SUPPORTED_DESTINATIONS)}; found {sorted(actual)}."
        )


def _validate_destination_month_grid(
    frame: pd.DataFrame,
    month_column: str,
    source_name: str,
) -> None:
    if len(frame) != 48:
        raise DataValidationError(f"{source_name} must contain 48 rows; found {len(frame)}.")
    if frame.duplicated(["destination", month_column]).any():
        raise DataValidationError(
            f"{source_name} contains duplicate destination-month records."
        )
    counts = frame.groupby("destination", observed=True).size()
    if not counts.reindex(sorted(SUPPORTED_DESTINATIONS)).eq(12).all():
        raise DataValidationError(
            f"{source_name} must contain 12 records for each destination."
        )


@st.cache_data(show_spinner=False)
def load_modelling_data() -> pd.DataFrame:
    """Load and validate the historical table used by the saved model."""
    _require_file(MODELLING_DATA_PATH)
    frame = pd.read_csv(MODELLING_DATA_PATH, parse_dates=["month"])
    _require_columns(frame, MODELLING_REQUIRED_COLUMNS, "Modelling table")
    frame = _normalise_destinations(frame)
    _validate_destinations(frame, "Modelling table")

    if frame["month"].isna().any():
        raise DataValidationError("Modelling table contains invalid month values.")
    required_numeric = [
        "sampled_reviews_count",
        "avg_reviews_rating",
        "sampled_review_activity_score",
        "total_tiktok_count",
        "avg_tiktok_play_count",
        *XGBOOST_FEATURES,
    ]
    if frame[required_numeric].isna().any().any():
        raise DataValidationError("Modelling table contains missing required numeric values.")
    expected_review_activity = (
        frame["sampled_reviews_count"] * frame["avg_reviews_rating"]
    )
    if not np.allclose(
        frame["sampled_review_activity_score"],
        expected_review_activity,
        rtol=1e-9,
        atol=1e-9,
    ):
        raise DataValidationError(
            "Review-activity scores must equal sampled review count multiplied "
            "by average review rating."
        )
    return frame.sort_values(["month", "destination"]).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_seasonality_profile() -> pd.DataFrame:
    """Load the separate destination-month Low/Mid/High context."""
    _require_file(SEASONALITY_WORKBOOK_PATH)
    frame = pd.read_excel(SEASONALITY_WORKBOOK_PATH, sheet_name="seasonality_profile")
    _require_columns(frame, SEASONALITY_REQUIRED_COLUMNS, "Seasonality profile")
    frame = _normalise_destinations(frame)
    _validate_destinations(frame, "Seasonality profile")
    _validate_destination_month_grid(frame, "month_number", "Seasonality profile")

    if not frame["month_number"].between(1, 12).all():
        raise DataValidationError("Seasonality profile contains an invalid month number.")
    if not set(frame["season"].dropna()).issubset({"Low", "Mid", "High"}):
        raise DataValidationError("Seasonality profile contains an invalid season label.")
    return frame.sort_values(["destination", "month_number"]).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_investigation_anomalies() -> pd.DataFrame:
    """Load the August 2025-July 2026 search-anomaly investigation."""
    _require_file(SEASONALITY_WORKBOOK_PATH)
    frame = pd.read_excel(
        SEASONALITY_WORKBOOK_PATH,
        sheet_name="investigation_period_anomalies",
        parse_dates=["month_date"],
    )
    _require_columns(frame, ANOMALY_REQUIRED_COLUMNS, "Investigation anomalies")
    frame = _normalise_destinations(frame)
    _validate_destinations(frame, "Investigation anomalies")
    _validate_destination_month_grid(frame, "month_date", "Investigation anomalies")

    for destination, destination_rows in frame.groupby("destination", observed=True):
        actual_months = pd.DatetimeIndex(destination_rows["month_date"].sort_values())
        if not actual_months.equals(INVESTIGATION_MONTHS):
            raise DataValidationError(
                f"Investigation anomalies for {destination} must cover "
                "August 2025 through July 2026 exactly."
            )

    calculated_flags = (
        frame["standardised_difference"].abs().ge(2)
        & frame["actual_vs_expected"].abs().ge(10)
    )
    if not frame["anomaly_flag"].astype(bool).equals(calculated_flags):
        raise DataValidationError(
            "Investigation anomaly flags do not match the documented thresholds."
        )
    return frame.sort_values(["destination", "month_date"]).reset_index(drop=True)


@st.cache_resource(show_spinner=False)
def load_xgboost_model() -> object:
    """Load the existing fitted XGBoost pipeline without modifying it."""
    _require_file(XGBOOST_MODEL_PATH)
    model = joblib.load(XGBOOST_MODEL_PATH)
    actual_features = tuple(getattr(model, "feature_names_in_", ()))
    if actual_features != XGBOOST_FEATURES:
        raise DataValidationError(
            "Saved XGBoost feature contract changed. Expected "
            f"{list(XGBOOST_FEATURES)}; found {list(actual_features)}."
        )
    if "destination" in actual_features:
        raise DataValidationError("Destination must not be a feature in XGBoost.")
    if not callable(getattr(model, "predict", None)):
        raise DataValidationError("Saved XGBoost object does not provide predict().")
    return model


def load_app_data() -> AppData:
    """Load all validated sources and run a non-mutating prediction smoke test."""
    modelling = load_modelling_data()
    model = load_xgboost_model()
    seasonality = load_seasonality_profile()
    anomalies = load_investigation_anomalies()

    smoke_input = modelling.loc[[modelling.index[0]], list(XGBOOST_FEATURES)]
    smoke_prediction = np.asarray(model.predict(smoke_input), dtype=float)
    if smoke_prediction.size != 1 or not np.isfinite(smoke_prediction).all():
        raise DataValidationError("Saved XGBoost model did not return a valid prediction.")

    return AppData(
        modelling=modelling,
        xgboost_model=model,
        seasonality=seasonality,
        anomalies=anomalies,
    )


@st.cache_data(show_spinner=False)
def load_historical_predictions() -> pd.DataFrame:
    """Generate one unchanged-model prediction for every location-month row."""
    modelling = load_modelling_data()
    model = load_xgboost_model()
    prediction_input = modelling.loc[:, list(XGBOOST_FEATURES)]
    predictions = np.asarray(model.predict(prediction_input), dtype=float)

    if predictions.shape != (len(modelling),):
        raise DataValidationError(
            "XGBoost must return one prediction for every modelling row."
        )
    if not np.isfinite(predictions).all():
        raise DataValidationError("XGBoost returned a non-finite historical prediction.")
    if (predictions < 0).any():
        raise DataValidationError(
            "XGBoost returned a negative historical review-activity prediction; "
            "the app does not silently clip model outputs."
        )

    result = modelling.copy()
    result["predicted_review_activity"] = predictions
    return result


def build_xgboost_features(
    tiktok_post_count: float,
    average_tiktok_views: float,
    month_number: int,
) -> pd.DataFrame:
    """Transform stakeholder inputs exactly as in the modelling notebook."""
    raw_values = np.asarray([tiktok_post_count, average_tiktok_views], dtype=float)
    if not np.isfinite(raw_values).all():
        raise DataValidationError("TikTok scenario inputs must be finite numbers.")
    if (raw_values < 0).any():
        raise DataValidationError("TikTok scenario inputs cannot be negative.")
    if month_number not in range(1, 13):
        raise DataValidationError("Month number must be between 1 and 12.")

    angle = 2 * np.pi * month_number / 12
    values = {
        "log_tiktok_count": np.log1p(float(tiktok_post_count)),
        "log_avg_tiktok_play_count": np.log1p(float(average_tiktok_views)),
        "month_sin": np.sin(angle),
        "month_cos": np.cos(angle),
    }
    features = pd.DataFrame([values], columns=XGBOOST_FEATURES)
    if not np.isfinite(features.to_numpy(dtype=float)).all():
        raise DataValidationError("Transformed XGBoost features must be finite.")
    return features


def predict_hypothetical_location(
    tiktok_post_count: float,
    average_tiktok_views: float,
    month_number: int,
) -> float:
    """Predict one hypothetical sampled location-month without destination input."""
    features = build_xgboost_features(
        tiktok_post_count,
        average_tiktok_views,
        month_number,
    )
    prediction = np.asarray(load_xgboost_model().predict(features), dtype=float)
    if prediction.size != 1 or not np.isfinite(prediction).all():
        raise DataValidationError("XGBoost did not return one finite scenario prediction.")
    if prediction[0] < 0:
        raise DataValidationError(
            "XGBoost returned a negative review-activity prediction; the app does "
            "not silently clip model outputs."
        )
    return float(prediction[0])


@st.cache_data(show_spinner=False)
def load_model_input_ranges() -> dict[str, tuple[float, float]]:
    """Return observed raw-input ranges for cautious scenario interpretation."""
    modelling = load_modelling_data()
    return {
        "tiktok_post_count": (
            float(modelling["total_tiktok_count"].min()),
            float(modelling["total_tiktok_count"].max()),
        ),
        "average_tiktok_views": (
            float(modelling["avg_tiktok_play_count"].min()),
            float(modelling["avg_tiktok_play_count"].max()),
        ),
    }


def stakeholder_anomaly_status(row) -> tuple[str, str, str]:
    """Translate analytical anomaly fields into stakeholder-facing context."""
    direction = str(row["anomaly_direction"])
    if bool(row["anomaly_flag"]):
        tone = "positive" if float(row["actual_vs_expected"]) > 0 else "negative"
        explanation = (
            f"Search activity was {direction.lower()} and met both potential-anomaly "
            "thresholds. Treat this as a prompt for investigation, not a campaign decision."
        )
        return "Potential anomaly", tone, explanation
    if str(row["anomaly_strength"]) == "Notable deviation":
        explanation = (
            f"Search activity was {direction.lower()}, but the result did not meet both "
            "conditions required for a potential anomaly. This month is worth monitoring."
        )
        return "Worth monitoring", "monitor", explanation
    return (
        "Within expected range",
        "typical",
        "Search activity remained within the destination-month's expected seasonal range.",
    )


def overview_anomaly_status(row) -> tuple[str, str]:
    """Return a potential-only Overview label and visual tone."""
    if bool(row["anomaly_flag"]):
        if float(row["actual_vs_expected"]) > 0:
            return "Potential positive anomaly", "positive"
        return "Potential negative anomaly", "negative"
    return "No strong departure from seasonal expectations", "neutral"


@st.cache_data(show_spinner=False)
def load_destination_monthly_data() -> pd.DataFrame:
    """Create one display row per destination-month without imputing missing evidence."""
    modelling = load_historical_predictions()
    seasonality = load_seasonality_profile()
    anomalies = load_investigation_anomalies()

    observed = (
        modelling.groupby(["destination", "month"], observed=True)
        .agg(
            place_count=("place_id", "nunique"),
            tiktok_post_count=("total_tiktok_count", "sum"),
            tiktok_play_count=("total_tiktok_play_count", "sum"),
            actual_review_activity=("sampled_review_activity_score", "sum"),
            predicted_review_activity=("predicted_review_activity", "sum"),
        )
        .reset_index()
    )
    observed["average_tiktok_views"] = (
        observed["tiktok_play_count"] / observed["tiktok_post_count"]
    )

    complete_grid = pd.MultiIndex.from_product(
        [sorted(SUPPORTED_DESTINATIONS), INVESTIGATION_MONTHS],
        names=["destination", "month"],
    ).to_frame(index=False)
    monthly = complete_grid.merge(
        observed,
        how="left",
        on=["destination", "month"],
        validate="one_to_one",
    )
    monthly["month_number"] = monthly["month"].dt.month
    monthly = monthly.merge(
        seasonality,
        how="left",
        on=["destination", "month_number"],
        validate="many_to_one",
    )
    monthly = monthly.merge(
        anomalies.rename(columns={"month_date": "month"}),
        how="left",
        on=["destination", "month"],
        validate="one_to_one",
        suffixes=("", "_anomaly"),
    )
    monthly["stakeholder_anomaly_status"] = np.select(
        [
            monthly["anomaly_flag"].astype(bool),
            monthly["anomaly_strength"].eq("Notable deviation"),
        ],
        ["Potential anomaly", "Worth monitoring"],
        default="Within expected range",
    )
    monthly["stakeholder_anomaly_tone"] = np.select(
        [
            monthly["anomaly_flag"].astype(bool)
            & monthly["actual_vs_expected"].gt(0),
            monthly["anomaly_flag"].astype(bool)
            & monthly["actual_vs_expected"].lt(0),
            monthly["anomaly_strength"].eq("Notable deviation"),
        ],
        ["positive", "negative", "monitor"],
        default="typical",
    )
    monthly["anomaly_marker_label"] = np.select(
        [
            monthly["anomaly_flag"].astype(bool)
            & monthly["actual_vs_expected"].gt(0),
            monthly["anomaly_flag"].astype(bool)
            & monthly["actual_vs_expected"].lt(0),
            monthly["anomaly_strength"].eq("Notable deviation"),
        ],
        ["Potential positive anomaly", "Potential negative anomaly", "Worth monitoring"],
        default="Within expected range",
    )

    if len(monthly) != 48:
        raise DataValidationError(
            f"Destination-month presentation data must contain 48 rows; found {len(monthly)}."
        )
    if monthly[["season", "search_interest", "expected_seasonal_index"]].isna().any().any():
        raise DataValidationError(
            "Destination-month presentation data is missing seasonality or search context."
        )
    expected_status_counts = {
        "Potential anomaly": 5,
        "Worth monitoring": 10,
        "Within expected range": 33,
    }
    if monthly["stakeholder_anomaly_status"].value_counts().to_dict() != expected_status_counts:
        raise DataValidationError(
            "Stakeholder anomaly labels do not reconcile to the validated 48-row investigation."
        )
    return monthly.sort_values(["destination", "month"]).reset_index(drop=True)
