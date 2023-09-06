"use strict";
$(document).ready(
	function()
	{
        $(".ajx").css(
	        {
	            "display": "flex", "justify-content":"center",
	            "align-items": "center",
	            "flex-direction":"column"
	        }
        );
        $('.link').on('click', function(e)
            {
                e.preventDefault();
                showLoader();
                let form = $("#form");
                let body = $("body");
                let title = $(this).text();
                let href = $(this).attr('href');
                $.ajax({
                    url: href,
                    type: "GET",
                    success:function(data, textStatus, jqXHR){
                        var bodyText = jqXHR.responseText.match(/<body[^>]*>([\s\S]*)<\/body>/i)[1];
                        $('body').html(bodyText);
                        hideLoader(title, href);
                        // bloader.fadeOut(1000);
                        // form.show();
                        // window.history.pushState(null, null, href);
                        // body.css('overflow','auto');
                    }
                });
            }
        );
	}
);