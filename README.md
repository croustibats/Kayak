My email :👉 baptiste.cournault@gmail.com 👈

Video link : 👉 https://share.vidyard.com/watch/esjWMgHC85fyw38em735LQ? 👈




Plan your trip with Kayak
Company's description 📇
Kayak is a travel search engine that helps user plan their next trip at the best price.
The company was founded in 2004 by Steve Hafner & Paul M. English. After a few rounds of fundraising, Kayak was acquired by Booking Holdings which now holds:

Booking.com
Kayak
Priceline
Agoda
RentalCars
OpenTable
With over $300 million revenue a year, Kayak operates in almost all countries and all languages to help their users book travels accros the globe.

Project 🚧
The marketing team needs help on a new project. After doing some user research, the team discovered that 70% of their users who are planning a trip would like to have more information about the destination they are going to.

In addition, user research shows that people tend to be defiant about the information they are reading if they don't know the brand which produced the content.

Therefore, Kayak Marketing Team would like to create an application that will recommend where people should plan their next holidays. The application should be based on real data about:

Weather
Hotels in the area
The application should then be able to recommend the best destinations and hotels based on the above variables at any given time.

Goals 🎯
As the project has just started, your team doesn't have any data that can be used to create this application. Therefore, your job will be to:

Scrape data from destinations
Get weather data from each destination
Get hotels' info about each destination
Store all the information above in a data lake
Extract, transform and load cleaned data from your datalake to a data warehouse
Scope of this project 🖼️
Marketing team wants to focus first on the best cities to travel to in France. According One Week In.com here are the top-35 cities to visit in France:

["Mont Saint Michel",
"St Malo",
"Bayeux",
"Le Havre",
"Rouen",
"Paris",
"Amiens",
"Lille",
"Strasbourg",
"Chateau du Haut Koenigsbourg",
"Colmar",
"Eguisheim",
"Besancon",
"Dijon",
"Annecy",
"Grenoble",
"Lyon",
"Gorges du Verdon",
"Bormes les Mimosas",
"Cassis",
"Marseille",
"Aix en Provence",
"Avignon",
"Uzes",
"Nimes",
"Aigues Mortes",
"Saintes Maries de la mer",
"Collioure",
"Carcassonne",
"Ariege",
"Toulouse",
"Montauban",
"Biarritz",
"Bayonne",
"La Rochelle"]
Your team should focus only on the above cities for your project.

Helpers 🦮
To help you achieve this project, here are a few tips that should help you

Get weather data with an API
Use https://nominatim.org/ to get the gps coordinates of all the cities (no subscription required) Documentation : https://nominatim.org/release-docs/develop/api/Search/

Use https://openweathermap.org/appid (you have to subscribe to get a free apikey) and https://openweathermap.org/api/one-call-api to get some information about the weather for the 35 cities and put it in a DataFrame

Determine the list of cities where the weather will be the nicest within the next 7 days For example, you can use the values of daily.pop and daily.rain to compute the expected volume of rain within the next 7 days... But it's only an example, actually you can have different opinions on a what a nice weather would be like 😎 Maybe the most important criterion for you is the temperature or humidity, so feel free to change the rules !

Save all the results in a .csv file, you will use it later 😉 You can save all the informations that seem important to you ! Don't forget to save the name of the cities, and also to create a column containing a unique identifier (id) of each city (this is important for what's next in the project)

Use plotly to display the best destinations on a map

Scrape Booking.com
Since BookingHoldings doesn't have aggregated databases, it will be much faster to scrape data directly from booking.com

You can scrap as many information asyou want, but we suggest that you get at least:

hotel name,
Url to its booking.com page,
Its coordinates: latitude and longitude
Score given by the website users
Text description of the hotel
Create your data lake using S3
Once you managed to build your dataset, you should store into S3 as a csv file.

ETL
Once you uploaded your data onto S3, it will be better for the next data analysis team to extract clean data directly from a Data Warehouse. Therefore, create a SQL Database using AWS RDS, extract your data from S3 and store it in your newly created DB.
