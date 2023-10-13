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
if (token !== null){
    $.ajaxSetup({
        headers:{Authorization: `Bearer ${localStorage.getItem("refresh")}`}
    });
    let location = window.location.pathname;
    if (location === "/login/" || location === "/sign-up/"){
        showLoader();
        let resp = getHtml(`/ajax/v1.0/match-course/`, "Match");
        let form = $("form");
        form.css("class", "mt-3");
        hideLoader();
        window.history.pushState(null, null, "/match-course/");
        // $("#body").html(resp.bodyText);
    }
    

}else
{
    let location = window.location.pathname;
    if (location !== "/login/" && location !== "/sign-up/" && location !== "/admin/authenticate/")
    {
        window.location.pathname = "/login/";// redirect users to the login page
    }
}
const showLoader = ()=>{
    let content = $("#content");
    let body = $("body");
    let bloader = $("#blo");
    console.log(bloader);
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
    console.log("hidden");
}// hides the loader icon
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

}// A util function that changes pages content on click
// const eventNavLink = ()=>{
//     $(".sp").click(function(e){
//         e.preventDefault();
//         let a = $(this);
//         let active = $("a.active");
//         let href = a.attr("href");
//         let title = a.text();
//         let lco = window.location.pathname;
//         if (lco === "/"){
//             console.log("home");
//             let fieldset = `<fieldset class="form mt-3"></fieldset>`;
//             $("#home-content").html(fieldset);
//         }
//         $.ajax({
//         url: href,
//         type: "get",
//         dataType: "script",
//         beforeSend: function(){
//             showLoader();
//         },
//         success: function(data, textStatus, jqXHR)
//             {
//                 let bodyText = jqXHR.responseText.match(/<fieldset[^>]*>([\s\S]*)<\/fieldset>/i)[1];
//                 let msg = "success";
//                 let d = $(data).find("#content");
//                 $("#content").html(d);
//                 hideLoader(title, href);
//             }
//         });
//     }
//     );
// }// set an event listener for all anchor tag applied sp
$(window).on("load", function()
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
        $(".bio-data").css({display: "none"});
    }
});