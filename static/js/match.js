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
            class:"bg-success card pt-3 p-3 mt-4 text-light",
        id:"agg"});
    }
    let field=$("#field1").prepend(aggregate);
});