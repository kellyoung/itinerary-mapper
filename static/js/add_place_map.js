
// bad naming of file but basically the page with all the functionalities being
// executed in my google maps API callback function
var addPlace;
var editPlace;
var editMap;
var addMap;
var tripViewPort;


function tripPageMaps() {

  //requests trip map info and uses it to display Google Maps
  addPlaceMapInfo();

  //addPlaceToDB in add_new_place.js
  $('#add-trip-form').on('submit', addPlaceToDB);
  
  //open edit form modal, displayForm in edit_form.js
  $(document).on('click', '.edit-btn', displayForm);

  //delete place that is clicked, sendDeleteInfo from edit_form.js
  $('#delete-place-btn').on('click', sendDeleteInfo);

  //edit place on click, sendEditInfo from edit_form.js
  $('#edit-place-btn').on('click', sendEditInfo);

  //toggle trip to be public or private. publishTrip from trip_page.js
  $('#publish-btn').on('click', publishTrip);
}

function addPlaceMapInfo(){
  var tripLat;
  var tripLong;
  //AJAX request to get map bounds and latitude and longitude from database
  var params = {
                  'trip_id': $('#trip_id').val()
               };

  $.get('/trip_loc_info.json', params, function(results){
    console.log(results);
    tripLat = results.latitude;
    tripLong = results.longitude;
    tripViewPort = JSON.parse(results.viewport);

    console.log(tripViewPort);
    console.log(tripLat);
    console.log(tripLong);
    //call addPlaceFormMap with the parameters
    addPlaceFormMap(tripLat, tripLong, tripViewPort);

  });
  
}

function addPlaceFormMap(latitude, longitude, viewport){
  var addMapBounds;
  if (viewport){
    addMapBounds = new google.maps.LatLngBounds(
                        new google.maps.LatLng(viewport.south, viewport.west),
                        new google.maps.LatLng(viewport.north, viewport.east)
                      );
  }
  

  addMap = new google.maps.Map(document.getElementById('placemap'), {
    center: {lat: latitude, lng: longitude},
    zoom: 3,
    mapTypeControl: false,
    
    streetViewControl: false
  });

  if (addMapBounds){
    addMap.fitBounds(addMapBounds);
  }
  
  // Create the search box and link it to the UI element.
  var input = document.getElementById('place-search');
  var searchBox = new google.maps.places.SearchBox(input);


  // Bias the SearchBox results towards current map's viewport.
  addMap.addListener('bounds_changed', function() {
    searchBox.setBounds(addMap.getBounds());
  });

  
  var addMarkers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    addPlace = searchBox.getPlaces()[0];
    console.log(addPlace);
    if (addPlace.length === 0) {
      return;
    }

  
    // Clear out the old markers.
    addMarkers.forEach(function(marker) {
      marker.setMap(null);
    });
    
    addMarkers = [];

    var bounds = new google.maps.LatLngBounds();

    addMarkers.push(new google.maps.Marker({
      map: addMap,
      title: addPlace.name,
      position: addPlace.geometry.location
    }));

    if (addPlace.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(addPlace.geometry.viewport);
    } else {
        bounds.extend(addPlace.geometry.location);
    }
    addMap.fitBounds(bounds);
  });
    
  console.log(addPlace);
}