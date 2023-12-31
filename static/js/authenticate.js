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
            console.log(form)
            $.ajax(
            {
                url: `${window.location.pathname}`,
                type:"POST",
                data:form,
                contentType: "application/x-www-form-urlencoded",
                beforeSend: function(xhr, settings)
                {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain)
                    {
                        xhr.setRequestHeader("X-CSRFToken", $("#csrf_token").val());
                    }
                },
                success: function(data, textStatus, jqXHR)
                {
                    let form = $("form");
                    localStorage.setItem("refresh", data["refresh_token"]);
                    $.ajaxSetup({
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem("refresh")}`, 
                        },
                        async: true,
                    });//sets the default req header
                    window.location.pathname = "/match-course/";
                    // form.hide();
                    // let resp = getHtml(`/ajax/v1.0/match-course/`);//gets the form element
                    // $(".usp").show();
                    // $(".bio-data").show(0);
                    // form.css("class", "");
                    // form.show();

                    // hideLoader("Match", "/match-course/");
                    // showAlert(data["msg"][0], data["msg"][1]);
                },
                error: function(data)
                {
                    console.log(data.responseJSON);
                    let resp = data.responseJSON;
                    hideLoader("Login", "/login/");
                    showAlert( resp["msg"][0], resp["msg"][1]);
                }
            });// ajax requests ends here
        });
        hideLoader();
        $(window).on("load",function(){
            $(".nav-link").click(function(e){
                e.preventDefault();//Stops the default action of the page
                getAndChangePageFunction($(this).attr('href'));

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
                    success:function(data, textStatus, jqXHR)
                    {
                        let bodyText = $.parseHTML(data);
                        bodyText.forEach(function(data){
                            if ($(data).hasClass('ajx'))
                            {
                                $(".ajx").replaceWith(data);
                                $('title').text("Sign Up")
                            }

                        });
                        $.ajax({
                            url: '/static/js/signup.js/',
                            dataType: 'script',
                            success: function(){
                                let script = $("script[src='/static/js/authenticate.js/']");
                                if (script.length > 0)
                                {
                                    script.remove();
                                } else {
                                    console.log("script does not exist !");
                                }
                            }
                        });
                        // bloader.fadeOut(1000);
                        // form.show();
                        // window.history.pushState(null, null, href);
                        // body.css('overflow','auto');

                    },
                    complete: function()
                    {
                        hideLoader(title, href);
                    },
                });
            }
        );

    }
);
