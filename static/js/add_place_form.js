var addFormMap;
var addFormPlace;
var formMapBounds;
var currentCenter;



function displayAddForm(){
    var params = {
                  'trip_id': $('#trip_id').val()
               };

    $.get('/trip_loc_info.json', params, function(results){

        var formLat = results.latitude;
        var formLong = results.longitude;
        var formViewPort = JSON.parse(results.viewport);

        console.log(formViewPort);


        if (formViewPort){
            formMapBounds = new google.maps.LatLngBounds(
                           new google.maps.LatLng(formViewPort.south, formViewPort.west),
                           new google.maps.LatLng(formViewPort.north, formViewPort.east)
                         );
        }

        addFormMap = new google.maps.Map(document.getElementById('add-form-map'), {
                                    center: {lat: formLat, lng: formLong },
                                    zoom: 5,
                                    mapTypeControl: false,
                                    
                                    streetViewControl: false
                                  });
        if (formMapBounds){
            addFormMap.fitBounds(formMapBounds);
        }

        var form_search = document.getElementById('add-form-search');
        var formSearchBox = new google.maps.places.SearchBox(form_search);

        // Bias the SearchBox results towards current map's viewport.
          addFormMap.addListener('bounds_changed', function() {
            formSearchBox.setBounds(addFormMap.getBounds());
          });

          
          var addFormMarkers = [];
          // Listen for the event fired when the user selects a prediction and retrieve
          // more details for that place.
          formSearchBox.addListener('places_changed', function() {
            addFormPlace = formSearchBox.getPlaces()[0];
            console.log(addFormPlace);
            if (addFormPlace.length === 0) {
              return;
            }

          
            // Clear out the old markers.
            addFormMarkers.forEach(function(marker) {
              marker.setMap(null);
            });
            
            addFormMarkers = [];

            var bounds = new google.maps.LatLngBounds();

            addFormMarkers.push(new google.maps.Marker({
              map: addFormMap,
              title: addFormPlace.name,
              position: addFormPlace.geometry.location
            }));

            if (addFormPlace.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(addFormPlace.geometry.viewport);
            } else {
                bounds.extend(addFormPlace.geometry.location);
            }
            addFormMap.fitBounds(bounds);
          });
            
          console.log(addFormPlace);

    

    });
}