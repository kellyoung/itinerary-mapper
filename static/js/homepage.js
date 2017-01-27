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
    event.preventDefault();
    var validChars = /([a-z])([0-9])/;
    var validEntry = true;
    $("#login-form input[type=text]").each(function() {
        // if (! $(this).val().value.match(validChars)){
        //     validEntry = false;
        // }
        // validEntry =  /^[\x00-\x7F]*$/.test($(this.val()));
        console.log($(this).val());
    });
    console.log(validEntry);
    if (validEntry) {
        alert('valid!');
        return;
    }

    alert('NOT VALID!');

});