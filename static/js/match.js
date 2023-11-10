//data storage space

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


    $('#submit').on('click', function (e)
    {
        let jamb = document.getElementById('jamb_score');
        let btn = document.getElementById('submit');
        let grade1 = document.getElementById('grade_1');
        let grade2 = document.getElementById('grade_2');
        let grade3 = document.getElementById('grade_3');
        let grade4 = document.getElementById('grade_4');
        let grade5 = document.getElementById('grade_5');
        let grade6 = document.getElementById('grade_6');
        let grade7 = document.getElementById('grade_7');


        let toInt = (a) => {
            return Number.parseInt(a);
        }
        let calculator = (...args) => {
            return (args.reduce(sum) + (jamb.value * 0.15)).toFixed(2);
        }

        let sum = (a, b) => {
            return (toInt(a) + toInt(b));
        }
        e.preventDefault();//Stop The Form Default Action
        let score = calculator(grade1.value, grade2.value, grade3.value,
            grade4.value,
            grade5.value);
        console.log(score);
        let aggregate = $('#agg');
        if ($("#agg").html() !== undefined)
        {
            let code = aggregate.children('code');
            code.attr("class", "text-info");
            code.first().text(score + "%");
        } else
        {
            aggregate = $("<span>Aggregate: <code>" + score + "%</code></span>");
            aggregate.attr({
                class: "alert-primary alert card pt-3 p-3 mt-4 text-dark",
                id: "agg"
            });
        }
        let field = $("#form").prepend(aggregate);
        let c = $("#course_name").val();

        $.getJSON(
            `/course/?c=${c}`,
            function (data)
            {
                let subject = data["subject"];
                let span = "<ul>Subject: ";
                let ali = "";
                for (let i = 0; i <= subject.length - 1; i++)
                {
                    let li = "\n<li>" + Object.keys(subject[i])[0] + "</li>"
                    ali += li;
                }
                span += ali;
                span += "</ul>";
                console.log(subject);
                console.log(span);
                let subj = $('#sub');
                if ($("#sub").html() !== undefined)
                {
                    subj.html(span);
                } else {
                    subj = $(span);
                    subj.attr({
                        class: "bg-primary card pt-3 pl-3 pb-3 text-dark mt-3",
                        id: "sub", display: "inline"
                    });
                    let field = $("#form").prepend(subj);
                    return '';
                }
                subj.attr({
                    class: "bg-primary card pt-3 pl-3 pb-3 text-dark mt-3",
                    id: "sub", display: "inline"
                });
            }
        );
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
setInterval(() => {
    onEvent();
}, 3000);