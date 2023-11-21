const getProcessed = function(page=1){
    let processed = $('.processed-documents');
	let p = $("<p></p>");
	$.ajaxSetup({cache: false});
	$.getJSON(`/ajax/v1.0/view-processed-file/?page=${page}`, function(data){
		let file = data['files'];
		if ($('.ccpdc').html()){
			$('.ccpdc').html('');
		}
	    if (file)
	    {
	    	for (let student of file)
	    	{
	    		let tr = $("<tr></tr>");
	    		tr.append($(`<td align='center'>${student['Full Name']}</td>`));
	    		tr.append($(`<td align='center'>${student['Jamb']}</td>`));
	    		tr.append($(`<td align='center'>${student['Course']}</td>`));
	    		tr.append($(`<td align='center'>${student['subject1']}</td>`));
	    		tr.append($(`<td align='center'>${student['grade1']}</td>`));
	    		tr.append($(`<td align='center'>${student['subject2']}</td>`));
	    		tr.append($(`<td align='center'>${student['grade2']}</td>`));
	    		tr.append($(`<td align='center'>${student['subject3']}</td>`));
	    		tr.append($(`<td align='center'>${student['grade3']}</td>`));
	    		tr.append($(`<td align='center'>${student['subject4']}</td>`));
	    		tr.append($(`<td align='center'>${student['grade4']}</td>`));
	    		tr.append($(`<td align='center'>${student['subject5']}</td>`));
	    		tr.append($(`<td align='center'>${student['grade5']}</td>`));
	    		tr.append($(`<td align='center'>${student['score']}%</td>`));
	    		tr.append($(`<td align='center'>${student['Qualified']}</td>`));
	    		tr.append($(`<td align='center'>${student['Why']}</td>`));
	    		$('.ccpdc').append(tr);
	    	}
	    } else
	    {
	    	p.text("You haven't processed any file yet");
	    	processed.html(p);
	    }
	    $('.next').attr('disabled', !data['has_next']);
	    $('.prev').attr('disabled', !data['has_prev']) ;
	});
}
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
						showAlert(data['msg'][0], data['msg'][1]);
					}
				});
		    },
		    error: function () {
		        naShowAlert("Sorry, an error seems to have occured !", "danger");
		    }
		});
	}
});
$(".processed").on("click", ()=>{
	let processed = $('.processed-documents');
	processed.toggleClass('spd');
	getProcessed()
});
let page = 1;
$('.prev').click(function(){
	page--;
	getProcessed(page);
});

$('.next').click(function(){
	page++;
	getProcessed(page);
});

$('.pclose').click(function(){
	$('.processed-documents').toggleClass('spd');
})