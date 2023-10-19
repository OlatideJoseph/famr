$.ajax({
    url:"/ajax/v1.0/get-auth-data/",
    type:"get",
    success:function(data){
        $('.ausr').text(data['username']);
    }
});