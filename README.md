#JourneyTeller

![](https://github.com/kellyoung/itinerary-mapper/blob/post-hackbright/readme-pics/mapview.png?raw=true "Map View Image")

##### Deployed Site: http://journey-teller.herokuapp.com<br>

JourneyTeller is an interactive tool where users construct their travel stories as a map. The map medium allows users to create a streamlined, informative, and engaging travel narrative to share with friends and family. In the application, users create trips and store places in it. Each place stores user-entered information such as notes, a photo, and geographic data (via Google Places API). Once places are added, a dynamic map is generated with all of the trip's places as markers on the map. Viewers of the map can learn about the user's travels by clicking on the markers for more information. They can also view a collage view of the pictures from the trip.

## Table of Contents
* [Technologies](#technologies)
* [Features](#features)

## <a name="technologies"></a>Technologies
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy<br>
__Frontend:__ Javascript, jQuery, AJAX, Bootstrap<br>
__APIs:__ Google Places API, Google Maps JavaScript API, Imgur API<br>
__Deployment:__ Heroku<br>

## <a name="features"></a>Features
To begin using the app, the user must log in or create an account. The passwords are hashed with bcrypt before they are stored in the database.
![](https://github.com/kellyoung/itinerary-mapper/blob/post-hackbright/readme-pics/homepage.png?raw=true "Homepage Image")
Once a user creates an account or logs in, they can create a trip. The trip takes in a name, a location, a start date, and
an end date. The Google Places API is used to get the geographic bounds of the place selected by the user.
![](https://github.com/kellyoung/itinerary-mapper/blob/post-hackbright/readme-pics/createtrip.png?raw=true "Create Trip Image")