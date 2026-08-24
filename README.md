# External Travel Signals Explorer


An exploratory destination-intelligence project developed by Anna Claire Breuss-Burgess during a Navigator internship. It investigates whether external online signals can help non-technical digital marketing stakeholders understand travel interest in four case-study destinations:


- Marrakech
- Hanoi
- Lisbon
- Reykjavik


## Explore the web app


**[Open the deployed External Travel Signals Explorer](https://external-travel-signals-explorer-app.streamlit.app/)**


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
