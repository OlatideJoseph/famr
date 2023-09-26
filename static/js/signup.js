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
        $("form").on("submit", function(e)
        {
            e.preventDefault();
            let data = $(this).serialize();
            console.log(data);
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
$(window).on("load",function(){
    $(".nav-link").click(function(e){
        e.preventDefault();//Stops the default action of the page
        getAndChangePageFunction($(this).attr('href'));
        $("title").text($(this).text());
    });
});