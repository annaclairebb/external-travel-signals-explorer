# Web App Evidence, Methods and Limitations

This section consolidates the methods of this project as well as its evaluation, findings and limitations, expanding the confidence notes displayed throughout the web app.

The app combines three distinct evidence layers:

1. XGBoost estimates of sampled Google Maps review activity using TikTok visibility and annual timing.
2. Destination-specific seasonality describing each destination's normal monthly travel-search pattern.
3. Travel-search anomalies identifying months that differ from destination-specific seasonal expectations.

These layers must remain separate. Destination seasonality and anomaly status provide context after prediction; neither is an XGBoost feature and neither changes the model. The combined evidence supports investigation, not automatic campaign recommendations.

## 1. XGBoost, TikTok visibility and sampled Google Maps review activity

### Purpose

The selected XGBoost model without engagement rate estimates the monthly `sampled_review_activity_score` for one sampled visitor location. It tests whether TikTok visibility and general annual timing contain information associated with sampled Google Maps review activity.

The model does not predict bookings, visitors, revenue, total Google Maps reviews, total destination demand or marketing performance.

### How the linked sample was created

1. TikTok posts were scraped using travel-related, destination-specific key words and hashtags.
2. Specific attractions, restaurants and other visitor locations mentioned in those posts were identified.
3. Google Maps reviews were collected for those identified locations.
4. Location-month observations were used to connect the TikTok and Google Maps evidence.

An example of the keywords used to filter the TikTok data during the scraping process:
- Travel Marrakech
- Things to do in Marrakech
- Day in Marrakech
- Days in Marrakech
- #marrakech #travel 
- #visitmarrakech 
- #marrakechtravel 
- #marrakechguide

Exact same keywords for the other three destinations but "Marrakech" was replaced with its destination. 

The sample therefore represents scraped TikTok posts and Google Maps reviews associated with identified locations. It does not represent all TikTok activity, all visitor locations or all Google Maps reviews for a destination. Posts from which a specific location could not be identified are not represented in the location-level analysis.

### Scraped-data coverage

The collection plan aimed to scrape up to 3,000 TikTok records and approximately 2,000 Google Maps reviews for each destination. These were collection targets rather than guarantees: the scraper returned fewer usable records, and duplicate removal and later cleaning reduced the sample further.

The collection log records the following TikTok volumes:

| Destination | Initially collected, including duplicate occurrences | Retained after initial duplicate removal |
|---|---:|---:|
| Lisbon | 2,098 | 875 |
| Marrakech | 2,103 | 853 |
| Hanoi | 2,123 | 1,097 |
| Reykjavik | 2,110 | 901 |
| **Total** | **8,434** | **3,726** |

The collection log records the following Google Maps review volumes:

| Destination | Reviews collected |
|---|---:|
| Lisbon | 1,678 |
| Marrakech | 1,977 |
| Hanoi | 1,912 |
| Reykjavik | 1,912 |
| **Total** | **7,479** |

The current final cleaned combined files contain 3,725 TikTok posts and 7,478 Google Maps reviews—one fewer record in each source than the initial post-deduplication collection log following subsequent processing. These scraped-record totals describe the source-data collection, not the number of posts or reviews ultimately linked to every location-month model observation.

### Measures shown in the app

**TikTok post count** is the number of scraped posts associated with an identified location.

**Average TikTok views** is calculated as:

```text
total views across the scraped posts associated with an identified location
÷ number of those scraped posts
= average TikTok views
```

It is not unique reach and is not an estimate of total destination visibility.

**Sampled Google Maps review activity** is calculated at location level as:

```text
sampled Google Maps review count
× average review rating across those sampled reviews
= sampled Google Maps review-activity score
```

At destination-month level, the app sums the available location-level scores. A higher score can reflect more sampled reviews, a higher average rating, or both. It is a constructed score in the units of the modelling target—not total review activity.

### XGBoost inputs

The saved XGBoost model receives exactly four features:

- `log_tiktok_count`: log-transformed TikTok post count.
- `log_avg_tiktok_play_count`: log-transformed average TikTok play count.
- `month_sin`: sine-transformed calendar month.
- `month_cos`: cosine-transformed calendar month.

