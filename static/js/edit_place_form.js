 var editFormParams;
function displayForm(){
    var parentDiv = $(this).parent();
    var divPlaceID = parentDiv.attr('id').split('-')[2];
    console.log(divPlaceID);
    
    editFormParams = {
        'place_id': divPlaceID
    };

    $.get('/edit_place_info.json', editFormParams, function(results){
        $("#edit-place_id").val(divPlaceID);
        $("#edit-placename").val(results.place_name);
        $("#edit-place-search").val(results.place_loc);
        $("#edit-tripnotes").val(results.notes);

        var selectedDate = '#edit-tripday option[value="'+results.day_num+','+results.formatted_date+'"]';
        $(selectedDate).attr("selected", "selected");

        var selectedCategory = '#edit-tripcat option[value="'+results.cat_id+'"]';
        $(selectedCategory).attr("selected", "selected");
    });
    
}


 $('.edit-btn').on('click', displayForm);
