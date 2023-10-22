"use strict";
const createScript = (src)=>{
    const sc = document.createElement("script");
    sc.type = "text/javascript";
    sc.defer = true;
    sc.src = `/static/js/${src}`;

    return sc;  
}
const loadScript = (url, func)=>{
    $.ajax({
        url: url,
        dataType: 'script',
        success: (func) ? func : function(){
            let script = $("script[src='/static/js/authenticate.js/']");
            if (script.length > 0)
            {
                script.remove();
            } else {
                console.log("script does not exist !");
            }
        }
    });
}
const showAlert = (msg, category)=>{
    let alert = `<p class="alert alert-${category} `
    alert += `alert-dismissible mt-2 mb-2 pl-3 pl- fade show">${msg}`
    alert += `<span class="btn-close" data-bs-dismiss="alert"`
    alert += ` aria-label="Close">&times</span></p>`;
    // $("#loader").fadeOut(500);
    $(".ajx").prepend(alert);
};
const showLoader = ()=>{
    let content = $("#content");
    let body = $("body");
    let bloader = $("#blo");
    body.addClass("body-loading");
    bloader.removeClass("bloader");
    content.hide(1);
    console.log("Shown");
}

const hideLoader = (title, url)=>{
    let bloader = $("#blo");
    let body = $("body");
    let content = $("#content");
    $("title").text(title);
    bloader.addClass("bloader");
    window.history.pushState(null, null, url);
    content.show(1);
    body.removeClass("body-loading");
    console.log("hidden");
}// hides the loader icon
const getHtml = (url, title, script)=>{
    $.ajax({
        url: url,
        type: "GET",
        success:function(data, textStatus, jqXHR)
        {
            // let bodyText = jqXHR.responseText.match(/<fieldset[^>]*>([\s\S]*)<\/fieldset>/i)[1];
            let bodyText = $.parseHTML(data);
            bodyText.forEach(function(data){
                if ($(data).hasClass('ajx'))
                {
                    $(".ajx").replaceWith(data);
                }

            });
        }
    });
}// only to be used when the user is logged in
let token = localStorage.getItem("refresh");
if (token !== null)
{
    $.ajaxSetup({
        headers:{Authorization: `Bearer ${localStorage.getItem("refresh")}`},
        error:function()
        {
            showAlert("An error occured !", "danger");
        }
    });
    let location = window.location.pathname;
    if (location === "/login/" || location === "/sign-up/")
    {
        showLoader();
        let resp = getHtml(`/ajax/v1.0/match-course/`, "Match");
        let form = $("form");
        form.css("class", "mt-3");
        hideLoader("Match", '/match-course/');
        $.ajax(
        {
            url: '/static/js/match.js/',
            dataType: 'script',
            success: function()
            {
                let script = $("script[src='/static/js/authenticate.js/']");
                let script0 = $("script[src='/static/js/signup.js/']");
                if (script.length > 0)
                {
                    script.remove();
                } else if (script0.length > 0){
                    script0.remove();
                    alert("removed");
                } else {
                    console.log("Script does not exist");
                }
            }
        });
        // $("#body").html(resp.bodyText);
    } else if (location === "/admin/authenticate/" || location === "/admin/sign-up/")
    {
        let user = $.getJSON("/ajax/v1.0/get-auth-data/", function(user){
            let msg = `User ${user["username"]} is not an admin, you need to login with an admin account!!!`;
            if (!user["is_admin"])
            {
                showAlert(msg, "danger");
            } else
            {
                window.location.pathname = '/admin/';
            }
        });
    } else if (location === "/admin/")
    {
        $.ajax({
            url:"/static/js/admin/home.js/",
            dataType: 'script',
            type:"get",
            success:function(data){
                console.log("admin js loaded successfully");
            }
        });
    } else
    {
        console.log("An Else statement");
    }
    

} else
{
    let location = window.location.pathname;
    if (location !== "/login/" && location !== "/sign-up/" && location !== "/admin/authenticate/")
    {
        window.location.pathname = "/login/";// redirect users to the login page
    }
}
const getAndChangePageFunction = (href)=>{
    console.log("Function Executed");
    $.ajax({
        url: href,
        type: "GET",
        beforeSend: function(){
            showLoader();
        },
        success:function(data, textStatus, jqXHR)
        {
            let bodyText = $.parseHTML(data);
            bodyText.forEach(function(data){
                if ($(data).hasClass('ajx'))
                {
                    $(".ajx").replaceWith(data);
                }

            });
        }
    });
    window.history.pushState(null, null, href);

}
$(document).ready(function()
{
    if (token)
    {
        $(".usp").hide(1);//hide  views required for not authenticated
        $(".auth").show(1);//shows views required for authentication 
    }else{
        $(".usp").show(1);//vice versa
        $(".auth").hide(1);//vice versa
    }
    hideLoader();
    if(window.location.pathname == "/login/")
    {
        $(".bio-data").css({display: null});
    }//remove the bio data form from login
});
