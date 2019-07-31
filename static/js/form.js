$(document).ready(function() {

    // send user selected 'ad_account' and 'page' to /lead_ad_generator_1 and pass iframe with default variables
    $('.lead_ad_generator_form_1').on('change', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val()
            },
            type : 'POST', // type of request to send
            url : '/lead_ad_step_2' // url to send data to
        })
        .done(function(data) {
            $('#headline').text("iframe loaded");
            $('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
        });

        event.preventDefault();

    });

});
