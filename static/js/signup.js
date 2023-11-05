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
            let objData = {

            };
            $(this).find('input').each(
                function (...args) {
                    let cu = $(args[1]);
                    if (cu.attr('type') != 'submit')
                        objData[cu.attr('name')] = cu.val();
                }
            );//gets each form in
            objData = JSON.stringify(objData);
            $.ajax(
            {
                url: `${window.location.pathname}`,
                type:"POST",
                contentType:'application/json',
                data: objData,
                beforeSend: function(data)
                {
                    showLoader();
                },
                success: function(data, textStatus, jqXHR)
                {
                    window.history.pushState(null, null, '/login/');
                    showAlert(data["msg"][0] + ';you\'ll be redirected in 3s', data["msg"][1]);
                    setTimeout(()=>{window.location.pathname = '/login/'}, 3000);
                },
                error: function(data)
                {
                    console.log(data.responseJSON);
                    let resp = data.responseJSON;
                    hideLoader("Signup", "/sign-up/");
                    showAlert(data["msg"][0], resp["msg"][1]);
                }
            });
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
                        let bodyText = $.parseHTML(data);
                        bodyText.forEach(function(data)
                        {
                            if ($(data).hasClass('ajx'))
                            {
                                $(".ajx").replaceWith(data);
                                $('title').text('Login');
                            }
                        });
                        $.ajax(
                        {
                            url: '/static/js/authenticate.js/',
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