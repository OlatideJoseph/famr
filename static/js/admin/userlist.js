$(document).ready(function ()
{
    let page = 0;
    const getPageList = function(page)
    {
        $.getJSON(`/ajax/v1.0/get-user-all-data?page=${page}`, function (data)
        {
            $('.user-list').html('');
            for (let key of Object.keys(data))
            {
                if (typeof data[key] === "object")
                {
                    console.log(typeof data[key]);
                    let paraCss = { "cursor": "pointer" };
                    let p = `<p><small>${data[key]['username']}</small>|`;
                    p += `<small>${data[key]['first_name']}</small> |`;
                    p += `<small>${data[key]['last_name']}</small> |`;
                    p += `<small>${data[key]['email']}</small>`;
                    p = $(`${p}</p>`);
                    p.css(paraCss);
                    p.addClass("user-item");
                    $('.user-list').append(p);
                    p.after('<hr/>');
                }
            }
            let prevVal = data['prev'];
            if (data['next']){
                $('.next').attr('disabled', false);
                $('.previous').attr('disabled', !prevVal);
            } else
            {
                $('.next').attr('disabled', true);
                $('.previous').attr('disabled', !prevVal);
            }
        });
    }
    getPageList(++page);
    $('.previous').on('click', function(){
        page--;//decrease the page value
        if (page > 0)
        {
            getPageList(page);
        }
    });
    $('.next').on('click', function () {
        page++;//increase the page number
        if (page >= 0) {
            getPageList(page);
        }
    });
});