The two month transformations represent the annual cycle without treating December and January as unrelated periods. Engagement rate, attraction classifier and destination were excluded because they did not improve chronological validation performance sufficiently. The selected XGBoost model had the lowest Mean May and June fold MAE values compared to the other XGBoost models with different features. The XGBoost model was selected before final July test. 

Destination identity, destination Low/Mid/High seasonality, travel-search values and anomaly status are not passed to XGBoost.

### Model-development design

The model was evaluated chronologically rather than with a random split. Earlier observations were used for development, with May and June assessed as separate validation periods and July retained as a final unseen test period. This reduces future-information leakage and better reflects the intended future-facing use.

The dataset contained 131 place-month observations:

- 75 observations available for model development.
- 56 observations in the final July test set.

Locations appeared for different numbers of months, so frequently observed locations contributed more observations than locations represented in only one or two months.

### Recorded performance

Mean absolute error (MAE) is the main performance measure. It is expressed in units of the sampled review-activity score and represents the average absolute difference between prediction and observation.

| Evaluation period | XGBoost MAE | Destination historical-mean baseline MAE | Difference |
|---|---:|---:|---:|
| May validation | 47.16 | 50.96 | XGBoost lower by 3.80 |
| June validation | 98.95 | 108.54 | XGBoost lower by 9.59 |
| Mean validation | **73.05** | **79.75** | **Approximately 8.4% lower** |
| July final test | **251.60** | **253.84** | **2.24 lower; approximately 0.9%** |

Additional July XGBoost results:

- Median absolute error: 284.87.
- Root mean squared error: 289.96.
- Test observations: 56 location-month rows.

Held-out July error varied by destination:

| Destination | July test rows | XGBoost MAE | XGBoost median absolute error |
|---|---:|---:|---:|
| Hanoi | 12 | 279.34 | 244.76 |
| Lisbon | 15 | 286.29 | 296.76 |
| Marrakech | 12 | 225.50 | 206.60 |
| Reykjavik | 17 | 219.83 | 232.81 |

### Supported finding

TikTok post volume and average play count, combined with annual timing, produced lower error than the destination historical-mean baseline in both validation months. This provides limited evidence that the selected external signals contain some predictive information beyond simply using a destination's previous average activity.

The improvement was not stable. Error increased from 47.16 in May to 98.95 in June and then to 251.60 in July. In July, XGBoost only marginally improved upon the destination baseline. The most defensible conclusion is:

> TikTok visibility shows potential as a supplementary external travel signal, but the current evidence is not strong or stable enough for independent travel-demand forecasting or decision-making.

The model should be described as an exploratory proof of concept, not a reliable forecasting system.

### How predictions should be presented

- “XGBoost estimates the sampled Google Maps review-activity score associated with TikTok visibility and seasonality.”
- “Predictions are generated for each sampled location and then summed for the destination-month.”
- “The result is an association, not evidence that TikTok caused review activity.”
- “The destination supplies contextual seasonality and anomaly evidence but is not a model input.”
- “The estimate does not predict bookings, visitors or marketing performance.”

### XGBoost and linked-sample limitations

