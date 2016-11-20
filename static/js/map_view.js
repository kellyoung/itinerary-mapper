var finalMap;
var placesLatLng=[];
function allPlacesControl(controlDiv, map, bounds) {
    // Set CSS for the control border.
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.border = '2px solid #fff';
    controlUI.style.borderRadius = '0px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '10px';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Click to see all Places';
    controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(25,25,25)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '24px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.innerHTML = 'All Places';
    controlUI.appendChild(controlText);

    // Setup the click event listeners: simply set the map to Chicago.
    controlUI.addEventListener('click', function() {
        var latlngbounds = new google.maps.LatLngBounds();
        for (var i = 0; i < bounds.length; i++) {
            latlngbounds.extend(placesLatLng[i]);
        }
        finalMap.fitBounds(latlngbounds);
    });
    // console.log('control button!!!');

}
window.createAllPlacesMap = function(results){
    console.log(results);

    finalMap = new google.maps.Map(document.getElementById("final-map"), {
                center: new google.maps.LatLng(0, 0),
                zoom: 0,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            });
    
    for(var place in results){
        var latLng = new google.maps.LatLng(results[place].latitude, results[place].longitude);
        placesLatLng.push(latLng);

        var content = results[place].content;
        var dayNum = String(results[place].day_num);

        var markerColor;
        switch(results[place].category){
            case 'transport':
                markerColor = '0C9FF9';
                break;
            case 'eat':
                markerColor = 'FF8B29';
                break;
            case 'explore':
                markerColor = '8BC34A';
                break;
            case 'sleep':
                markerColor = 'FF3891';
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

    var allPlacesControlDiv = document.createElement('div');
    var allPlacesButton  = new allPlacesControl(allPlacesControlDiv, finalMap, placesLatLng);

    allPlacesControlDiv.index = 5;
    finalMap.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(allPlacesControlDiv);

};

function mapPlaces(){
    var params = {'trip_id': $('#map-trip_id').val()};
    $.get('/places_to_map.json', params, createAllPlacesMap);
}

$(document).ready(mapPlaces);

