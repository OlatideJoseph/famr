"use strict";
showLoader();
let slocation = window.location.pathname;
getHtml(`/ajax/v1.0${slocation}`);
hideLoader('Match', '/match-course/');
$(window).load(function(){
	let href = "/ajax/v1.0" + window.location.pathname;
	$("form").on("submit", function()
	{
		e.preventDefault();
	}
	);
});