1. **Small and unbalanced data.** There are only 131 place-month observations. This is small for learning nonlinear relationships, and locations contribute unequal numbers of months.
2. **Sample-controlled target.** Review counts were controlled during scraping, so the target partly reflects the collection method.
3. **Review ordering.** Google Maps reviews were sorted by “most relevant,” not “most recent.” Their monthly distribution may not represent all reviews posted chronologically.
4. **Selected-location sample.** Highly visible attractions, accessible posts, particular languages or content surfaced by the collection method may be overrepresented.
5. **Unidentified locations excluded.** TikTok posts without an identifiable visitor location are not included in the linked location-level analysis.
6. **Viral-post sensitivity.** Average play count can be influenced by a small number of viral posts. Log transformation reduces but does not remove this influence.
7. **Platform measurement error.** Algorithms, search visibility, deleted posts and collection timing can affect TikTok measures.
8. **July distribution shift.** The large July error suggests that learned relationships did not transfer reliably to the final period. July may contain different activity levels, locations or concentration of review activity.
9. **Limited extrapolation.** Tree models generally predict within learned patterns and may perform poorly when future values fall beyond earlier training ranges.
10. **TikTok contribution not isolated.** XGBoost includes both TikTok features and annual timing. It was not compared with an otherwise identical month-only XGBoost model, so the specific incremental contribution of TikTok has not been isolated.
11. **Same-month association.** TikTok and review measures come from the same month. The model tests co-movement, not whether TikTok precedes later review activity. Lagged variables would provide a stronger forecasting test.
12. **No causal identification.** Season, events, campaigns, news, price, availability and destination popularity could affect both platforms.
13. **Limited geographic generalisability.** Only four destinations and selected locations are represented. Excluding destination from the feature set does not demonstrate performance on an entirely unseen destination.
14. **Limited validation evidence.** Only two validation months were available. No confidence intervals are reported for MAE or individual predictions.
15. **Scraping targets and retained coverage differ.** The planned per-destination record targets were not fully returned as usable, unique observations. The collection log recorded 8,434 TikTok records including duplicate occurrences, reduced to 3,726 after initial duplicate removal, and 7,479 Google Maps reviews. Subsequent processing left 3,725 TikTok posts and 7,478 reviews in the current final cleaned combined files. The uneven retained coverage limits representativeness and comparability across destinations.
16. **Most modelling rows are recent and July-heavy.** Of 131 place-month modelling observations, 56 are from July 2026 and only 75 are spread across all earlier months. Individual pre-July months contain between 1 and 26 observations. Retaining July as the final chronological test was methodologically appropriate, but it left relatively little earlier data for model development while testing on the month with the largest and potentially different sample. This imbalance makes it difficult to separate a genuine time-period shift from changes in location coverage or data availability and contributes to uncertainty around the large July error.

## 2. Destination-specific travel-search seasonality

### Purpose

The seasonality layer describes what is normally Low, Mid or High travel-search season for each destination and calendar month. It connects the evidence back to Marrakech, Hanoi, Lisbon and Reykjavik without adding destination to the XGBoost model.

This layer is contextual evidence. It is not an XGBoost feature and does not change an XGBoost prediction.

### Search data

The seasonality analysis used destination-specific Google Trends travel-topic data with the following settings:

- Destinations: Marrakech, Hanoi, Lisbon and Reykjavik.
- Search geography: worldwide.
- Search type: web search.
- Topic: travel.
- Source frequency: weekly, aggregated to monthly means.
- Historical window: the available five-year extract.

Google Trends values are relative indices, not numbers of searches.

### Seasonal-index calculation

Only complete destination calendar years were used for the reusable seasonality profile.

For each destination-year:

```text
year-normalised monthly index
= 100 × monthly search interest
  ÷ destination's average monthly search interest in that year
```

An index of 100 represents the destination's estimated average monthly level in that year. Values above 100 indicate relatively stronger search interest; values below 100 indicate relatively weaker interest.

For each destination and calendar month, the profile then calculates:

- `seasonal_index`: mean year-normalised index across complete baseline years.
- `seasonal_index_std`: standard deviation across those complete baseline years.
- `baseline_years`: number of complete years used.

The main profile uses four complete baseline years.

### Low/Mid/High classification

Months are ranked separately within each destination using the unrounded seasonal index:

- Three lowest-ranked months: **Low**.
- Middle six months: **Mid**.
- Three highest-ranked months: **High**.

This is the 3–6–3 classification. It guarantees that every destination has all three categories and avoids imposing a universal percentage threshold. The categories are relative within a destination; a High month for one destination is not automatically equivalent to a High month for another. The continuous seasonal index should be retained when comparing the strength of patterns.

### Destination seasonal findings

| Destination | Normally High months | Normally Low months |
|---|---|---|
| Hanoi | August, October, December | April, May, June |
| Lisbon | April, July, August | January, November, December |
| Marrakech | February, September, December | May, June, July |
| Reykjavik | June, July, August | March, April, November |

These labels describe normal relative timing, not marketing performance. A High month should not automatically be called a trend, and a Low month should not automatically be treated as a poor opportunity.

### How seasonality should be presented

