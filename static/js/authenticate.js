"use strict";
$(document).ready(
    function()
    {
        const showAlert = (msg, category)=>{
            let alert = `<p class="alert alert-${category} `
            alert += `alert-dismissible mt-2 mb-2 pl-3 pl- fade show">${msg}`
            alert += `<span class="btn-close" data-bs-dismiss="alert"`
            alert += ` aria-label="Close">&times</span></p>`;
            // $("#loader").fadeOut(500);
            $("nav").after(alert);
        }
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
            alert(form);
            $.ajax(
            {
                url:window.location,
                type:"POST",
                data:form,
                beforeSend: function(data)
                {
                    $('.login').after(spinner);
                },
                success: function(data)
                {
                    localStorage.setItem("refresh", data["refresh_token"]);
                    showAlert(data["msg"][0], data["msg"][1]);
                },
                error: function(data)
                {
                    console.log(data.responseJSON);
                    let resp = data.responseJSON;
                    showAlert( resp["msg"][0], resp["msg"][1]);
                }
            });
        });
        // signup link event listener
        $('.link').on('click', function(e)
            {
                e.preventDefault();
                let href = $(this).attr('href');
                $.get(`${window.origin}/${href}#form`,function(data)
                {
                    alert(data);
                }
                );
            }
        );

    }
);
