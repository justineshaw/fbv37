// load preview on first page load
$(function ()
{
    if ($('form.lead_ad_generator_form_1').length > 0)
    {
        $.ajax({
            data : {
                ad_account : $('#ad_account').val(),
                page : $('#page').val(),
                headline : $('#headline').val(),
                text : $('#text').val(),
                image : $('#image').val(),
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
    }
});

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
                image : $('#image').val(),
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
            $('#lead_ad_generator_menu div').first().css("background-color", "#4c637a");
            $('#lead_ad_generator_menu div:nth-child(2)').css("background-color", "#5d80a3");
            $('#lead_ad_generator_menu div:nth-child(3)').css("background-color", "#5d80a3");
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
                image : $('#image').val(),
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
                image : $('#image').val(),
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
            $('#lead_ad_generator_menu div').first().css("background-color", "#5d80a3");
            $('#lead_ad_generator_menu div:nth-child(2)').css("background-color", "#4c637a");
            $('#lead_ad_generator_menu div:nth-child(3)').css("background-color", "#5d80a3");

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
                image : $('#image').val(),
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
        console.log("triggering javascript lead_ad_step_3 on click");
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
            },
            type : 'POST', // type of request to send
            url : '/get_preview' // url to send data to
        })
        .done(function(data) {
            $('#lead_ad_generator_form_1').hide();
            $('#lead_ad_generator_form_2').hide();
            $('#lead_ad_generator_form_3').show();
            $('#publish_lead_ad_button_div').show();
            $('#lead_ad_generator_menu div:nth-child(3)').css("background-color", "#4c637a");
            $('#lead_ad_generator_menu div').first().css("background-color", "#5d80a3");
            $('#lead_ad_generator_menu div:nth-child(2)').css("background-color", "#5d80a3");
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
        console.log("triggering javascript url");
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
                    /*
                    html+='<div id=location'+index+' class="dropdown-item" data-index='+index+'>';
                        html+='<div class="row justify-content-between mx-4 my-1">';
                            html+='<span>';
                                //html+='<strong class>'+location_query+'</strong>';
                                html+='<span id='+value.key+' class="user_selected_location">'+value.name+'</span>';
                            html+='</span>';
                            html+='<div id="location_type" class="text-secondary text-sm">'+value.type+'</div>';
                        html+='</div>';
                    html+='</div>';
                    */

                    // html+='<a class="dropdown-item" id='+value.key+' href="#">'+value.name+'</a>';
                    //html+='<button type="button" class="list-group-item list-group-item-action" id='+value.key+'>'+value.name+'</button>';
                    html+='<li class="list-group-item" id='+value.key+'>'+value.name+'</li>';
                    //html+='<a class="list-group-item" id='+value.key+'>'+value.name+'</li>';
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
               },
             });

        });

        event.preventDefault();

    });

});
