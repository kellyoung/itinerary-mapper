//need place from add_place_map.js

//add a place
function addPlace(evt) {
    evt.preventDefault();

    // TODO: show the result message after your form
    // TODO: if the result code is ERROR, make it show up in red (see our CSS!)
    var day_info = $('#tripday').val().split(',');

    var params = {
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
    console.log(params);

    $( '#add-trip-form' ).each(function(){
        this.reset();
    });
    var dayDiv = '#day-'+params.daynum;
    $.post('/add_place.json', params, function(results){
        console.log(dayDiv);
        $(dayDiv).append(results.new_div);
    });
}

$('#add-trip-form').on('submit', addPlace);
