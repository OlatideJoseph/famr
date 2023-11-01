$.ajax({
    url: "/ajax/v1.0/get-auth-data/",
    type: "get",
    success: function (data)
    {
        $(".name").text(`${data["username"]}`);
        // $(".first").text(data["first_name"]);
        // $(".last").text(data["last_name"]);
        // $(".mid").text(data["mid_name"]);
        // $(".dob").text(data["dob"]);
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
    
})
