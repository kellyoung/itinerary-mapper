 $("#editModal").on("shown.bs.modal", function () {
    var currentCenter = editMap.getCenter();
    google.maps.event.trigger(editMap, "resize");
    editMap.setCenter(currentCenter);
});


var editFormParams;
function displayForm(){
    var parentDiv = $(this).parent();
    var divPlaceID = parentDiv.attr('id').split('-')[2];
    
    editFormParams = {
        'place_id': divPlaceID
    };

    $.get('/edit_place_info.json', editFormParams, function(results){
        $("#edit-place_id").val(divPlaceID);
        $("#edit-placename").val(results.place_name);
        $("#edit-place-search").val(results.place_loc);
        $("#edit-tripnotes").val(results.notes);

        var selectedDate = '#edit-tripday option[value="'+results.day_num+','+results.formatted_date+'"]';
        $(selectedDate).attr("selected", "selected");

        var selectedCategory = '#edit-tripcat option[value="'+results.cat_id+'"]';
        $(selectedCategory).attr("selected", "selected");

        var icon = {
          url: 'http://maps.google.com/mapfiles/ms/icons/red.png',
          size: new google.maps.Size(71, 71),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(17, 34),
          scaledSize: new google.maps.Size(25, 25)
        };

        var editMarkers = [];

        var latLng = {lat: results.latitude, lng: results.longitude};

        editMap = new google.maps.Map(document.getElementById('edit-placemap'), {
            center: latLng,
            zoom: 18,
            mapTypeControl: false,
            
            streetViewControl: false
        });

        var editMarker = new google.maps.Marker({
          position: latLng,
          map: editMap,
          title: 'Hello World!',
          visible: true
        });

        editMarkers.push(editMarker);

        var editInput = document.getElementById('edit-place-search');
        var editSearchBox = new google.maps.places.SearchBox(editInput);

          

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
            });
    
}

//send info to server to delete place and refresh page
function sendDeleteInfo(){
    var delete_place_id = $("#edit-place_id").val();
    var deletePlaceParams = {
        place_id: delete_place_id
    };

    $.post('/delete_place.json', deletePlaceParams, function(results){
        console.log(results.status);
        location.reload();
    });
}

//send info to server to update place and refresh page
function sendEditInfo(evt){
    evt.preventDefault();
    var place_id = $('#edit-place_id').val();
    var place_name = $('#edit-placename').val();
    var place_search = $('#edit-place-search').val();
    var visit_day = $('#edit-tripday').val();
    var category = $('#edit-tripcat').val();
    var notes = $('#edit-tripnotes').val();

    var editPlaceParams = {
        place_id: place_id,
        place_name: place_name,
        place_search: place_search,
        visit_day: visit_day,
        category: category,
        notes: notes
    };

    //check to see if there was a new place (editPlace), if there is pass in lat and long
    if (editPlace) {
        editPlaceParams.latitude = editPlace.geometry.location.lat();
        editPlaceParams.longitude = editPlace.geometry.location.lng();
    }
    editPlace = '';
    console.log(editPlaceParams);
    $.post('/edit_place.json', editPlaceParams, function(results){
        console.log(results.status);
        location.reload();
    });
}

$('#edit-place-btn').on('click', sendEditInfo);