- “The destination's normal Low, Mid or High search season for this month.”
- “A seasonal index compares search interest with the destination's estimated annual level.”
- “An index of 100 represents that level; values above 100 indicate relatively stronger interest and values below 100 indicate relatively weaker interest.”
- “It is a relative measure, not the number of searches.”
- “Seasonality is destination-specific context and is not an XGBoost feature.”

Possible research framing:

- Before High season: investigate awareness and planning behaviour.
- High season: investigate whether other signals show anything beyond normal strong timing.
- Low season: investigate value, niche or early-booking themes.
- Unexpected Low-season uplift: investigate events, content themes or source markets.
- Unexpected weakness in High season: investigate price, availability, events, competing destinations or data quality.

These are hypotheses and next questions, not campaign-spend recommendations.

### Seasonality confidence and limitations

1. **Relative measure.** The index describes relative search interest, not absolute search volume or traveller counts.
2. **Four-year baseline.** The main profile is based on four complete years, which limits certainty about long-term stability.
3. **Between-year variability.** `seasonal_index_std` shows how much a destination-month varied across baseline years. Higher variability means lower confidence in a precise expectation.
4. **Forced ranking.** The 3–6–3 method always assigns three High and three Low months even when differences between months are small.
5. **Within-destination meaning.** Low/Mid/High labels are not directly comparable across destinations without the continuous index.
6. **Worldwide aggregation.** The search data does not identify which source markets generated the interest.
7. **Platform effects.** Google Trends can reflect changes in platform use, topic classification and sampling as well as traveller behaviour.
8. **Context, not outcome.** Seasonality does not measure bookings, conversion, revenue, price or availability.

## 3. Travel-search anomaly investigation

### Purpose

The anomaly layer asks whether observed travel-search interest was unusual for a destination and month after accounting for that destination's normal seasonal pattern.

It helps distinguish normal seasonal movement from external interest worth investigating. It does not convert every increase into a “trend,” and it does not change the XGBoost model.

### Investigation period and data contract

The investigation covers August 2025 through July 2026 for all four destinations:

- 4 destinations × 12 months = 48 validated rows.
- `seasonality_profile` remains unchanged as the reusable profile.
- `incomplete_year_anomalies` is retained separately for audit purposes.
- The investigation results are stored in `investigation_period_anomalies`.

### Baseline method

**August–December 2025**

- Expected monthly seasonal indices and standard deviations use complete destination-years excluding 2025.
- The baseline therefore contains three complete years.
- The observed 2025 seasonal index uses each destination's complete 2025 calendar-year mean, preventing the August–December subset from defining its own annual level.

**January–July 2026**

- Expectations use all complete destination-years because incomplete 2026 was never part of that baseline.
- The baseline contains four complete years.
- The underlying 2026 level is estimated for each destination as the median of `search_interest / (expected_seasonal_index / 100)` across January–July.
- Observed monthly indices are expressed relative to that estimated 2026 level.

### Anomaly calculations

- `search_interest`: observed monthly Google Trends interest.
- `observed_seasonal_index`: the observed month expressed relative to the estimated level for the relevant destination-year.
- `expected_seasonal_index`: normal destination-month index from the applicable complete-year baseline.
- `expected_seasonal_std`: between-year standard deviation for that destination-month baseline.
- `actual_vs_expected = observed_seasonal_index - expected_seasonal_index`.
- `standardised_difference = actual_vs_expected ÷ expected_seasonal_std`.
- `anomaly_direction`: Above expected or Below expected.
- `baseline_years_used`, `baseline_year_count` and `confidence_note`: audit and interpretation fields retained in the app.

### Stakeholder labels and thresholds

**Potential anomaly**

```text
abs(standardised_difference) >= 2
AND
abs(actual_vs_expected) >= 10
```

Both conditions must be met. These results receive the strongest highlighting.

**Worth monitoring**

The analytical result is a `Notable deviation` when either:

```text
abs(standardised_difference) >= 1.5
OR
abs(actual_vs_expected) >= 10
```

but the row does not meet both Potential anomaly conditions.

**Within expected range**

Neither highlighted condition is met.

App colours:

