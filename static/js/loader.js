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
            break;
        case ('/admin/grade-add/'):
        	loadScript("/static/js/gp.js/");
        	$('title').text('Grade Point');
        	break;
        case ('/admin/add-form/'):
        	$('title').text('Add Lasustech course');
        	break;

    }

});