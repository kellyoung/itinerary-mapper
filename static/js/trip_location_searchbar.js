function tripLocSearch(){
    var input = document.getElementById('trip-loc-search');
    var searchBox = new google.maps.places.SearchBox(input);

    var tripLoc;
    searchBox.addListener('places_changed', function() {
        tripLoc = searchBox.getPlaces()[0];
        console.log(tripLoc);
        if (tripLoc.length === 0) {
          return;
        }
    });

}