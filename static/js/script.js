$( document ).ready(function() {

    $("#btnResult").on("click", function() {
        console.log("Wheeee!");
        $("<p>")
            .text("The crocodiles have eaten this ENTIRE PAGE!")
            .addClass("crocodile")
            .appendTo("#divResult");
    });

    $("#speedInput").on("keydown", function(event) {
        // At the time of the event, the input does not have the
        // key that was just pressed, which is why we append it here
        var fullStr = $("#speedInput").val() + event.key;
        isSpeedStrReadyForParsing(fullStr);
    });
});

var isSpeedStrReadyForParsing = function(speedStr) {
    console.log("called is ready for parsing with " + speedStr);
};