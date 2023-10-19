const authLogin = ()=>{
	let user = {
		'username': $('#username').val(),
		'password': $('#password').val()
	}
	user = JSON.stringfy(user);
	$.ajax({
		url:'/admin/authenticate/',
		data: user,
		contentType: 'application/json',
		dataType: 'json',
		type: "POST",
		success: function (data, textStatus, jqXHR){
			if (data['is_admin'])
			{
				$.ajaxSetup({
					headers:{Authorization: data['refresh_token']}
				});//sets the default header for authentication
				localStorage.setItem('refresh', data['refresh_token']);//sets the default token
				showAlert("User logged in successfully", "success");
			} else
			{
				showAlert("User account is not an admin", "warning");
			}
		}
	});
}
$('.login').on('submit', function()
{
	console.log("loading");
});