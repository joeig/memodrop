$("#braindump #show-hint").click(function() {
    $("#braindump #hint").show();
    $(this).attr("disabled", "disabled");
});

$("#braindump #show-answer").click(function() {
    $("#braindump #answer").show();
    $(this).attr("disabled", "disabled");
});