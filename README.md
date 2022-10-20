# Relohelper project

You can see the final dashboard at [Tableau Public](https://public.tableau.com/app/profile/smagindenis/viz/relohelper/Dashboard1#1)

To help with choosing a city (country) for relocation, I've collected in one place data on the cost of living in major cities of the world from the [Numbeo Index](https://www.numbeo.com/cost-of-living/rankings_current.jsp), climate ([Weather Atlas](https://www.weather-atlas.com/)) and various indices ([Numbeo](https://www.numbeo.com/cost-of-living/) & [Legatum](https://www.prosperity.com/rankings)) with the ability to visually compare over 10 cities simultaneously. For this, I created an ETL process and displayed the indexes in Tableau. The architecture of this solution is shown below.

![architecture](./images/architecture.png)

Also I added the ability to select 5 currencies. The exchange rate is updated every day.

There are 2 roles involved in project creation: data engineer and analyst, who works in Jupyter Notebook.
DE creates a Jupyter kernel on the VPS and gives a token to the analyst for access.
The analyst analyzes the cities in the Numbeo Index, removes unnecessary data, and creates master tables for further scraping, which the DE performs. The analyst also gets read access to the final database to do SQL Ad-Hoc queries.

Users can view the dashboard on [Tableau Public](https://public.tableau.com/app/profile/smagindenis/viz/relohelper/Dashboard1#1).

In the future, I plan to buy a VPS, install the Tableau Server, and host [relohelper.online](http://relohelper.online/). In the 'live mode' is already set up automatic exchange rate updates from the database, which is updated once a day by Airflow.


ER-diagram:

![er_diagram](./images/er-diagram.png)

Tableau dashboard screenshot:

![dashboard](./images/dashboard.jpg)


P.S. This is a training project, so I practiced scraping and didn't get the API data.

What are the benefits:
- General - everything in one place on one page.
- Numbeo Cost of Living - possibility to compare more than ten cities simultaneously + visual part
- Numbeo Indices - you can get confused and a lot scattered on the site. Now everything is in one place + visual component helps to understand which index is good and which is bad.
- Climate - you couldn't compare cities with each other at all. Now you can.
- Legatum Index - a good table on the site, but there is no way to track changes over the years in dynamics. I have this.