alert("Exception");
jQuery("form").on('submit', function(){
	let formObj = $(this);
	let csrf_token = $('#csrf_token').val();
	let name = $('#name').val();
	let jamb_reg = $('#jamb_reg').val();
	let formData = {};
	formData['name'] = name;
	formData['jamb_reg'] = jamb_reg;
	formData['csrf_token'] = csrf_token;
	jQuery.ajax({
		url: `/ajax/v1.0/admin/students-exception/`,
		type: 'POST',
		data: JSON.stringify(formData),
		headers: {'X-CSRFToken': csrf_token, 'Content-Type': "application/json"},
		beforeSend: (xhr) => {
			//j
		},
		success: (data, textStatus, jqXHR)=>{
			showAlert(data['msg'], data['status']);
		}
	})
});