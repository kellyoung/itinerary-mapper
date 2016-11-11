function publishTrip(evt){
    evt.preventDefault();
    var params = {'trip_id': $('#publish_trip_id').val()};
    
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

