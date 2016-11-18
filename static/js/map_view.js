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
        var dayNum = String(results[place].day_num);

        var markerColor;
        switch(results[place].category){
            case 'transport':
                markerColor = '009688';
                break;
            case 'eat':
                markerColor = 'FFC107';
                break;
            case 'explore':
                markerColor = '8BC34A';
                break;
            case 'sleep':
                markerColor = '00BCD4';
                break;
        }

        var marker = new google.maps.Marker({
            map: finalMap,
            place: {
            location: latLng,
            query: results[place].place_loc

            },

            title: results[place].title,
            
            // position: latLng,
            content: content,
            icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=' +
                  dayNum + '|' + markerColor + '|000000'
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

