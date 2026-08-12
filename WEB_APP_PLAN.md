# External Travel Signals Explorer

## Overview

The web app shows whether external online activity suggests growing or weakening interest in four destinations: Marrakech, Hanoi, Lisbon, and Reykjavik.

It combines:

- TikTok visibility as an early attention signal.
- X2's predicted Google Maps review activity as a proxy for destination engagement.
- Destination-specific Low/Mid/High seasonality to describe what is normally expected for each destination and month.
- Travel-search anomalies to identify whether observed search interest was unusually high or low compared with that destination's seasonal expectation.
- Signal agreement to show whether search behaviour and modelled review activity tell a consistent, conflicting, or inconclusive story.

In a nutshell:

> The app helps Navigator identify when online attention around a destination may be strengthening, whether that movement is seasonally expected or unusual, and whether it is worth investigating for potential marketing activity.

It does not predict bookings, prove that TikTok causes travel, or make definitive marketing recommendations. It provides an early external signal that can complement Navigator's first-party data.

Anomaly detection helps the app distinguish normal destination seasonality from unusual external interest, allowing stakeholders to identify signals worth investigating while avoiding overconfident marketing conclusions.

## 1. Purpose

The app helps a non-technical digital marketing stakeholder explore external signs of travel interest across:

- Marrakech
- Hanoi
- Lisbon
- Reykjavik

It answers:

> Is online interest in this destination strengthening, is that activity normal for the season or unusually different from expectations, and is the signal worth investigating further?

It provides evidence for marketing conversations, not automated campaign recommendations.

## 2. Landing page: "What are the signals telling us?"

Start with a short explanation:

> This prototype combines TikTok visibility, predicted Google Maps review activity, destination-specific search seasonality, and travel-search anomalies. It helps distinguish potentially meaningful changes in interest from normal seasonal movement.

Show four destination cards containing:

- Current seasonal classification: Low, Mid, or High
- Recent TikTok direction
- Predicted review-activity level
- Potential travel-search anomaly, if one exists
- Overall evidence: Positive, Negative, Mixed, or Insufficient

To avoid overwhelming users, highlight only **Potential anomalies** on the overview page. Do not surface every smaller deviation there. If no potential anomaly exists, show a neutral message such as "No strong departure from seasonal expectations."

Use the following visual hierarchy:

- Strong blue: potential positive anomaly
- Strong red: potential negative anomaly
- Navigator teal-green (`#22B89A`): within expected range

Include a visible disclaimer:

> These signals indicate online attention and engagement. They do not measure bookings, revenue, or marketing effectiveness. Potential anomalies are prompts for investigation, not recommendations to change campaign spending.

## 3. Destination Explorer

The user selects one of the four case-study destinations.

### Destination briefing

Produce a plain-language summary such as:

> Lisbon is currently in High season. TikTok visibility suggests strong online attention, but travel-search interest is below its normal level for this month. The evidence is therefore mixed rather than a clear sign of unusual growth.

### Key information

Show five cards:

- TikTok visibility: Rising, Stable, or Falling
- X2 prediction: Low, Typical, or High review activity
- Destination season: Low, Mid, or High
- Search anomaly status: Potential anomaly, Worth monitoring, or Within expected range
- Signal agreement: Aligned, Mixed, or Unclear

Exact values can appear underneath or inside a "See details" section.

### Stakeholder-friendly anomaly labels

Map the analytical results to three app labels:

- **Potential anomaly** - strongly highlight because search activity is substantially above or below seasonal expectations.
- **Worth monitoring** - use for a `Notable deviation` that does not meet the full potential-anomaly threshold.
- **Within expected range** - use for typical seasonal movement.

On each destination-detail page, show both Potential anomalies and Worth monitoring months, including whether they were above or below expectations.

Use:

- Strong blue: potential positive anomaly
- Strong red: potential negative anomaly
- Warm orange (`#F59E42`, with `#B76516` text): worth monitoring
- Navigator teal-green (`#22B89A`): within expected range

In the Destination Explorer evidence view, give a **Within expected range** search-status card a white background with a green top accent and green status text. This should follow the same restrained format as the **Worth monitoring** card rather than filling the whole card with colour.

