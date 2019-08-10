// update iFrame
$(document).ready(function() {

    // send data to /get_preview and send iframe to HTML
    function getPreview() {
        var headline = ($('#headline').val() == "") ? "SEE PICS & PRICE 👉" : $('#headline').val();
        var image = ($('#image').val() == "") ? "https://drive.google.com/uc?id=1_pvz61BtsDM1T2n21oU9bRASNUG3BCak" : $('#image').val();
        var url = ($('#url').val() == "") ? "LinkToTheProperty.com" : $('#url').val();
        var text = ($('#text').val() == '🔥 New CITY area listing!! 🔥 \n\nBEDS: \nBATHS:  \nSQ FT: \n\n🏠🔑🏠🔑🏠🔑\n\nTo see the price, location, and more pictures, tap "Learn More"') ? '🔥 New NEW YORK area listing!! 🔥 \n\nBEDS: 2 \nBATHS: 3  \nSQ FT: 2100 \n\n🏠🔑🏠🔑🏠🔑\n\nTo see the price, location, and more pictures, tap "Learn More"' : $('#text').val();
        console.log(image);
        $.ajax({
            data : {
                ad_account : $('#ad_account').val(),
                page : $('#page').val(),
                headline : headline,
                text : text,
                image : image,
                url : url,
                budget : $('#budget').val(),
            },
            type : 'POST', // type of request to send
            url : '/get_preview' // url to send data to
        })
        .done(function(data) {
            //$('#iframe').text(data.iframe); // show updated iframe
            $('#lead_ad_preview').attr("src", data.iframe);  // "https://cdn-img.meetedgar.com/wp-content/uploads/2017/07/Mr-DNA.gif"
        });
    };

    // load preview on first page load
    if ($('form.lead_ad_generator_form_1').length > 0)
    {
        getPreview();
    }

    // load preview each time a relevant field is changed
    $('#page, #headline').on('change', function(event) {
        getPreview();
    });

    // validate user input
    $('#text').on('change', function(event) {
        $('#invalid_text').hide();
        $('#valid_text').show();
        getPreview();
    });
    $('#url').on('change', function(event) {
        $('#invalid_url').hide();
        $('#valid_url').show();
        getPreview();
    });

    // load user uploaded image
    $(document).on('change', '.btn-file :file', function() {
        var input = $(this),
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        input.trigger('fileselect', [label]);
    });

    $('.btn-file :file').on('fileselect', function(event, label) {

        var input = $(this).parents('.input-group').find(':text'),
            log = label;

        if( input.length ) {
            input.val(log);
        } else {
            if( log ) alert(log);
        }

    });

    // send user uploaded image to cloudinary and get back uploaded image link
    function readURL(input) {
        console.log("uploading photo...");
        // var CLOUDINARY_URL = 'https://api.cloudinary.com/v1_1/dhzcvp1gh/upload';
        var CLOUDINARY_URL = 'https://api.cloudinary.com/v1_1/dhzcvp1gh/image/upload';
        var CLOUDINARY_UPLOAD_PRESET = 'omqjgbu0';
        var file = event.target.files[0];
        var formData = new FormData();
        formData.append('file', file); // add file to FormData
        formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);
        $('#valid_image').text("Uploading Image..");
        axios({
            url: CLOUDINARY_URL,
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: formData
        }).then(function(res) {
            $('#image').val(res.data.secure_url);
            $('#valid_image').text("Upload Successful.");
            getPreview();
        }).catch(function(err) {
            //$('#image').val('https://res.cloudinary.com/dhzcvp1gh/image/upload/v1565444311/cxvuqosctw4z3qydmahx.png');
            //getPreview();
            console.error(err);
            $('#valid_image').hide();
            $('#invalid_image').text("Error uploading image: (" + err + ")").show();
        });
    };

    $("#imgInp").change(function(){
        $('#invalid_image').hide();
        $('#valid_image').text("Uploading Image.").show();
        readURL(this);
    });

});

// popovers
$(document).ready(function(){
    $('[data-toggle="popover"]').popover()
});


