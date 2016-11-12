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
        //pass in lat long to the server to store in db
        $('#create-trip-loc').html("<input type='hidden' name='coordinates' value='" +
                                   tripLoc.geometry.location.lat() + "," +
                                   tripLoc.geometry.location.lng()+ "'>");
        //pass in the location name from Google Places object
        $('#create-trip-loc-name').html("<input type='hidden' name='loc-name' value='" +
                                        tripLoc.formated_address + "'>");
    });



}