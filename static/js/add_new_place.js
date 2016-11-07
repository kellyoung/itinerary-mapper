//need place from add_place_map.js

//add a place
var add_place_params;
function addPlace(evt) {
    evt.preventDefault();

    
    var day_info = $('#tripday').val().split(',');

    add_place_params = {
        'trip_id': $('#trip_id').val(),
        'placename': $('#placename').val(),
        'placesearch': addPlace.formatted_address,
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
        $(dayDiv).append(results.new_place_div);
    });
}

$('#add-trip-form').on('submit', addPlace);
