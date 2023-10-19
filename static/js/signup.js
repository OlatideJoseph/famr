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
            // e.preventDefault();
            let data = $(this).serialize();
            $.ajax(
            {
                url: `${window.location.pathname}`,
                type:"POST",
                data: data,
                beforeSend: function(data)
                {
                    showLoader();
                },
                success: function(data, textStatus, jqXHR)
                {
                    window.history.pushState(null, null, '/login/');
                    showAlert(data["msg"][0], data["msg"][1]);
                },
                error: function(data)
                {
                    console.log(data.responseJSON);
                    let resp = data.responseJSON;
                    hideLoader("Login", "/login/");
                    showAlert( resp["msg"][0], resp["msg"][1]);
                }
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
                $.ajax(
                {
                    url: href,
                    type: "GET",
                    success:function(data, textStatus, jqXHR)
                    {
                        var bodyText = jqXHR.responseText.match(/<body[^>]*>([\s\S]*)<\/body>/i)[1];
                        $('body').html(bodyText);
                        $.ajax(
                        {
                            url: '/static/js/signup.js/',
                            dataType: 'script',
                            success: function()
                            {
                                let script = $("script[src='/static/js/signup.js/']");
                                if (script.length > 0)
                                {
                                    script.remove();
                                } else {
                                    console.log("script does not exist !");
                                }
                            }
                        });
                    },
                    complete: function()
                    {
                        hideLoader(title, href);
                    }
                });
            }
        );
	}
);
$(window).on("load",function()
{
    hideLoader();
    if (token)
    {
        $(".usp").hide(1);//hide  views required for not authenticated
        $(".auth").show(1);//shows views required for authentication 
    }else{
        $(".usp").show(1);//vice versa
        $(".auth").hide(1);//vice versa
    }
});