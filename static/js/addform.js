"use strict";
//data storage space
$(document).ready(function()
{
	showLoader();
	getHtml(`/ajax/v1.0${window.location.pathname}`);
	hideLoader('Register Course', '/add-form/');
	// eventNavLink();
}
);
