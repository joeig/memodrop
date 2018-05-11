$(document).ready(function(){
    $("#braindump #show-hint").click(function() {
        $("#braindump #hint").show();
        $(this).addClass("disabled");
    });

    $("#braindump #show-answer").click(function() {
        $("#braindump #answer").show();
        $(this).addClass("disabled");
    });
});
