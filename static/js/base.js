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
let token = localStorage.getItem("refresh");
if (token){
    $.ajaxSetup({
        headers:{Authorization: `Bearer ${localStorage.getItem("refresh")}`}
    });
    $('#content').load("/ajax/v1.0/match-course/ #content", function(data)
    {
        showAlert("Already Logged In", "info");
    }
    );

}else
{ 
    if (window.location.pathname !== "/login/" && window.location.pathname !== "/sign-up/")
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
    let bloader = $('.bloader');
    bloader.css('display', 'flex');
    body.css('overflow','hidden');
    content.hide();
}

const hideLoader = (title, url)=>{
    let bloader = $('.bloader');
    let content = $("#content");
    let body = $("body");
    $('title').text(title);
    bloader.fadeOut(1000);
    content.show();
    body.css('overflow','auto');
    window.history.pushState(null, null, url);
}
const linkOpener = (tag)=>{
$(tag).on('click',
    function(e)
    {
        showLoader();
        let href = $(this).attr('href');
        e.preventDefault();
        if ((href !== "/sign-up/") && (href !== "/login/"))
        {
            $('body').load(`/ajax/v1.0${href} #content`, function(data)
            {
                hideLoader($(this).text(), href);
            }
            );
        }else
        {
            $('#body').load(`${href} #content`, function(data)
            {
                hideLoader($(this).text(), href);
            }
            );
        }       
    }
);
}

    // const showAlert = (msg, category)=>{
    //     let alert = `<p class="alert alert-${category} `
    //     alert += `alert-dismissible mt-2 mb-2 pl-3 pl- fade show">${msg}`
    //     alert += `<span class="btn-close" data-bs-dismiss="alert"`
    //     alert += ` aria-label="Close">&times</span></p>`;
    //     // $("#loader").fadeOut(500);
    //     $("nav").after(alert);
    // }