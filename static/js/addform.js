//data storage space
// eventNavLink();
showLoader();
getHtml(`/ajax/v1.0${window.location.pathname}`);
hideLoader('Register Course', '/add-form/');
$(window).on("load",function(){
    $(".nav-link").click(function(e){
        e.preventDefault();//Stops the default action of the page
        getAndChangePageFunction($(this).attr('href'));

    });
    $("form").on("submit", function(e){
        e.preventDefault();
    });
});