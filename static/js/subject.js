const validator = () =>
{
    let subject = $('#name');
    let span = $('<span></span>');
    if (!subject.val())
    {
        subject.addClass('is-valid');
        span.addClass('invalid-feedback');
        span.text('Inputted value cannot be empty !');
        subject.after(span);
        return false;
    }
    return true;
}
$('form').on('submit', function(e){
    "use strict";
    e.preventDefault();
    let formData = JSON.stringify({"subject": [$('#name').val()]});
    if (validator())
    {
        $.ajax({
            url: `/ajax/v1.0/admin/add-subject-waec/`,
            type: "POST",
            contentType: "application/json",
            data: formData,
            success: function(data, textStatus, jqXHR)
            {
                showAlert(data['msg'][0], data['msg'][1]);
                console.log(data);
            },
            error: function(){
                console.log("An error occured");
            }
        });
    }
});