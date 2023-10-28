$.ajax({
    url:"/ajax/v1.0/get-auth-data/",
    type:"get",
    success:function(data){
        console.log(data);
        $(".username").text(data["username"]);
        $(".real").text(
            data["first_name"] + " " + data["last_name"] + " " + data["mid_name"]
        );
        // $(".last").text();
        // $(".mid").text(data["mid_name"]);
        $(".age").prepend(data["age"]);
    }
});