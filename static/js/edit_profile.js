$.ajax({
    url: "/ajax/v1.0/get-auth-data/",
    type: "get",
    success: function (data)
    {
        $(".name").text(`${data["username"]}`);
        $("#first_name").val(data["first_name"]);
        $("#last_name").val(data["last_name"]);
        $("#email").val(data["email"]);
        $("#username").val(data["username"]);
        $("#middle_name").val(data["mid_name"]);
        $(".form-img").attr('src', `/static/img/${data["img_path"]}/`);
    },
    error: function () {
        naShowAlert("Sorry, an error seems to have occured !", "danger");
    }
});

$("#img").on("change", function(et)
{
    const [files] = $(this).prop('files');

    if (files)
    {
        $(".form-img").attr("src", URL.createObjectURL(files));
    }
    
});

$(".usr").on('click', function (e)
{
    let form = $(this).parent();
    let formData = {};
    form.find('input').each(
        function (...args) {
            let cu = $(args[1]);
            if (cu.attr('type') != 'submit')
                formData[cu.attr('name')] = cu.val();
        }
    );//gets each form input element
    formData = JSON.stringify(formData);
    $.ajax({
        url: `${window.location.pathname}`,
        type: "POST",
        data: formData,
        contentType: "application/json",
        success: function(data){
            console.log(data);
        }
    });
});
$(".bbio").on('click', function (e) {
    let form = $(this).parent().serialize();
    // let formData = {};
    // form.find('input').each(
    //     function (...args) {
    //         let cu = $(args[1]);
    //         if (cu.attr('type') != 'submit')
    //             formData[cu.attr('name')] = cu.val();
    //     }
    // );//gets each form input element
    // formData = JSON.stringify(formData);
    console.log(form);
    $.ajax({
        url: `/edit/profile/bio/data/`,
        type: "POST",
        data: form,
        success: function (data) {
            console.log(data);
        }
    });
});
$(".ff").on('submit', function (e)
{
    $.getJSON("/ajax/v1.0/get-auth-data/", function (data)
    {
        let fd = new FormData();
        fd.append('img', $("#img")[0].files[0]);
        fd.append('csrf_token', $("#csrf_token").val());
        $.ajax({
            url: `/edit/profile/image/${data["id"]}/`,
            type: "POST",
            data: fd,
            contentType: false,
            processData: false,
            cache: false,
            success: function (data)
            {
                alert(data["msg"]);
            }
        });
    });// gets user id
});// the upload event handler

