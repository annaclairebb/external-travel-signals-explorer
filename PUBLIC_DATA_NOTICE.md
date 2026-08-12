# Public data notice

This public repository is a sanitized release of the External Travel Signals Explorer.

It intentionally excludes:

- Raw TikTok posts and profile information
- Raw Google Maps reviews and reviewer information
- Scraper responses, tokens and collection logs
- Test scrape outputs
- Internal working files and notebook outputs

The included modelling table contains only the numerical location-month fields required to reproduce the web app. Real Google place identifiers and place names have been replaced with opaque `sample_location_*` identifiers. The seasonality workbook contains destination-month aggregate search evidence used by the app.

The included data must not be interpreted as a complete or representative measure of TikTok activity, Google Maps reviews, visitor demand, bookings or marketing performance. See `WEB_APP_EVIDENCE_CONTENT.md` for the full methodology and limitations.

No licence is granted for reuse of the included code, model or data unless a licence is added explicitly by the repository owner.
