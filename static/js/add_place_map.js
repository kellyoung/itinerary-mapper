
// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search 
// will return the first place it finds.
// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

function initAutocomplete() {
  var map = new google.maps.Map(document.getElementById('placemap'), {
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

  var markers = [];

  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    var place = searchBox.getPlaces()[0];
    console.log(place);
    if (place.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach(function(marker) {
      marker.setMap(null);
    });

    var bounds = new google.maps.LatLngBounds();
    var icon = {
      url: 'http://maps.google.com/mapfiles/ms/icons/red.png',
      size: new google.maps.Size(71, 71),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(17, 34),
      scaledSize: new google.maps.Size(25, 25)
    };

    new google.maps.Marker({
      map: map,
      icon: icon,
      title: place.name,
      position: place.geometry.location
    });

    if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
    } else {
        bounds.extend(place.geometry.location);
    }
    map.fitBounds(bounds);

  });
}
