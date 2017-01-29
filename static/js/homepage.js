
$('#login-form').submit(function(event){
    

    var nameCheck = /^[a-z0-9]+$/.test($('#login-name').val()); //alphanumeric check
    var pwCheck = /^[\x00-\x7F]*$/.test($('#login-pw').val()); //ascii check

    if (nameCheck && pwCheck){
        return;
    }
    
    // give some feedback if it's not right entry
    console.log('not valid');
    event.preventDefault();

});

$('#create-form').submit(function(event){
    var usernameCheck = /^[a-z0-9]+$/.test($('#create-uname').val()); //alphanumeric
    var pwCheck = /^[\x00-\x7F]*$/.test($('#create-pw').val()); //ascii check
    var nameCheck = /^[\x00-\x7F]*$/.test($('#create-name').val()); //ascii check

    if (nameCheck && pwCheck && usernameCheck){
        return;
    }

    console.log('not valid');
    event.preventDefault();

});