"use strict";
const notAllowedUrl = [
    "/login/",
    "/sign-up/",
    "/admin/",
    "/admin/authenticate/ua/",
    "/admin/register-admin-user/ua/"
];
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
    let path = window.location.pathname;
    let alert = `<p class="alert alert-${category} `;
    
    alert += `alert-dismissible mt-2 mb-2 pl-3 pl- fade show">${msg}`;
    alert += `<span class="btn-close" data-bs-dismiss="alert"`;
    alert += ` aria-label="Close">&times</span></p>`;
    // $("#loader").fadeOut(500);
    if (path != "/match-course/" && path != '/match-course-file/')
    {
        $(".ajx").prepend(alert);
    } else
    {
        $("#form").prepend(alert);
    }
};
const naShowAlert = (msg, category) => {
    let alert = `<p class="alert alert-${category} `
    alert += `alert-dismissible mt-2 mb-2 pl-3 pl- fade show">${msg}`
    alert += `<span class="btn-close" data-bs-dismiss="alert"`
    alert += ` aria-label="Close">&times</span></p>`;
    // $("#loader").fadeOut(500);
    $(".na").prepend(alert);
};

const showLoader = ()=>{
    let content = $("#content");
    let body = $("body");
    let bloader = $("#blo");
    body.addClass("body-loading");
    bloader.removeClass("bloader");
    content.hide(1);
};

const hideLoader = (title, url)=>{
    let bloader = $("#blo");
    let body = $("body");
    let content = $("#content");
    $("title").text(title);
    bloader.addClass("bloader");
    window.history.pushState(null, null, url);
    content.show(1);
    body.removeClass("body-loading");
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
const logOut = ()=>{
    $.get(`/log-out/?token=${token}`, function(data){
        showAlert(data['msg'], 'success');
    });
    localStorage.clear();
    setInterval(function(){window.location.pathname = '/';}, 3500);
    //waits for 3.5 seconds before loading to the user page
}//clears the user token and logs the user out
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
                $('title').text("Match and Find");
                let script = $("script[src='/static/js/authenticate.js/']");
                let style = $('link[href^="/static/css/auth.css"');
                if (style.length > 0)
                {
                    style.attr('href', '/static/css/match.css');
                }
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
    } else if (location.endsWith("/ua/"))
    {
        let user = $.getJSON("/ajax/v1.0/get-auth-data/", function(user){
            let msg = `User ${user["username"]} is not an admin, you need to login with an admin account!!!`;
            if (!user["is_admin"])
            {
                showAlert(msg, "danger");
                console.log(user);
            } else
            {
                window.location.pathname = '/admin/';
            }
        });
    } else if (location.startsWith('/admin/'))
    {
        $.ajax({
            url:"/ajax/v1.0/get-auth-data/",
            type:"get",
            success: function(data)
            {
                if (data["is_admin"])
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
                    window.location.pathname = "/admin/authenticate/ua/";
                } //check if user is an admin
            }
        });// get the data of the authenticated user
    }
} else
{
    let location = window.location.pathname;
    if (!(notAllowedUrl.find(t => {return t == location})))
    {
        window.location.pathname = "/login/";// redirect users to the login page
    } else if (location == '/admin/')
    {
        window.location.pathname = '/admin/authenticate/ua/';
    } else
    {
        console.log("Not auth");
    }// redirects user is they are not yet authenticated
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
        $(".usp").hide(1);//hides the views not allowed for authenticated users
        $(".auth").show(1);//shows the views allowed for authenticated users
    }else{
        $(".usp").show(1);//vice versa
        $(".auth").hide(1);//vice versa
    }
    hideLoader();
    if(window.location.pathname == "/login/")
    {
        $(".bio-data").css({display: null});
    }//remove the bio data form from login
    if (window.location.pathname.startsWith('/admin/'))
    {
        $(".core").on('click', function () {
            $('.n').toggleClass('b-ul');
            $('span.carat').toggleClass("c-r");
        });
        $(".a-o").on('click', function () {
            $('.c').toggleClass('c-ul');
            $('span.a-carat').toggleClass("c-r");
        });
    }//only create this event its the admin page
});
