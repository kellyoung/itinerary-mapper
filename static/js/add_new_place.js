//need place from add_place_map.js

//if I want to work on encoding to utf8 and sending to database
function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
}

function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}
//add a place
var add_place_params;

function addPlaceToDB(evt) {
    evt.preventDefault();

    var form_data = new FormData();
    var day_info = $('#tripday').val().split(',');
    var place_picture = $('input[type=file]')[0].files[0];
    if (addPlace){
        form_data.append("trip_id", $('#trip_id').val());
        form_data.append("placename", encode_utf8($('#placename').val()));
        form_data.append("placesearch", encode_utf8(addPlace.formatted_address));
        form_data.append("latitude", addPlace.geometry.location.lat());
        form_data.append("longitude", addPlace.geometry.location.lng());
        form_data.append("visitday", day_info[1]);
        form_data.append("daynum", day_info[0]);
        form_data.append("category", $('#tripcat').val());
        form_data.append("notes", encode_utf8($('#tripnotes').val()));

        if(place_picture){
            form_data.append('pic', place_picture);
        }
        

        $( '#add-trip-form' ).each(function(){
            this.reset();
        });

        var dayDiv = '#day-'+day_info[0];
        var place_id;

        $.ajax({
            url: '/add_place.json',
            data: form_data,
            type: 'POST',
            // THIS MUST BE DONE FOR FILE UPLOADING
            contentType: false,
            processData: false,
            // ... Other options like success and etc
            success: function(results){

                $(dayDiv).append(decode_utf8(results.new_place_div));
            }
        });
    }
    else {
        console.log('needs a valid place');
        return false;
    }
    
}

//function to handle incorrect file types
function checkFileType(event){
    var ext = this.value.match(/\.(.+)$/)[1];
    switch(ext)
    {
        case 'jpg':
        case 'png':
        case 'jpeg':
        case 'JPG':
        case 'PNG':
            console.log('allowed');
            break;
        default:
            alert('File type not allowed.');
            this.value='';
    }
}
$('#place-pic-file').on('change', checkFileType);
$('#edit-place-pic-file').on('change', checkFileType);

//show and hide add place form_data
$('#show-add-form-btn').hide();

$('#hide-add-form-btn').on('click', function(){
    $('#add-trip-div').hide();
    $('#add-place-row-btns').hide();
    $('#show-add-form-btn').show();
});

$('#show-add-form-btn').on('click', function(){
    $('#add-trip-div').show();
    $('#add-place-row-btns').show();
    $('#show-add-form-btn').hide();
});
