//need place from add_place_map.js


//add a place
var add_place_params;

function addPlaceToDB(evt) {
    evt.preventDefault();

    

    var form_data = new FormData();
    var day_info = $('#tripday').val().split(',');
    var place_picture = $('input[type=file]')[0].files[0];
    if (addFormPlace){
        // $('#addModal').modal('hide');
        form_data.append("trip_id", $('#trip_id').val());
        form_data.append("placename", encode_utf8($('#placename').val()));
        form_data.append("placesearch", encode_utf8(addFormPlace.formatted_address));
        form_data.append("latitude", addFormPlace.geometry.location.lat());
        form_data.append("longitude", addFormPlace.geometry.location.lng());
        form_data.append("visitday", day_info[1]);
        form_data.append("daynum", day_info[0]);
        form_data.append("category", $('#tripcat').val());
        form_data.append("notes", encode_utf8($('#tripnotes').val()));

        // this is for if I use picture upload
        if(place_picture){
            
            var imgurData = new FormData();
          imgurData.append("image", place_picture);
          $.ajax({
            url: "https://api.imgur.com/3/image",
            type: "POST",
            datatype: "json",
            headers: {
              "Authorization": "Client-ID a8350698449bb9a"
            },
            data: imgurData,
            success: function(response) {
              //console.log(response);
              var photo = response.data.link;
              var photo_hash = response.data.deletehash;
              console.log(photo);
              console.log(typeof(photo));

              form_data.append('pic', photo);

              var ajax_url = '/add_place_no_upload.json';
                $.ajax({
                    url: ajax_url,
                    data: form_data,
                    type: 'POST',
                    // THIS MUST BE DONE FOR FILE UPLOADING
                    contentType: false,
                    processData: false,
                    // ... Other options like success and etc
                    success: function(results){

                        location.reload();
                    }
                });

            },
            cache: false,
            contentType: false,
            processData: false
          });
        }
        else{
            var ajax_url = '/add_place_no_upload.json';
                $.ajax({
                    url: ajax_url,
                    data: form_data,
                    type: 'POST',
                    // THIS MUST BE DONE FOR FILE UPLOADING
                    contentType: false,
                    processData: false,
                    // ... Other options like success and etc
                    success: function(results){

                        location.reload();
                    }
                });
        }

        // for deployment switch it to a url link
        // if ($('#place-pic-link').val()){
        //     form_data.append("img_link", encode_utf8($('#place-pic-link').val()));
        // }
        
        

        $( '#add-trip-form' ).each(function(){
            this.reset();
        });

        // url for file upload
        // var ajax_url = '/add_place.json';

        
    }
    else {
        console.log('needs a valid place');
        $('#invalid-place').html('Invalid Place. Please try again.');
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


