"use strict";
$("form").first().on('submit',function(e){
    e.preventDefault();
    let form = $(this).serialize();
    alert(form);
    $.ajax(
    {
        url:window.location,
        type:"POST",
        data:form,
        success: function(data){
            localStorage.setItem("refresh", data["refresh_token"]);
            let alert = `<span class="alert alert-${data["msg"][1]}">${data["msg"][0]}</span>`
            $(".ajx").prepend(alert);
        },
        error: function(data){
            console.log(data.responseJSON);
        }
    });
});