showLoader();
getHtml(`/ajax/v1.0${window.location.pathname}`);
hideLoader('Add Subjects', window.location.pathname);
$(window).on("load",function(){
    $(".nav-link").click(function(e){
        e.preventDefault();//Stops the default action of the page
        getAndChangePageFunction($(this).attr('href'));
        $("title").text($(this).text());
    });
});