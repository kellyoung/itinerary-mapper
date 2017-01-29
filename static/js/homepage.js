// $('#open-login').on('click', function(){
//     $('#no-sess-forms').html(
//         "<form action='/login' method='POST' class='doc-form' id='login-doc-form'>" +
//             "<label for='username'>Username: </label><br>" +
//             "<input type='text' name='username' class='char-restrict' autocomplete='off'required><br>" +
//             "<label for='password'>Password: </label><br>" +
//             "<input type='password' name='password' autocomplete='off' required><br><br>" +
//             "<input type='submit' value='LOG IN' id='login-doc-submit'>"+
//         "</form>"
//     );
// });

// $('#open-create-acct').on('click', function(){
//     $('#no-sess-forms').html(
//         "<form action='/create_user' method='POST' class='doc-form' id='create-acct-doc-form'>" +
//                     "<label for='name'>Name: </label><br>" +
//                     "<input type='text' name='name' autocomplete='off' required><br>" +
//                     "<label for='username'>Username  (alphanumeric only): </label><br>" +
//                     "<input type='text' name='username' class='char-restrict' autocomplete='off' required><br>" +
//                     "<label for='password'>Password: </label><br>" +
//                     "<input type='password' name='password' autocomplete='off' required><br><br>" +
//                     "<input type='submit' value='CREATE USER' id='create-doc-submit'>" +
//                 "</form>"
//     );
// });

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