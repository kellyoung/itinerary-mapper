function publishTrip(evt){
    evt.preventDefault();
    var params = {'trip_id': $('#trip_id').val()};
    
    $.post('/publish_trip.json', params, function(results){
        console.log(results.status);
        if (results.status){
            $('#publish-btn').text('Make Trip Private');
        }
        else{
            $('#publish-btn').text('Make Trip Public');
        }
    });
}

// to be executed in add_place_map, to stay consistent
function deleteTrip(){
    var params = {'trip_id': $('#trip_id').val()};

    $.post('/delete_trip.json', params, function(results){
        console.log(results.status);
        window.location.replace("/" + results.username +
                                "/trips");
    });
}