For every highlighted result, include a plain-language explanation and confidence note. For example:

> Search interest was above its seasonal expectation, but the difference was not large enough to be classified as a potential anomaly. This month is worth monitoring.

### Historical chart

Show monthly:

- TikTok post count
- Average TikTok views
- Actual Google Maps review-activity score
- X2 predicted review-activity score
- Observed travel-search interest compared with its seasonal expectation
- Markers for Potential anomaly and Worth monitoring months

Add seasonal shading for Low, Mid, and High months.

Include the calculation directly in the description inside the **Google Maps review activity** section of the Destination Explorer. Do not use a separate calculation card:

```text
Sampled reviews collected for TikTok-mentioned locations
× average Google Maps review rating across those sampled reviews
= sampled Google Maps review-activity score
```

Do not include a worked example. Explain that a higher score reflects more sampled reviews, a higher average rating, or both, and does not measure total destination reviews, visitors, or bookings. Do not repeat the calculation elsewhere. Where space is not limited, use the full phrase **Google Maps review activity** rather than only **review activity**.

State that Google Maps reviews were collected for the locations identified from the TikTok data. At destination-month level, sum the location-level scores across locations with available observations.

This allows users to see whether the model follows observed review activity, where it makes errors, and whether travel-search behaviour provides supporting or conflicting external evidence.

## 4. Seasonal marketing calendar

Display all 12 months for the chosen destination:

```text
Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
Low  Mid  Mid  High Mid  Mid  High High Mid  Mid  Low  Low
```

When a month is selected, explain:

- Its seasonal index
- Whether it is Low, Mid, or High season
- How consistent that pattern has been between years
- Whether observed search interest was above, below, or within its seasonal expectation
- Whether the month is a Potential anomaly, Worth monitoring, or Within expected range
- The confidence note associated with its baseline

Provide cautious marketing context:

- Before high season: potential awareness and planning window
- High season: potentially useful for conversion-oriented research
- Low season: possible value, niche, or early-booking research opportunity
- Unexpected low-season uplift: investigate whether an event, trend, content theme, or source market may be contributing
- Unexpected weakness in high season: investigate price, availability, events, competing destinations, or data quality

Make clear that these are hypotheses. The data does not include campaign costs, conversions, bookings, market-level search origins, or evidence of causation.

## 5. Travel-search anomaly investigation

This layer explains whether observed Google travel-search interest was unusual after accounting for the destination's normal month-by-month seasonal pattern.

### Why it is useful for marketing investigation

Potential positive anomalies may help stakeholders identify:

- Unexpected growth during a normally quiet month
- Interest rising earlier than the normal peak
- A possible event, trend, or content-driven surge worth investigating
- Destinations that may deserve additional campaign research

Potential negative anomalies may help identify:

- A normally strong month underperforming expectations
- Weakening search interest despite strong TikTok visibility
- Disagreement between platforms
- A need to investigate price, availability, events, competing destinations, or data quality

The app should not automatically recommend increasing or decreasing campaign spending. It should recommend a next question, for example:

> Search interest is unusually high for this month. Investigate which markets, events, or content themes may be contributing before making a campaign decision.

For a negative anomaly:

> Search interest is unusually low for this month. Investigate whether pricing, availability, events, competing destinations, or data quality may explain the weakness before making a campaign decision.

### Keep the evidence layers separate

Present anomalies alongside, but separate from, the other evidence:

- **X2 prediction:** expected sampled Google Maps review activity based on TikTok visibility and the month’s position in the annual seasonal cycle.
- **Stakeholder description:** XGBoost uses TikTok visibility and the time of year to estimate sampled Google Maps review activity. It predicts activity for each sampled location and combines the results for the destination and month.
- **Low/Mid/High classification:** normal destination-specific search seasonality.
- **Anomaly status:** whether observed travel-search interest was unusual for that destination and month.

The seasonality classification and anomaly status are contextual evidence. Neither is passed into X2, and neither changes the X2 model.

## 6. X2 Model Explorer

### Inputs

Allow the stakeholder to choose:

- Case-study destination
- Month
- TikTok post count
- Average TikTok play count

