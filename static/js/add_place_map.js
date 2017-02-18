
// bad naming of file but basically the page with all the functionalities being
// executed in my google maps API callback function


window.tripPageMaps = function(){
  convertUTF();

  //addPlaceToDB in add_new_place.js
  $('#add-trip-form').on('submit', addPlaceToDB);
  
  //open edit form modal, displayForm in edit_form.js
  $(document).on('click', '.edit-btn', displayForm);

  // open add place modal and show map
  $(document).on('click', '#add-btn', displayAddForm);

  //delete place that is clicked, sendDeleteInfo from edit_form.js
  $('#delete-place-btn').on('click', sendDeleteInfo);

  //edit place on click, sendEditInfo from edit_form.js
  $('#edit-place-btn').on('click', sendEditInfo);

  //toggle trip to be public or private. publishTrip from trip_page.js
  $('#publish-btn').on('click', publishTrip);

  //deletes trip. deleteTrip from trip_page.js
  $('#delete-trip-btn').on('click', deleteTrip);

   $("#addModal").on("shown.bs.modal", function () {
      currentCenter = addFormMap.getCenter();
      console.log(currentCenter);
      google.maps.event.trigger(addFormMap, "resize");
      addFormMap.setCenter(currentCenter);
      addFormMap.fitBounds(formMapBounds);
  });

  $("#editModal").on("shown.bs.modal", function () {
      var currentCenter = editMap.getCenter();
      google.maps.event.trigger(editMap, "resize");
      editMap.setCenter(currentCenter);
  });
};