// show left menu to user for each step
$(document).ready(function() {
    var selected_color = '#4C637A';
    var deselected_color = '#C79031';
    $('#lead_ad_generator_step_1').on('click', function(event) {

        $('#lead_ad_generator_form_2').hide();
        $('#lead_ad_generator_form_3').hide();
        $('#lead_ad_generator_form_1').show();
        $('#publish_lead_ad_button_div').hide();
        $('#lead_ad_generator_menu div').first().css("background-color", selected_color);
        $('#lead_ad_generator_menu div:nth-child(2)').css("background-color", deselected_color);
        $('#lead_ad_generator_menu div:nth-child(3)').css("background-color", deselected_color);
    });

    $('#lead_ad_generator_step_2, #continue_button_step_1').on('click', function(event) {

        $('#lead_ad_generator_form_1').hide();
        $('#lead_ad_generator_form_3').hide();
        $('#lead_ad_generator_form_2').show();
        $('#publish_lead_ad_button_div').hide();
        $('#lead_ad_generator_menu div').first().css("background-color", deselected_color);
        $('#lead_ad_generator_menu div:nth-child(2)').css("background-color", selected_color);
        $('#lead_ad_generator_menu div:nth-child(3)').css("background-color", deselected_color);
    });

    $('#lead_ad_generator_step_3, #continue_button_step_2').on('click', function(event) {

        $('#lead_ad_generator_form_1').hide();
        $('#lead_ad_generator_form_2').hide();
        $('#lead_ad_generator_form_3').show();
        $('#publish_lead_ad_button_div').show();
        $('#lead_ad_generator_menu div:nth-child(3)').css("background-color", selected_color);
        $('#lead_ad_generator_menu div').first().css("background-color", deselected_color);
        $('#lead_ad_generator_menu div:nth-child(2)').css("background-color", deselected_color);
    });

});

/*
// turns "publish" button on
$(document).ready(function() {

    $('.lead_ad_generator_form_3').on('change', function(event) {
        console.log("triggering javascript");
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
*/
// when user clicks "publish" button, data is sent to facebook
$(document).ready(function() {

    $('#publish_lead_ad_button').on('click', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val(),
                headline : $('#headline').val(),
                text : $('#text').val(),
                image : $('#image').val(),
                privacy_policy : $('#privacy_policy').val(),
                url : $('#url').val(),
                budget : $('#budget').val(),
                city_key : $('.secret.sr-only').attr('id'),
            },
            type : 'POST', // type of request to send
            url : '/publish_ad' // url to send data to
        })
        .done(function(data) {

            // if error variable is anything but an empty string throw an error message and allow user to make edits
            if (data.tos_accepted == false) { // print
                $('#toserrorAlert').show();
            }
            else if (data.error != "") { // ad did not publish

                if (data.url) { // print no credit card error message
                    $('#errorAlertLink a').attr('href', data.url); // print facebook-specific error message
                    $('#errorAlertLink').show(); // print facebook-specific error message
                }
                else {
                    $('#errorAlert').text(data.error).show(); // print facebook-specific error message
                }
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

// display facebook locations based on user input
$(document).ready(function() {

    $('#location_query').on('keyup', function(event) {
        var location_query = "";
        $.ajax({
            data : {
                location_query : $('#location_query').val(),
            },
            type : 'POST',
            url : '/get_locations',
            success: function (data) {
                location_query = $('#location_query').val();
            },
        })
        .done(function(data) { // reference: https://stackoverflow.com/questions/43351617/javascript-how-to-loop-through-json-objects-with-jquery-in-an-ajax-call
            var html = '';
            var location_query_capitalized = location_query.charAt(0).toUpperCase() + location_query.slice(1)
            $(data).each(function(index, value) {
                    html+='<li class="list-group-item" id='+value.key+'>'+value.name+'</li>';
            });
            html = html.split(location_query_capitalized).join('<strong class>'+location_query_capitalized+'</strong>');
            $('.list-group').html(html);
            //$('#location_list').html(html);
            $('.list-group').show();

             // delayed callback to return user selected location
             var y = $(".list-group li").attr('class');
             console.log(y);
             $("ul li").on({
               click: function(){
                 var $this = $(this)
                 console.log($this);
                 $('#location_query').val($this.text()); // update value with user selected name
                 $('.secret.sr-only').attr("id", $this.attr('id')); // update id with user selected id by referencing the class
                 $('.list-group').hide();
                 $('#invalid_location').hide();
                 $('#valid_location').show();
               },
             });

        });

        event.preventDefault();

    });

});
