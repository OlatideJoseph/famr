"use strict";
const createScript = (src)=>{
    const sc = document.createElement("script");
    sc.type = "text/javascript";
    sc.defer = true;
    sc.src = `/static/js/${src}`;

    return sc;  
}
const showAlert = (msg, category)=>{
    let alert = `<p class="alert alert-${category} `
    alert += `alert-dismissible mt-2 mb-2 pl-3 pl- fade show">${msg}`
    alert += `<span class="btn-close" data-bs-dismiss="alert"`
    alert += ` aria-label="Close">&times</span></p>`;
    // $("#loader").fadeOut(500);
    $("nav").after(alert);
};
const getHtml = (url, title)=>{
    $.ajax({
        url: url,
        type: "GET",
        success:function(data, textStatus, jqXHR)
        {
            let bodyText = jqXHR.responseText.match(/<fieldset[^>]*>([\s\S]*)<\/fieldset>/i)[1];
            let msg = "success";
            let dat = data;
            hideLoader(title, url.split("0")[1]);
            $("fieldset").html(bodyText);
        }
    });
}// only to be used when the user is logged in
let token = localStorage.getItem("refresh");
if (token !== null){
    $.ajaxSetup({
        headers:{Authorization: `Bearer ${localStorage.getItem("refresh")}`}
    });
    let location = window.location.pathname;
    if (location === "/login/" || location === "/sign-up/"){
        let resp = getHtml(`/ajax/v1.0/match-course/`, "Match");
        let form = $("form");
        form.css("class", "mt-3");
        window.history.pushState(null, null, "/match-course/");
        // $("#body").html(resp.bodyText);
    }
    

}else
{
    let location = window.location.pathname;
    if (location !== "/login/" && location !== "/sign-up/")
    {
        window.location.pathname = "/login/";// redirect users to the login page
    }else
    {
        createScript("authenticate.js");
    }
}
const showLoader = ()=>{
    let content = $("#content");
    let body = $("body");
    let bloader = $("#blo");
    if (bloader.hasClass("bloader") !== true){
        content.hide(1);
        bloader.toggleClass("bloader");
        body.css("overflow","hidden");
    }
}

const hideLoader = (title, url)=>{
    let bloader = $("#blo");
    let body = $("body");
    let content = $("#content");
    $("title").text(title);
    if (bloader.hasClass("bloader") === true){
        content.show();
        bloader.toggleClass("bloader");
        body.css("overflow","auto");
        window.history.pushState(null, null, url);
    }
}// hides the loader icon

const linkOpener = (tag)=>{
$(tag).on("click",
    function(e)
    {
        showLoader();
        let href = $(this).attr("href");
        e.preventDefault();
        if ((href !== "/sign-up/") && (href !== "/login/"))
        {
            $("body").load(`/ajax/v1.0${href} #content`, function(data)
            {
                hideLoader($(this).text(), href);
            }
            );
        }else
        {
            $("#body").load(`${href} #content`, function(data)
            {
                hideLoader($(this).text(), href);
            }
            );
        }       
    }
);
}
const eventNavLink = ()=>{
    $(".sp").click(function(e){
        e.preventDefault();
        let a = $(this);
        let active = $("a.active");
        let href = a.attr("href");
        let title = a.text();
        let lco = window.location.pathname;
        if (lco === "/"){
            console.log("home");
            let fieldset = `<fieldset class="form mt-3"></fieldset>`;
            $("#home-content").html(fieldset);
        }
        showLoader();
        getHtml(`/ajax/v1.0${href}`, title);
        hideLoader(title, href);

    }
    );
}// set an event listener for all anchor tag applied sp
$(document).ready(function(){
    eventNavLink();
    if (token)
    {
        $(".usp").hide(1);//hide  views required for not authenticated
        $(".auth").show(1);//shows views required for authentication 
    }else{
        $(".usp").show(1);//vice versa
        $(".auth").hide(1);//vice versa
    }
});