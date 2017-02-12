function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
}

function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}

//function to try decoding/encoding utf-8
function convertUTF(){
    $('.utf-8').each(function(){
        var decoded = decode_utf8($(this).text());
        $(this).html(decoded);
    });
}

var tripLoc;
function tripLocSearch(){
    var input = document.getElementById('trip-loc-search');
    var searchBox = new google.maps.places.SearchBox(input);

    
    searchBox.addListener('places_changed', function() {
        tripLoc = searchBox.getPlaces()[0];
        console.log(tripLoc);
        if (tripLoc.length === 0) {
          return;

        }
    });
}

function addTriptoDB(evt){
    evt.preventDefault();
    if(!tripLoc || !tripLoc.geometry.viewport){
       console.log('choose a valid location');
        return false;
    }
    else{
        var latitude = tripLoc.geometry.location.lat();
        var longitude = tripLoc.geometry.location.lng();
        var tripAddress = tripLoc.formatted_address;
        var tripName = encode_utf8($('#tripname').val());
        var toDate = $('#to').val();
        var fromDate = $('#from').val();
        console.log(tripLoc.geometry.viewport);
        var viewPort = JSON.stringify(tripLoc.geometry.viewport.toJSON());
        
        var params = {
            'tripname': tripName,
            'from': fromDate,
            'to': toDate,
            'latitude': latitude,
            'longitude': longitude,
            'viewport': viewPort,
            'loc-name': tripAddress
        };

        console.log(params);
        $.post('/create_trip.json', params, function(results){
            console.log(results.status);
            window.location.replace("/create_trip/" + results.username +
                                    "/" + results.trip_id);
        });
    }
    
}
$('#create-trip').on('submit', addTriptoDB);

//show and hide form
$('#show-form-btn').hide();

$('#hide-form-btn').on('click', function(){
    $('#create-trip').hide();
    $('#show-form-btn').show();
});

$('#show-form-btn').on('click', function(){
    $('#create-trip').show();
    $('#show-form-btn').hide();
});

// run on load
convertUTF();