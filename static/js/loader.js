showLoader();
getHtml(`/ajax/v1.0${window.location.pathname}`);
hideLoader('Add Subjects', window.location.pathname);


$(window).on('load',function()
{
    switch (window.location.pathname)
    {
        case ('/admin/add-subject-waec/'):
            loadScript("/static/js/subject.js/");
            $('title').text('Add Subjects');
            $('.current').toggleClass('current');
            $('.subject').toggleClass('current');
            break;
        case ('/admin/grade-add/'):
        	loadScript("/static/js/gp.js/");
        	$('title').text('Grade Point');
            $('.current').toggleClass('current');
            $('.gp').toggleClass('current');
        	break;
        case ('/admin/add-form/'):
            loadScript("/static/js/addform.js/");
        	$('title').text('Add Lasustech course');
            $('.current').toggleClass('current');
            $('.course').toggleClass('current');
        	break;
        case ('/admin/authenticate/'):
            $('title').text('Admin | Authenticate');
            loadScript("/static/js/admin/auth.js/");
            break;
        case ('/match-course/'):
            $('title').text('Match and Find');
            loadScript("/static/js/match.js/");
            break;
    }

});