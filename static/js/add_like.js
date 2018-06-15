$(document).on('click', '[id^="addLike_"]', function() {
    var wish_id=$(this).attr('id').split('_')[1]
    $.ajax({
        url: '/addLike',
        method: 'POST',
        data: {
            wish_id: wish_id,
        },
        success: function(response, data) {
            console.log(response);
            var obj = JSON.parse(response);
            $("#likes_"+wish_id).html(obj.num_of_likes);
        },
        error: function(error) {
            console.log(error);
        }
    });
});