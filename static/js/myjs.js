 $(function () {
    $(window).resize(function () {
        var cliwidth = document.body.clientWidth;
        var cliheight = document.body.clientHeight;
        var divwidth = cliwidth - 2
        var divheight = cliheight - 2
        $('#resizeDiv').css("width", divwidth + "px");
        $('#resizeDiv').css("height", divheight + "px")
    })
})