The destination is used only to retrieve contextual seasonality and anomaly evidence; it is not passed to X2.

### Outputs

Show:

- Predicted Google Maps review-activity score
- Position relative to historical results: Low, Typical, or High
- Destination's seasonal classification for the selected month
- Search anomaly status for that historical destination-month, where observed search data exists
- Whether inputs are within the model's observed range
- A plain-language interpretation

For example:

> With this level of TikTok visibility, X2 associates August with higher-than-typical review activity. August is historically High season for Lisbon, and search interest was also unusually above its seasonal expectation. The external signals align positively, but the result does not establish that TikTok caused the increase or that marketing spend should change.

If the search activity was typical instead:

> X2 predicts higher review activity, but travel-search interest remained within its expected seasonal range. The modelled activity may reflect TikTok visibility or normal timing rather than wider unusual destination interest.

### What-if comparison

Let the stakeholder compare:

- Current TikTok scenario
- Increased or decreased TikTok visibility
- Difference in X2 prediction

Phrase results as associations, not causal effects. Do not present a historical search anomaly as if it changes a hypothetical X2 prediction.

## 7. Signal interpretation

Create a transparent, rule-based summary:

| Signal pattern | Interpretation |
|---|---|
| Positive search anomaly + high X2 prediction | Signals align positively |
| Negative search anomaly + low X2 prediction | Signals align negatively |
| Positive search anomaly + low X2 prediction | Signals disagree |
| Negative search anomaly + high X2 prediction | Signals disagree |
| Typical search activity + high X2 prediction | Modelled review activity may reflect TikTok visibility or normal timing rather than wider unusual interest |
| Typical search activity + typical/low X2 prediction | No strong combined external signal |
| Sparse or unreliable data | Insufficient evidence |

The app should explain which conditions generated the result. Avoid an unexplained composite score.

This is where the anomaly analysis adds the most value: it prevents the app from turning every rise into a "trend."

## 8. Findings page

Summarise the main findings by destination.

Each destination should have:

- Strongest seasonal months
- Weakest seasonal months
- TikTok and review-activity relationship
- X2's performance
- Potential travel-search anomalies
- Worth monitoring months
- Whether search and X2 signals align, disagree, or remain inconclusive
- One practical question for Navigator to investigate

Example:

> **Lisbon:** Interest is strongly seasonal, with a pronounced summer peak. High summer activity should not automatically be treated as emerging momentum. Search interest substantially above the normal summer expectation would be more informative and worth investigating alongside X2's predicted review activity.

Only include conclusions directly supported by the analysis.

## 9. Confidence and limitations

Every destination briefing, X2 prediction, and highlighted anomaly should include a confidence explanation.

For X2, consider:

- Whether inputs are inside the training range
- X2's historical prediction error
- Missing or sparse TikTok or Google Maps observations

For travel-search anomalies, show the supplied `confidence_note`, which explains:

- Number of complete baseline years used
- Destination-month baseline variability
- That higher variability means lower confidence

Do not merge model confidence and anomaly confidence into one unexplained score. They come from different analyses.

Include a permanent limitations panel:

- X2 predicts sampled Google Maps review activity, not bookings or visitor numbers.
- TikTok posts were scraped first, specific visitor locations mentioned in those posts were identified, and Google Maps reviews were then collected for those locations. This is not a representative sample of all TikTok activity about a destination.
- The selected locations and scraped posts may overrepresent highly visible attractions, accessible content, particular languages, or content surfaced by the collection method.
- Posts from which a specific visitor location could not be identified are not represented in the location-level TikTok-Google Maps analysis.
- A location mention does not show that viewers visited that location or that TikTok activity caused subsequent Google Maps reviews.
- TikTok association does not demonstrate causation.
- X2 uses a general annual cycle, not destination identity.
- Destination-specific seasonality and travel-search anomalies are added as interpretation after prediction.
- A search anomaly means unusual relative to a historical seasonal baseline, not necessarily a lasting trend.
- Potential anomalies may reflect events, news, platform effects, collection issues, or other unobserved factors.
- The dataset is small and covers only four destinations.
- Google Maps reviews, TikTok content, and Google search interest may contain platform and sampling biases.
- The main seasonal profile is based on four complete baseline years; August-December 2025 anomaly expectations use a leave-2025-out baseline of three complete years.
- Marketing effectiveness cannot be assessed without campaign, cost, conversion, booking, price, and availability data.

