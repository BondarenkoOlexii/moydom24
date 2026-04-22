$(document).ready(function(){
    $('.btn-tab-switch').click(function(e){
        console.log("Все працює")
        e.preventDefault(); // щоб сторінка не пригала вверх

        let targetId = $(this).attr('href');

        $('.nav-tabs li').removeClass('active');
        $(this).parent('li').addClass('active');
        $('.tab-pane').removeClass('active').hide();

        $(targetId).addClass('active').fadeIn();
    })


})