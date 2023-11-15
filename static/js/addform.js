$.getJSON("/ajax/v1.0/get-subject-data/", function(data){
    for (let i=0; i<data.length; i++){
        let d = data[i]; // holds the value and name for the option taken
        if (d)
        {
            let option = $(`<option value="${d[0]}">${d[1]}</option>`);
            $("select[id^='field']").append(option);
        }
    }
    
});
$.getJSON("/ajax/v1.0/get-grade-and-point/", function(data){
    for (let i=0; i<data.length; i++){
        let d = data[i]; // holds the value and name for the option taken
        if (d)
        {
            let option = $(`<option value="${d[0]}">${d[1]}</option>`);
            $("select[id^='grade']").append(option);
        }
    }
});
$(document).ajaxComplete(function()
{
    $("form").off("submit");
    $("form").on("submit", function(e){
        e.preventDefault();
        let formData = {};
        $(this).find('input').each(
            function(...args)
            {
                let cu = $(args[1]);
                if (cu.attr('type') != 'submit')
                    formData[cu.attr('name')] = cu.val();
            }
        );//gets each form in
        $(this).find('select').each(
            function(...args)
            {
                let cu = $(args[1]);
                formData[cu.attr('name')] = cu.val();
            }
        );
        console.log(formData);
        formData = JSON.stringify(formData);
        $.ajax({
            url: '/ajax/v1.0/admin/add-form/',
            type: "POST",
            data: formData,
            contentType: "application/json",
            beforeSend: function(xhr, settings)
            {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain)
                {
                    xhr.setRequestHeader("X-CSRFToken", $("#csrf_token").val());
                }
            },
            success: function(data)
            {
                showAlert(data["msg"], data["status"]);
            }
        });//add form url
    });
});