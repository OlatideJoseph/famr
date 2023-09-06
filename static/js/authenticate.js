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
            let spinner = `<img alt="spinner" id="loader/>`;
            $.ajax(
            {
                url: `${window.location.pathname}`,
                type:"POST",
                data:form,
                beforeSend: function(data)
                {
                    showLoader();
                },
                success: function(data)
                {
                    localStorage.setItem("refresh", data["refresh_token"]);
                    showAlert(data["msg"][0], data["msg"][1]);
                    $(".ajx").load("ajax/v1.0/match-course #form");
                    hideLoader("Match", "/match-course");
                },
                error: function(data)
                {
                    console.log(data.responseJSON);
                    let resp = data.responseJSON;
                    showAlert( resp["msg"][0], resp["msg"][1]);
                    hideLoader("Login", "/login/");
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
