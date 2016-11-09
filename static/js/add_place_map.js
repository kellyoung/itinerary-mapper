
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

  //addPlaceToDB in add_new_place.js
  $('#add-trip-form').on('submit', addPlaceToDB);
  
  //open edit form modal, displayForm in edit_form.js
  $(document).on('click', '.edit-btn', displayForm);

  //delete place that is clicked, sendDeleteInfo from edit_form.js
  $('#delete-place-btn').on('click', sendDeleteInfo);
  
}