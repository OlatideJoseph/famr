//data storage space
function recommend(arr, score, course = ''){
    let objSub = {
        "subjects": arr,
        "score": score
    }

    jQuery.ajax({
        url: '/ajax/v1.0/recommend-courses/',
        type: 'POST',
        headers: {"Content-Type": "application/json", "X-CSRFToken": $('#csrf_token').val()},
        data: JSON.stringify(objSub),
        success: (data, textStatus, jqXhr) => {
            if (data['status'] === 'success'){
                let rec_cour = []
                const results = data['results'];
                results.forEach((e) => {rec_cour.push(e.Name)});
                if (rec_cour.includes(course)) showAlert("You passed Gracefully", 'success');
                showAlert(rec_cour.join(', '), 'warning');
            } else {
                showAlert(data['msg'], 'danger');
            }
        }
    })
}
$(".bio-data").css("display", "block");
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
$.getJSON("/ajax/v1.0/get-course-data/", function(data){
    for (let i=0; i<data.length; i++){
        let d = data[i]; // holds the value and name for the option taken
        if (d)
        {
            let option = $(`<option value="${d[0]}">${d[1]}</option>`);
            $("select[id^='course']").append(option);
        }
    }
    
});
$.getJSON("/ajax/v1.0/get-subject-data/", function(data){
    for (let i=0; i<data.length; i++){
        let d = data[i]; // holds the value and name for the option taken
        if (d)
        {
            let option = $(`<option value="${d[0]}">${d[1]}</option>`);
            $("select[id^='field']").append(option);
        }
    }    
});//gets necessary data
let img = document.createElement('img');
const onEvent = ()=>
{
    //Updating for aggregate data
    $('img').on("click", function (_e)
    {
        let t = $(this);
        let css = { display: "flex" };
        let attr = { src: t.attr('src'), alt: t.attr('alt') }
        if (attr["src"])
        {
            $(".img-modal").css(css);
            $(".selected-img").attr(attr);
        }
        $('#circled').on("click", function (_e)
        {
            $('.img-modal').css("display", "none");
        });
    });

    $('#submit').off('click');
    $('#submit').on('click', function (e)
    {
        let course = $('#course_name').val();
        let jamb = document.getElementById('jamb_score');
        let btn = document.getElementById('submit');
        let grade1 = document.getElementById('grade_1');
        let grade2 = document.getElementById('grade_2');
        let grade3 = document.getElementById('grade_3');
        let grade4 = document.getElementById('grade_4');
        let grade5 = document.getElementById('grade_5');
        let grade6 = document.getElementById('grade_6');
        let grade7 = document.getElementById('grade_7');
        let subjects = new Array();
        let toInt = (a) =>
        {
            return Number.parseInt(a);
        }
        let calculator = (...args) =>
        {
            return (args.reduce(sum) + (jamb.value * 0.15)).toFixed(2);
        }

        let sum = (a, b) =>
        {
            return (toInt(a) + toInt(b));
        }

        $('select[id^="fie"]').each((n, e) => subjects.push($(e).val()));
        e.preventDefault();//Stop The Form Default Action
        let score = calculator(grade1.value, grade2.value, grade3.value,
            grade4.value,
            grade5.value);
        if (score){
            let field1 = $('#field1').val();
            let field2 = $('#field2').val();
            let field3 = $('#field3').val();
            let field4 = $('#field4').val();
            let field5 = $('#field5').val();
            let arr = [field1, field2, field3, field4, field5];
            recommend(arr, score, course);
        }
        $.getJSON(
            `/course/?c=${course}`,
            function (data)
            {
                let csubjects = data["subject"];
                for (csub in csubjects)
                {
                    let sub = Object.keys(csubjects[csub])[0];
                    if (sub)
                    {
                        if (!subjects.includes(sub))
                        {
                            showAlert(`${course} does not require Subject ${sub}`, "danger");
                        }
                    }
                }
            }
        );
    });
    $('.rr-close').off('click');
    $('.rr-close').on('click', function(){
        $('.rr').toggleClass('rr-show');
    });

}
$.ajax({
    url: "/ajax/v1.0/get-auth-data/",
    type: "get",
    success: function (data) {
        $(".email").text(data["email"]);
        $(".first").text(data["first_name"]);
        $(".last").text(data["last_name"]);
        $(".mid").text(data["mid_name"]);
        $(".dob").text(data["dob"]);
        $(".bio-img").attr('src', `/static/img/${data["img_path"]}/`);
        img.src = `/static/img/${data["img_path"]}/`;
        img.alt = 'user-img';
        img.className = "bio-img";
    },
    error: function () {
        naShowAlert("Sorry, an error seems to have occured !", "danger");
    }
});

$(document).ajaxComplete(function()
{
    $("#submit").off("submit");
    onEvent();
});
