$(document).ready(function() {

	$('.lead_ad_generator_form_1').on('change', function(event) {

		$.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
			data : { // specifies the data to be sent to the server
				headline : $('#headlineInput').val(),
                ad_account : $('#ad_account').val() // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
			},
			type : 'POST', // type of request to send
			url : '/lead_ad_process_1' // url to send data to
		})
		.done(function(data) {
            $('#headline').text(data.headline); // data.headline
            // $('#page').text(data.ad_account);
            //$('#lead_ad_preview').attr("src", data.lead_ad_preview);  // https://stackoverflow.com/questions/554273/changing-the-image-source-using-jquery
		});

		event.preventDefault();

	});

    // send user selected 'ad_account' and 'page' to /lead_ad_generator_1 and pass iframe with default variables
    $('.lead_ad_generator_form_1').on('change', function(event) {

        $.ajax({ // jquery AJAX method to perform an AJAX (asynchronous HTTP) request
            data : { // specifies the data to be sent to the server
                headline : $('#headlineInput').val(),
                ad_account : $('#ad_account').val(), // https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
                page : $('#page').val()
            },
            type : 'POST', // type of request to send
            url : '/lead_ad_process_1' // url to send data to
        })
        .done(function(data) {
            $('#headline').text(data.headline);
            $('#ad_account').text(data.ad_account);
            $('#page').text(data.page);
            //$('#lead_ad_preview').attr("src", data.lead_ad_preview);  // https://stackoverflow.com/questions/554273/changing-the-image-source-using-jquery
        });

        event.preventDefault();

    });

});
