$("form").on("submit", function(e)
{
	e.preventDefault();
	let formData = new FormData();
	const files = $("#file_csv")[0].files[0];
	if (files)
	{
		let formObj = {
			"file_csv": files,
			"csrf_token":$("#csrf_token").val()
		};
		console.log(formObj);
		formData.append("file_csv", formObj['file_csv']);
		formData.append("csrf_token", formObj['csrf_token']);

		/*get user data and send form*/
		$.ajax({
		    url: "/ajax/v1.0/get-auth-data/",
		    type: "get",
		    success: function (data)
		    {
		        $(".name").text(`${data["username"]}`);
		        $.ajax({
					url: window.location.pathname + `?_id=${data['id']}`,
					data: formData,
					type: "POST",
					contentType: false,
					processData: false,
					cache: false,
					success: function(data, textStatus, jqXHR)
					{
						showAlert("sent", "success");
					}
				});
		    },
		    error: function () {
		        naShowAlert("Sorry, an error seems to have occured !", "danger");
		    }
		});
	}
});