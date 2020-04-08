$( document ).ready(function() {

    $("#btnResult").on("click", function() {
        console.log("Wheeee!");
        $("<p>")
            .text($("#speedInput").val())
            .addClass("crocodile")
            .appendTo("#divResult");
    });

    $("#speedInput").on("keydown", function(event) {
        // At the time of the event, the input does not have the
        // key that was just pressed, which is why we append it here
        var fullStr = $("#speedInput").val();
        if (isValidKeyCode(event.keyCode)) {
            fullStr += event.key;
        }
        isSpeedStrReadyForParsing(fullStr);
    });
});

function isValidKeyCode(keyCode) {
    return keyCode > 32 && keyCode < 127;
}

var getStrFromSpeedObj = function(speedObj) {
    const distance = speedObj.distance;
    const distanceUnit = speedObj.distanceUnit;
    const time = speedObj.time;
    const timeUnit = speedObj.timeUnit;
    return distance + " " + distanceUnit + " per " + timeUnit;
}

var isSpeedStrReadyForParsing = function(speedStr) {
    console.log("called is ready for parsing with " + speedStr);
    parseSpeedStr(speedStr)
        .then((data) => {
            if (data.exitcode === 0) {
                $("#divParsedSpeed").text(getStrFromSpeedObj(data.data));
            } else {
                console.log("got this back: " + getStrFromSpeedObj(data.data)); // JSON data parsed by `response.json()` call
                $("#divParsedSpeed").text("");
            }
        });
};

// http://127.0.0.1:5000//api/v1.0/parseSpeedStr?speedStr=10kph
async function parseSpeedStr(speedStr) {
    const response = await fetch("http://127.0.0.1:5000//api/v1.0/parseSpeedStr?speedStr=" + speedStr, {
        method: "GET"
    });
    return response.json();
}