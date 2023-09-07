"use strict";
$(document).ready(
    function()
    {
        //setting the form to the center
        $(".ajx").css(
        {
            "display": "flex", "justify-content":"center",
            "align-items": "center",
            "flex-direction":"column"
        }
        );
        $("form").first().on('submit',function(e){
            e.preventDefault();
            let form = $(this).serialize();
            $.ajax(
            {
                url: `${window.location.pathname}`,
                type:"POST",
                data:form,
                beforeSend: function(data)
                {
                    showLoader();
                },
                success: function(data, textStatus, jqXHR)
                {
                    localStorage.setItem("refresh", data["refresh_token"]);
                    let resp = getHtml("/match-course/");
                    $('body').html(resp["bodyText"]);
                    hideLoader("Match", "/match-course/");
                    showAlert(data["msg"][0], data["msg"][1]);
                },
                error: function(data)
                {
                    console.log(data.responseJSON);
                    let resp = data.responseJSON;
                    hideLoader("Login", "/login/");
                    showAlert( resp["msg"][0], resp["msg"][1]);
                }
            });
        });
        // signup link event listener
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
                        let bodyText = jqXHR.responseText.match(/<body[^>]*>([\s\S]*)<\/body>/i)[1];
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
