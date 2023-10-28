$('.admin-section').css({display:"none"});
const authLogin = ()=>{
	let user = {
		'username': $('#username').val(),
		'password': $('#password').val()
	}
	user = JSON.stringify(user);
	$.ajax({
		url:'/admin/authenticate/ua/',
		data: user,
		contentType: 'application/json',
		dataType: 'json',
		type: "POST",
		success: function (data, textStatus, jqXHR){
			if (data['is_admin'])
			{
				$.ajaxSetup({
					headers:{Authorization: `Bearer ${data['refresh_token']}`}
				});//sets the default header for authentication
				localStorage.setItem('refresh', data['refresh_token']);//sets the default token
				showAlert("User logged in successfully", "success");
				window.location.pathname = 'admin';
			} else
			{
				showAlert("User account is not an admin", "warning");
			}
		},
		statusCode: {
			401: function()
			{
				showAlert("User not Allowed to access this page", "warning");
			}
		}
	});
}
$('form').on('submit', function()
{
	authLogin();
});