## 10. Expandable Methodology

Keep exact values, thresholds, and calculations in an expandable section so the main interface remains accessible.

Explain:

- **TikTok and Google Maps sample:** TikTok posts were scraped first, and specific attractions, restaurants, and other visitor locations mentioned in those posts were identified. Google Maps reviews were then collected for those locations. The resulting dataset reflects activity associated with the identified-location sample, rather than all TikTok content, locations, or Google Maps reviews across the destination.
- **Average TikTok views:** total views across the scraped posts associated with the identified locations divided by the number of those posts. It is not unique reach or an estimate of total destination visibility.
- **Sampled Google Maps review activity:** `sampled_reviews_count × avg_reviews_rating` at location level. Reviews were collected for locations identified from the TikTok data, and destination-month values sum the location-level scores with available observations. A higher score reflects more sampled reviews, a higher average rating, or both; it is not total destination reviews, visitors, or bookings.
- `observed_seasonal_index`: observed search interest expressed relative to the destination's estimated level for the relevant year.
- `expected_seasonal_index`: the normal destination-month index calculated from complete baseline years.
- `actual_vs_expected`: observed seasonal index minus expected seasonal index.
- `standardised_difference`: actual-versus-expected gap divided by the destination-month baseline standard deviation.
- **Potential anomaly:** `abs(standardised_difference) >= 2` and `abs(actual_vs_expected) >= 10`.
- **Worth monitoring:** analytical `Notable deviation`, where `abs(standardised_difference) >= 1.5` or `abs(actual_vs_expected) >= 10`, without meeting both Potential anomaly conditions.
- **Within expected range:** neither highlighted condition is met.

Make the baseline methodology explicit:

- August-December 2025 expectations use complete baseline years excluding 2025.
- January-July 2026 expectations use the complete-year baseline because incomplete 2026 was not included in it.
- The investigation contains 48 rows: four destinations by twelve months.

## 11. Guided Q&A

Offer clickable questions:

- What is happening in this destination?
- Is the current search movement unusual or normal seasonality?
- Which months should I investigate?
- When is this destination normally strongest?
- Do the external signals agree or conflict?
- How reliable is this evidence?
- What can this evidence not tell me?
- What should I investigate next?

Group the eight unchanged question cards by scope: four under **Selected month**, two under **Destination pattern**, and two under **Understanding the evidence**. Place the month selector only in the Selected month group and keep it synchronised with the seasonal calendar. Show one full-width answer panel directly below the selected question's group row; move it between groups as the selected question changes and do not repeat it at the bottom. Use calculated answers and prepared templates. A general-purpose chatbot is unnecessary for the first version.

## 12. Recommended navigation

Keep the app to four pages:

1. **Overview** - compare all four destinations and surface only Potential anomalies.
2. **Destination Explorer** - evidence, seasonality, Potential anomalies, Worth monitoring months, and findings.
3. **Model Explorer** - X2 prediction, scenarios, and separate destination context.
4. **Method & Limitations** - definitions, anomaly thresholds, baselines, model performance, and caveats.

## Two-to-three-day build priority

### Day 1

- Build navigation and destination selector.
- Load the dataset, X2 model, seasonality profile, and investigation-period anomaly sheet.
- Create destination cards and historical charts.
- Generate X2 predictions correctly.

### Day 2

- Add the seasonal calendar and model playground.
- Add Potential anomaly, Worth monitoring, and Within expected range labels.
- Add plain-language summaries, next-question prompts, and signal-agreement logic.
- Add input-range checks and separate confidence explanations.
- Complete the findings and limitations pages.

### Day 3, if available

- Add guided questions.
- Improve visual presentation and anomaly highlighting.
- Test every destination, anomaly label, and edge case.
- Deploy and rehearse the demonstration.

The final product can be described as:

> A destination intelligence prototype that translates TikTok visibility, predicted review activity, normal destination seasonality, and unusual travel-search behaviour into understandable external signals for digital marketing investigation.
