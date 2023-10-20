$.ajax({
    url:"/ajax/v1.0/get-auth-data/",
    type:"get",
    success:function(data){
        $('.ausr').text(data['username']);
    }
});//loads the user welcome message
$.ajax({
    url:"/admin/get-admin-data/",
    type:"get",
    success:function(data){
        $('.userno').text(data['usrno']);
    }
});