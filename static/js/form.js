/*
show step 1 to user
*/
$(document).ready(function() {

    $('#lead_ad_generator_step_1').on('click', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val(),
                headline : $('#headline').val(),
                text : $('#text').val(),
                //image : $('#image').val(),
                privacy_policy : $('#privacy_policy').val(),
                url : $('#url').val(),
                budget : $('#budget').val(),
            },
            type : 'POST', // type of request to send
            url : '/get_preview' // url to send data to
        })
        .done(function(data) {
            $('#lead_ad_generator_form_2').hide();
            $('#lead_ad_generator_form_3').hide();
            $('#lead_ad_generator_form_1').show();
            $('#publish_lead_ad_button_div').hide();
            //$('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
        });

        event.preventDefault();

    });

});

/*
update iFrame based on users selections from step 1
*/
$(document).ready(function() {

    // send user selected 'ad_account' and 'page' to /lead_ad_generator_1 and pass iframe with default variables
    $('.lead_ad_generator_form_1').on('change', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val(),
                headline : $('#headline').val(),
                text : $('#text').val(),
                //image : $('#image').val(),
                privacy_policy : $('#privacy_policy').val(),
                url : $('#url').val(),
                budget : $('#budget').val(),
            },
            type : 'POST', // type of request to send
            url : '/get_preview' // url to send data to
        })
        .done(function(data) {
            //$('#iframe').text(data.iframe); // show updated iframe
            $('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
        });

        event.preventDefault();

    });

});

/*
show step 2 to user
*/
$(document).ready(function() {

    $('#lead_ad_generator_step_2').on('click', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val(),
                headline : $('#headline').val(),
                text : $('#text').val(),
                //image : $('#image').val(),
                privacy_policy : $('#privacy_policy').val(),
                url : $('#url').val(),
                budget : $('#budget').val(),
            },
            type : 'POST', // type of request to send
            url : '/get_preview' // url to send data to
        })
        .done(function(data) {
            $('#lead_ad_generator_form_1').hide();
            $('#lead_ad_generator_form_3').hide();
            $('#lead_ad_generator_form_2').show();
            $('#publish_lead_ad_button_div').hide();
            //$('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
        });

        event.preventDefault();

    });

});

/*
update iFrame based on users selections from step 2
*/
$(document).ready(function() {

    // send user selected 'ad_account' and 'page' to /lead_ad_generator_1 and pass iframe with default variables
    $('.lead_ad_generator_form_2').on('change', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val(),
                headline : $('#headline').val(),
                text : $('#text').val(),
                //image : $('#image').val(),
                privacy_policy : $('#privacy_policy').val(),
                url : $('#url').val(),
                budget : $('#budget').val(),
            },
            type : 'POST', // type of request to send
            url : '/get_preview' // url to send data to
        })
        .done(function(data) {
            //$('#iframe').text(data.iframe); // show updated iframe
            $('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
        });

        event.preventDefault();

    });

});

/*
show step 3 to user
*/
$(document).ready(function() {

    $('#lead_ad_generator_step_3').on('click', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val(),
                headline : $('#headline').val(),
                text : $('#text').val(),
                //image : $('#image').val(),
                privacy_policy : $('#privacy_policy').val(),
                url : $('#url').val(),
                budget : $('#budget').val(),
            },
            type : 'POST', // type of request to send
            url : '/get_preview' // url to send data to
        })
        .done(function(data) {
            $('#lead_ad_generator_form_1').hide();
            $('#lead_ad_generator_form_2').hide();
            $('#lead_ad_generator_form_3').show();
            $('#publish_lead_ad_button_div').show();
            //$('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
        });

        event.preventDefault();

    });

});

/*
update iFrame based on users selections from step 3
*/
$(document).ready(function() {

    // send user selected 'ad_account' and 'page' to /lead_ad_generator_1 and pass iframe with default variables
    $('#url').on('change', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val(),
                headline : $('#headline').val(),
                text : $('#text').val(),
                //image : $('#image').val(),
                privacy_policy : $('#privacy_policy').val(),
                url : $('#url').val(),
                budget : $('#budget').val(),
            },
            type : 'POST', // type of request to send
            url : '/get_preview' // url to send data to
        })
        .done(function(data) {
            // update the iframe only if user updates the url
            $('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"

        });

        event.preventDefault();

    });

});


// turns "publish" button on
$(document).ready(function() {

    $('.lead_ad_generator_form_3').on('change', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
            },
            type : 'POST', // type of request to send
            url : '/get_preview' // url to send data to
        })
        .done(function(data) {
             $('#publish_lead_ad_button').removeAttr("disabled");
             //$('#publish_lead_ad_button_div').removeAttr("disabled");
        });

        event.preventDefault();

    });


});

// when user clicks "publish" button, data is sent to facebook
$(document).ready(function() {

    $('#publish_lead_ad_button').on('click', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val(),
                headline : $('#headline').val(),
                text : $('#text').val(),
                //image : $('#image').val(),
                privacy_policy : $('#privacy_policy').val(),
                url : $('#url').val(),
                budget : $('#budget').val(),
            },
            type : 'POST', // type of request to send
            url : '/publish_ad' // url to send data to
        })
        .done(function(data) {

            // if error variable is anything but an empty string throw an error message and allow user to make edits
            if (data.error != "") { // ad did not publish
                $('#errorAlert').text(data.error).show(); // print facebook-specific error message
            }
            else { // ad published successfully
                // remove ability for user to edit ad
                $('#lead_ad_generator_menu').hide();
                $('#lead_ad_generator_form_3').hide();

                // remove ability for user to see preview and publish another ad
                $('#lead_ad_preview').hide();
                $('#publish_lead_ad_button_div').hide();

                // add success message
                $('#successAlert').show();

                // add user form to enter email for notifications
                $('#lead_ad_generator_email_notifications').show();
            }
            //error message
        });

        event.preventDefault();

    });

});
