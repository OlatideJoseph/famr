$(window).on("load",function(){
    $(".nav-link").click(function(e){
        e.preventDefault();//Stops the default action of the page
        getAndChangePageFunction($(this).attr('href'));
        $("title").text($(this).text());
    });
    $('.btn').on('click', function(){
        alert("hello");
    });
});