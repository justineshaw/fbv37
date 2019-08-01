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
            //$('#iframe').text(data.iframe);
            $('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
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
            //$('#iframe').text(data.iframe); // show updated iframe
            $('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
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
            //$('#iframe').text(data.iframe); // show updated iframe
            $('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
        });

        event.preventDefault();

    });

});

/*
update iFrame based on users selections from step 3
*/
$(document).ready(function() {

    // send user selected 'ad_account' and 'page' to /lead_ad_generator_1 and pass iframe with default variables
    $('.lead_ad_generator_form_3').on('change', function(event) {

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
