let f = document.querySelector('form');
$(document).ajaxComplete(function()
{
    $("form").off("submit");
    $("form").on('submit', function(e)
    {
        alert("hello");
        e.preventDefault();
        let form = $(this).serialize();
        $.ajax(
        {
            url: `/ajax/v1.0${window.location.pathname}`,
            type:"POST",
            contentType: "application/x-www-form-urlencoded",
            data:form,
            beforeSend: function(xhr, settings)
            {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain)
                {
                    xhr.setRequestHeader("X-CSRFToken", $("#csrf_token").val());
                }
                showLoader();
            },
            success: function(data, textStatus, jqXHR)
            {
                hideLoader();
                console.log(data);
                showAlert(data["msg"][0], data["msg"][1]);
            },
            error: function(data)
            {
                console.log(data.responseJSON);
                let resp = data.responseJSON;
                hideLoader("Login", "/login/");
                showAlert( resp["msg"][0], resp["msg"][1]);
            }
        });
    }
    );
});