- Potential positive anomaly: strong blue.
- Potential negative anomaly: strong red/pink.
- Worth monitoring: warm orange `#F59E42`, with `#B76516` text.
- Within expected range: Navigator teal-green `#22B89A`.

### Validated destination anomaly findings

| Destination | Potential anomalies | Worth monitoring |
|---|---|---|
| Hanoi | None | October 2025 above expected; November 2025 above expected |
| Lisbon | August 2025 above expected; February 2026 above expected | October 2025 below expected; December 2025 below expected; March 2026 above expected; June 2026 below expected; July 2026 below expected |
| Marrakech | February 2026 above expected; March 2026 above expected | January 2026 above expected |
| Reykjavik | February 2026 above expected | August 2025 above expected; December 2025 below expected |

Across the complete investigation there are:

- 5 Potential anomalies.
- 10 Worth monitoring months.
- 33 months Within expected range.

### Marketing-investigation value

Potential positive anomalies can prompt investigation of:

- Unexpected growth during a normally quiet month.
- Interest rising earlier than the normal peak.
- Events, trends, source markets or content themes that may be contributing.

Potential negative anomalies can prompt investigation of:

- A normally strong month underperforming expectations.
- Weakening search despite strong TikTok visibility.
- Disagreement between platforms.
- Price, availability, events, competing destinations or data quality.

The app must not automatically recommend increasing or decreasing campaign spending. Appropriate wording is:

> Search interest is unusually high or low for this month. Investigate the relevant markets, events, content themes, pricing, availability or data quality before making a campaign decision.

### Signal-agreement interpretation

Search and XGBoost evidence can be compared only as separate layers:

| Pattern | Stakeholder interpretation |
|---|---|
| Positive search anomaly + High XGBoost prediction | Signals broadly align positively |
| Negative search anomaly + Low XGBoost prediction | Signals broadly align negatively |
| Positive search anomaly + Low XGBoost prediction | Signals disagree |
| Negative search anomaly + High XGBoost prediction | Signals disagree |
| Within-expected search + High XGBoost prediction | Modelled review activity may reflect TikTok visibility or normal timing rather than unusual wider interest |
| Within-expected search + Typical/Low XGBoost prediction | No strong combined external signal |
| Sparse or unreliable evidence | Insufficient evidence |

The app should state which conditions generated an interpretation and should not create an unexplained composite score.

### Anomaly confidence and limitations

1. **Confidence is destination-month specific.** The app should show the supplied `confidence_note`, including baseline-year count and baseline standard deviation.
2. **Higher variability lowers confidence.** A large `expected_seasonal_std` makes a precise monthly expectation less certain.
3. **Three-year 2025 baseline.** August–December 2025 expectations use only three complete leave-2025-out baseline years.
4. **Estimated 2026 level.** January–July 2026 observed indices depend on an estimated incomplete-year level derived from those seven months.
5. **Anomaly is not a trend.** A single unusual month does not establish persistence.
6. **Multiple possible causes.** Events, news, advertising, price, availability, platform changes, collection issues and other unobserved factors may create a deviation.
7. **Worldwide search data.** The analysis does not identify the source markets behind a change.
8. **Relative platform signal.** Search interest does not equal bookings, visitors, conversion or revenue.
9. **No causal link to TikTok or reviews.** Agreement across platforms does not prove that one platform caused movement on another.
10. **Separate confidence concepts.** Search-anomaly confidence and XGBoost reliability must not be merged into one score.

## Overall app conclusion

The three evidence layers together can show whether online attention appears stronger or weaker, whether that movement is normal for the destination and month, and whether separate signals align or conflict. They cannot determine why the movement occurred or whether marketing spend should change.

The most defensible app-level statement is:

> The External Travel Signals Explorer distinguishes normal destination seasonality from unusual external interest and shows how that context compares with TikTok visibility and modelled sampled Google Maps review activity. It identifies signals worth investigating while avoiding causal or forecasting claims that the evidence cannot support.

## About this prototype

Developed by Anna Claire Breuss-Burgess as part of a Navigator internship project. The analysis and app are an exploratory prototype and should not be interpreted as an official Navigator forecasting or campaign-planning product.
