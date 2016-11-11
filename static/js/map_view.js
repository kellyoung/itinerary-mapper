function createAllPlacesMap(results){
    console.log(results);

    var finalMap = new google.maps.Map(document.getElementById("final-map"), {
                center: new google.maps.LatLng(0, 0),
                zoom: 0,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            });

    var placesLatLng=[];


    for(var place in results){
        var latLng = new google.maps.LatLng(results[place].latitude, results[place].longitude);
        placesLatLng.push(latLng);

        var content = results[place].content;

        var marker = new google.maps.Marker({
            map: finalMap,
            title: results[place].title,
            position: latLng,
            content: content,
            label: String(results[place].day_num)
        });

        var infowindow = new google.maps.InfoWindow();

        google.maps.event.addListener(marker, 'click', function () {
                                infowindow.setContent(this.content);
                                infowindow.open(this.getMap(), this);
                            });
    }

    var latlngbounds = new google.maps.LatLngBounds();
    for (var i = 0; i < placesLatLng.length; i++) {
        latlngbounds.extend(placesLatLng[i]);
    }
    finalMap.fitBounds(latlngbounds);
    
}

function mapPlaces(){
    var params = {'trip_id': $('#map-trip_id').val()};
    $.get('/places_to_map.json', params, createAllPlacesMap);
}

$(document).ready(mapPlaces);