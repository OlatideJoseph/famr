$('.sub').on('click', function(e){
    e.preventDefault();
    let formData = JSON.stringify({"subject": [$('#name').val()]});
    alert("Hello");
    $.ajax({
        url: `/ajax/v1.0/admin/add-subject-waec/`,
        type: "POST",
        contentType: "application/json",
        data: formData,
        success: function(data, textStatus, jqXHR)
        {
            showAlert(data['msg'], data['status']);
            console.log(data);
        },
        error: function(){
            console.log("An error occured");
        }
    });
});