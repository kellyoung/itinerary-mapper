var placeLocs = [];
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

//function to try decoding/encoding utf-8
function convertUTF(){
    $(".utf-8").each(function(){ placeLocs.push($(this).text());});

    $('.utf-8').each(function(){
        var decoded = decode_utf8($(this).text());
        console.log(decoded);
        $(this).html(decoded);
    });
    // decode_utf8($('.utf-8').html());
    // unicodeTest = $('.utf-8').html();
}