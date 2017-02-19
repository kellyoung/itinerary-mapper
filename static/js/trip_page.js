//if I want to work on encoding to utf8 and sending to database
function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
}

function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}

var placeLocs = [];
function publishTrip(evt){
    evt.preventDefault();
    var params = {'trip_id': $('#trip_id').val()};
    
    $.post('/publish_trip.json', params, function(results){
        console.log(results.status);
        if (results.status){
            $('#publish-btn').html('<i class="fa fa-user"></i> &nbsp; MAKE TRIP PRIVATE');
        }
        else{
            $('#publish-btn').html('<i class="fa fa-users"></i> &nbsp; MAKE TRIP PUBLIC');
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

document.onload = function(){
    // console.log(document.title);
    var decoded = decode_utf8(document.title);

    // console.log(decoded);
    document.title = decoded;
};

document.onload();



//function to try decoding/encoding utf-8
function convertUTF(){
    // $(".utf-8").each(function(){ placeLocs.push($(this).text());
                                 
    //                             });

    $('.utf-8').each(function(){
        var decoded = decode_utf8($(this).text());
        $(this).html(decoded);
    });
    // decode_utf8($('.utf-8').html());
    // unicodeTest = $('.utf-8').html();
}