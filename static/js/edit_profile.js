$.ajax({
    url: "/ajax/v1.0/get-auth-data/",
    type: "get",
    success: function (data) {
        $(".name").text(`${data["username"]} Image`);
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
