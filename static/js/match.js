"use strict";

//data storage space
let jamb=document.getElementById('jamb_score');
let btn=document.getElementById('submit');
let form=document.getElementsByTagName('form')[0];
let grade1=document.getElementById('grade_1');
let grade2=document.getElementById('grade_2');
let grade3=document.getElementById('grade_3');
let grade4=document.getElementById('grade_4');
let grade5=document.getElementById('grade_5');
let grade6=document.getElementById('grade_6');
let grade7=document.getElementById('grade_7');

let toInt=(a)=>
{
    return Number.parseInt(a);
}
let calculator=(...args)=>
{
    return (args.reduce(sum)+(jamb.value*0.15)).toFixed(2);
}

let sum=(a, b)=>{
    return (toInt(a)+toInt(b));
}
//Updating for aggregate data
form.addEventListener('submit',function(e)
{
    e.preventDefault();//Stop The Form Default Action
    let score=calculator(grade1.value, grade2.value, grade3.value,
     grade4.value,
      grade5.value);
    console.log(score);
    let aggregate = $('#agg');
    if ($("#agg").html() !== undefined)
    {
        let code = aggregate.children('code');
        code.attr("class","text-info");
        code.first().text(score+"%");
    }else
    {
        aggregate=$("<span>Aggregate: <code>"+score+"%</code></span>");
        aggregate.attr({
            class:"alert-primary alert card pt-3 p-3 mt-4 text-dark",
        id:"agg"});
    }
    let field=$("#form").prepend(aggregate);
});
//Querying for course data
$("#course_name").on('input',function(){
    let c = $(this).val()
    $.getJSON(
        `/course/?c=${c}`,
        function(data)
        {
            let subject = data["subject"];
            let span = "<ul>Subject: ";
            let ali = "";
            for (let i = 0; i <= subject.length-1; i++){
                let li = "\n<li style='display:inline;'>" + subject[i] + "</li>"
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
               subj.attr({
                    class:"bg-info card pt-3 pl-3 pb-3 text-dark mt-3",
                id:"sub", display:"inline"});
               return '';
            }else
            {
                subj=$(span);
                subj.attr({
                    class:"alert alert-primary card pt-3 pl-3 pb-3 text-dark mt-3",
                id:"sub", display:"inline"});
                let field=$("#form").prepend(subj);
                return '';
            }
            $("li").each(function(){
                $("this").attr({
                    "style": "display:inline;"
                })});
        }
    );
})