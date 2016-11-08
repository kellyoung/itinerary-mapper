
// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search 
// will return the first place it finds.
// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
var addPlace;
var editPlace;
var editMap;
var map;

function initAutocomplete() {
  //first map for add place
  map = new google.maps.Map(document.getElementById('placemap'), {
    center: {lat: -0.0022, lng: -78.4558},
    zoom: 1,
    mapTypeControl: false,
    
    streetViewControl: false
  });


  // Create the search box and link it to the UI element.
  var input = document.getElementById('place-search');
  var searchBox = new google.maps.places.SearchBox(input);


  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
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
    var icon = {
      url: 'http://maps.google.com/mapfiles/ms/icons/red.png',
      size: new google.maps.Size(71, 71),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(17, 34),
      scaledSize: new google.maps.Size(25, 25)
    };

    addMarkers.push(new google.maps.Marker({
      map: map,
      icon: icon,
      title: addPlace.name,
      position: addPlace.geometry.location
    }));

    if (addPlace.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(addPlace.geometry.viewport);
    } else {
        bounds.extend(addPlace.geometry.location);
    }
    map.fitBounds(bounds);
  });
    
  console.log(addPlace);

  //second map for edit place
  editMap = new google.maps.Map(document.getElementById('edit-placemap'), {
    center: {lat: -0.0022, lng: -78.4558},
    zoom: 1,
    mapTypeControl: false,
    
    streetViewControl: false
  });

  var editInput = document.getElementById('edit-place-search');
  var editSearchBox = new google.maps.places.SearchBox(editInput);

  var editMarkers = [];

  editMap.addListener('bounds_changed', function() {
    editSearchBox.setBounds(map.getBounds());
  });

  editSearchBox.addListener('places_changed', function() {
    editPlace = editSearchBox.getPlaces()[0];
    console.log(editPlace);
    if (editPlace.length === 0) {
      return;
    }

    // Clear out the old markers.
    editMarkers.forEach(function(marker) {
      marker.setMap(null);
    });
    
    editMarkers = [];

    var bounds = new google.maps.LatLngBounds();
    var icon = {
      url: 'http://maps.google.com/mapfiles/ms/icons/red.png',
      size: new google.maps.Size(71, 71),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(17, 34),
      scaledSize: new google.maps.Size(25, 25)
    };

    editMarkers.push(new google.maps.Marker({
      map: editMap,
      icon: icon,
      title: editPlace.name,
      position: editPlace.geometry.location
    }));

    if (editPlace.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(editPlace.geometry.viewport);
    } else {
        bounds.extend(editPlace.geometry.location);
    }
    editMap.fitBounds(bounds);
  });
}