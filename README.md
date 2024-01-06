# Relohelper

**Architecture of the project**
![architecture](./docs/images/architecture.png)

**Content**
- [Scraping](#Scraping)
- [Storage](#Storage)
- [Airflow](#Airflow)
- [FastAPI](#FastAPI)
- [Tableau](#Tableau)
- [Benefits](#What-are-the-benefits)

### Scraping
To help with choosing a city (country) for relocation, I've collected in one place data on the cost of living in major cities of the world from the [Numbeo Index](https://www.numbeo.com/cost-of-living/rankings_current.jsp), climate ([Weather Atlas](https://www.weather-atlas.com/)) and various indices ([Numbeo](https://www.numbeo.com/cost-of-living/) & [Legatum](https://www.prosperity.com/rankings)).

### Storage
All scraped data is stored in the PostgresQL in the **RELOHELPER** DB.
Here is the ER-diagram.
![relohelper_db](./docs/images/relohelper_db.png)

Here is the ER-diagram of **SECURITY** DB which stores FastAPI user data.
<img src="./docs/images/security_db.png" width="600">

### Airflow
Also, I added the ability to select 5 currencies. The exchange rate is updated every day by Airflow.

### FastAPI
Thanks to FastAPI you have the opportunity to receive collected information on a single city or country in JSON format. To get more data, you need to register on [relohelper.space](http://relohelper.space/docs) and confirm your email (check your spam folder).

### Tableau
Users can view the dashboard on [Tableau Public](https://public.tableau.com/app/profile/smagindenis/viz/relohelper/Dashboard1#1).
Tableau dashboard screenshot.
![dashboard.jpg](./docs/images/dashboard.jpg)

### What are the benefits:
- General - everything in one place on one dashboard or one JSON.
- Numbeo Cost of Living - possibility to compare more than ten cities simultaneously + visual part
- Numbeo Indices - you can get confused and a lot scattered on the site. Now everything is in one place + visual component helps to understand which index is good and which is bad.
- Climate - you couldn't compare cities with each other at all. Now you can.
- Legatum Index - a good table on the site, but there is no way to track changes over the years in dynamics. I have this.











