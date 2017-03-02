
 

var editPlace;
var editMap;
var editFormParams;
function displayForm(){
    var parentDiv = $(this).parent();
    
    parentDiv = parentDiv.parent().parent().parent();

    var divPlaceID = parentDiv.attr('id').split('-')[2];
    
    editFormParams = {
        'place_id': divPlaceID
    };

    $.get('/edit_place_info.json', editFormParams, function(results){
        $("#edit-place_id").val(divPlaceID);
        $("#edit-placename").val(decode_utf8(results.place_name));
        $("#edit-place-search").val(decode_utf8(results.place_loc));
        $("#edit-tripnotes").val(decode_utf8(results.notes));

        var selectedDate = '#edit-tripday option[value="'+results.day_num+','+results.formatted_date+'"]';
        $(selectedDate).prop("selected", "selected");

        var selectedCategory = '#edit-tripcat option[value="'+results.cat_id+'"]';
        $(selectedCategory).prop("selected", "selected");

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
            editSearchBox.setBounds(editMap.getBounds());
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
    console.log(delete_place_id);
    var deletePlaceParams = {
        'place_id': delete_place_id
    };

    $.post('/delete_place.json', deletePlaceParams, function(results){
        console.log(results.status);
        location.reload(true);
    });
}

//send info to server to update place and refresh page
function sendEditInfo(evt){

    evt.preventDefault();
    var form_data = new FormData();

    form_data.append("place_id", $('#edit-place_id').val());
    form_data.append("place_name", encode_utf8($('#edit-placename').val()));
    form_data.append("place_search", encode_utf8($('#edit-place-search').val()));
    form_data.append("visit_day", $('#edit-tripday').val());
    form_data.append("category", $('#edit-tripcat').val());
    form_data.append("notes", encode_utf8($('#edit-tripnotes').val()));

    // if there is a file upload
    var edit_place_picture = $('#edit-place-pic-file')[0].files[0];
    // console.log(edit_place_picture);

    if(edit_place_picture){
        // form_data.append('pic', edit_place_picture);
        var imgurData = new FormData();
          imgurData.append("image", edit_place_picture);
          $.ajax({
            url: "https://api.imgur.com/3/image",
            type: "POST",
            datatype: "json",
            headers: {
              "Authorization": "Client-ID a8350698449bb9a"
            },
            data: imgurData,
            success: function(response) {
              //console.log(response);
              var photo = response.data.link;
              var photo_hash = response.data.deletehash;
              console.log(photo);
              console.log(typeof(photo));

              form_data.append('pic', photo);

              var delete_pic = $('#delete-file').is(":checked");

                if(delete_pic){
                    form_data.append('delete', 'yes');
                }
                else{
                    form_data.append('delete', 'no');
                }


                //check to see if there was a new place (editPlace), if there is pass in lat and long
                if (editPlace) {
                    form_data.append("latitude", editPlace.geometry.location.lat());
                    form_data.append("longitude", editPlace.geometry.location.lng());
                }

                editPlace = '';

                // if using file upload
                // var editURL = '/edit_place.json';

                // if using image url
                var editURL = '/edit_place.json';


                $.ajax({
                    url: editURL,
                    data: form_data,
                    type: 'POST',
                    // THIS MUST BE DONE FOR FILE UPLOADING
                    contentType: false,
                    processData: false,
                    // ... Other options like success and etc
                    success: function(results){
                        console.log(results.status);
                        location.reload();
                    }
                });

            },
            cache: false,
            contentType: false,
            processData: false
          });
          
                    
    }
    else{
        var delete_pic = $('#delete-file').is(":checked");

        if(delete_pic){
            form_data.append('delete', 'yes');
        }
        else{
            form_data.append('delete', 'no');
        }


        //check to see if there was a new place (editPlace), if there is pass in lat and long
        if (editPlace) {
            form_data.append("latitude", editPlace.geometry.location.lat());
            form_data.append("longitude", editPlace.geometry.location.lng());
        }

        editPlace = '';

        // if using file upload
        // var editURL = '/edit_place.json';

        // if using image url
        var editURL = '/edit_place.json';


        $.ajax({
            url: editURL,
            data: form_data,
            type: 'POST',
            // THIS MUST BE DONE FOR FILE UPLOADING
            contentType: false,
            processData: false,
            // ... Other options like success and etc
            success: function(results){
                console.log(results.status);
                location.reload();
            }
        });
        }

        // if there is an image url
        // if ($('#edit-place-pic-link').val()){
        //     form_data.append("img_url", encode_utf8($('#edit-place-pic-link').val()));
        // }

        
}


