//need place from add_place_map.js

//add a place
var params;
function addPlace(evt) {
    evt.preventDefault();

    
    var day_info = $('#tripday').val().split(',');

    params = {
        'trip_id': $('#trip_id').val(),
        'placename': $('#placename').val(),
        'placesearch': place.formatted_address,
        'latitude': place.geometry.location.lat(),
        'longitude': place.geometry.location.lng(),
        'visitday': day_info[1],
        'daynum': day_info[0],
        'category': $('#tripcat').val(),
        'notes': $('#tripnotes').val()
    };

    $( '#add-trip-form' ).each(function(){
        this.reset();
    });


    var dayDiv = '#day-'+params.daynum;
    var place_id;
    $.post('/add_place.json', params, function(results){
        console.log(results.place_id);
        console.log(results.new_place_div);
        $(dayDiv).append(results.new_place_div);
    });
}

$('#add-trip-form').on('submit', addPlace);
