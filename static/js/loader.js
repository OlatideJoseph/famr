showLoader();
getHtml(`/ajax/v1.0${window.location.pathname}`);
hideLoader('Add Subjects', window.location.pathname);