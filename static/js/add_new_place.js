//need place from add_place_map.js

//if I want to work on encoding to utf8 and sending to database
function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
}

function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}
//add a place
var add_place_params;
function addPlaceToDB(evt) {
    evt.preventDefault();

    
    var day_info = $('#tripday').val().split(',');

    add_place_params = {
        'trip_id': $('#trip_id').val(),
        'placename': $('#placename').val(),
        'placesearch': encode_utf8(addPlace.formatted_address),
        'latitude': addPlace.geometry.location.lat(),
        'longitude': addPlace.geometry.location.lng(),
        'visitday': day_info[1],
        'daynum': day_info[0],
        'category': $('#tripcat').val(),
        'notes': $('#tripnotes').val()
    };

    $( '#add-trip-form' ).each(function(){
        this.reset();
    });


    var dayDiv = '#day-'+add_place_params.daynum;
    var place_id;
    $.post('/add_place.json', add_place_params, function(results){
        //test what place_loc looks like on its own
        console.log(decode_utf8(results.place_loc));
        $(dayDiv).append(decode_utf8(results.new_place_div));

    });
}

