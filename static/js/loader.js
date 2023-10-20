showLoader();
getHtml(`/ajax/v1.0${window.location.pathname}`);
hideLoader('Add Subjects', window.location.pathname);


$(window).on('load',function()
{
    if(window.location.pathname == "/login/")
    {
        $(".bio-data").css({display: null});
    }//remove the bio data form from login
    switch (window.location.pathname)
    {
        case ('/admin/add-subject-waec/'):
            loadScript("/static/js/subject.js/");

    }

});