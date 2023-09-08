"use strict";
showLoader();
let glocation = window.location.pathname;
let form = document.querySelector("fieldset");
getHtml(`/ajax/v1.0${glocation}`);
console.log("htis");
hideLoader('Grade Point', '/grade-add/');
$(window).on('load', function(){
    let f = document.querySelector('form');
    $("form").on('submit', function(e)
    {
        alert("hello");
        e.preventDefault();
        let form = $(this).serialize();
        $.ajax(
        {
            url: `/ajax/v1.0${window.location.pathname}`,
            type:"POST",
            data:form,
            beforeSend: function(data)
            {
                console.log("started");
            },
            success: function(data, textStatus, jqXHR)
            {
                console.log(data);
                showAlert(data["msg"][0], data["msg"][1]);
                alert(data);
            },
            error: function(data)
            {
                console.log(data.responseJSON);
                let resp = data.responseJSON;
                hideLoader("Login", "/login/");
                showAlert( resp["msg"][0], resp["msg"][1]);
            }
        });
    }
    );
});
console.log("next");