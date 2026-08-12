# External Travel Signals Explorer

An exploratory destination-intelligence project developed by Anna Claire Breuss-Burgess during a Navigator internship. It investigates whether external online signals can help non-technical digital marketing stakeholders understand travel interest in four case-study destinations:

- Marrakech
- Hanoi
- Lisbon
- Reykjavik

## Explore the web app

**[Open the deployed External Travel Signals Explorer](https://external-travel-signals-explorer.streamlit.app/)**

The Streamlit app translates the project findings into stakeholder-friendly destination comparisons, historical charts, guided questions and an interactive XGBoost model explorer.

## What the project examines

The project brings together three separate analytical layers:

1. **XGBoost estimates** of a sampled Google Maps review-activity score using TikTok visibility and annual timing.
2. **Destination-specific search seasonality** describing each destination's normal Low, Mid or High travel-search pattern by month.
3. **Travel-search anomalies** identifying months in which search interest differed notably from the destination's seasonal expectation.

These layers are displayed together to help stakeholders assess whether external signals align, conflict or remain inconclusive. Destination, seasonality classifications and anomaly results provide contextual evidence; they are not input features in the XGBoost model.

## Data and linked sample

The analysis was created by:

1. Scraping destination-related TikTok posts.
2. Identifying attractions, restaurants and other visitor locations mentioned in those posts.
3. Collecting Google Maps reviews for the identified locations.
4. Linking TikTok and Google Maps evidence at location-month level.
5. Combining this linked sample with destination-specific Google Trends travel-search data.

The resulting sample does not represent all TikTok activity, visitor locations, Google Maps reviews or travel demand for each destination.

## XGBoost model

The selected saved XGBoost model uses four features:

- Log-transformed TikTok post count
- Log-transformed average TikTok play count
- Sine-transformed calendar month
- Cosine-transformed calendar month

It estimates a constructed sampled Google Maps review-activity score:

```text
sampled Google Maps review count × average review rating
```

The model does not predict bookings, visitors, revenue, total destination reviews or marketing performance. It tests association rather than causation and should be treated as an exploratory proof of concept.

## Travel-search interpretation

The seasonality analysis separates normal monthly patterns from unusual search behaviour. Anomaly results are translated into three labels:

- **Potential anomaly** — search activity met both documented anomaly thresholds.
- **Worth monitoring** — a notable deviation that did not meet both thresholds.
- **Within expected range** — movement consistent with the destination's seasonal context.

These labels prompt further investigation; they are not automatic recommendations to change campaign spending.

## Public-repository data policy

This is a sanitized public release. Raw TikTok posts, TikTok profile information, Google Maps review text, reviewer information, scraper responses and test scrape outputs are deliberately excluded. The included modelling table retains only the numerical fields required by the app, with real place identifiers replaced by opaque sample-location IDs.

See [PUBLIC_DATA_NOTICE.md](PUBLIC_DATA_NOTICE.md) for details. No licence is granted for reuse unless one is added explicitly by the repository owner.

## Repository structure

```text
app.py                         Streamlit entry point
webapp/                        App pages, navigation, styling and data logic
models/                        Saved modelling pipelines
data/                          Sanitized modelling data and aggregate search evidence
tests/                         Data-contract and app-rendering tests
WEB_APP_PLAN.md                Product and presentation plan
WEB_APP_EVIDENCE_CONTENT.md    Approved methods, findings and limitations content
PUBLIC_DATA_NOTICE.md          Public-release privacy and reuse notice
```

## Run locally

Python 3.12 is recommended to match the deployed Streamlit environment.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The tests validate the four-destination, twelve-month evidence grid; anomaly rules and labels; XGBoost feature contract; model safeguards; guided answers; app rendering; and navigation.

## Important limitations

- The linked dataset is small, uneven and concentrated in recent months.
- Scraping and location-identification choices affect the represented sample.
- Google Trends provides relative indices rather than search volumes.
- XGBoost performance varied substantially across chronological evaluation periods.
- Tree models may not extrapolate reliably beyond their observed input ranges.
- The analysis does not establish that TikTok caused search or review activity.
- The four case studies do not demonstrate generalisation to every destination.

For the full methodology, evaluation results and limitations, see [WEB_APP_EVIDENCE_CONTENT.md](WEB_APP_EVIDENCE_CONTENT.md). For the app's product plan and interpretation rules, see [WEB_APP_PLAN.md](WEB_APP_PLAN.md).
