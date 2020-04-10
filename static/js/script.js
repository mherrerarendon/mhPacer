$( document ).ready(function() {

    $("#btnResult").on("click", function() {
        console.log("Wheeee!");
        $("<p>")
            .text($("#speedInput").val())
            .addClass("crocodile")
            .appendTo("#divResult");
    });

    $("#speedInput").on("keydown", function(event) {
        startSpeedInputKeyDownTimer();
    });
});

var speedInputTimer;

function startSpeedInputKeyDownTimer() {
    clearTimeout(speedInputTimer)
    speedInputTimer = setTimeout(function() {
        var fullStr = $("#speedInput").val();
        doAttemptParseSpeedStr(fullStr);
    }, 250);
}

function getStrFromSpeedObj(speedObj) {
    const distance = speedObj.distance;
    const distanceUnit = speedObj.distanceUnit;
    const time = speedObj.time;
    const timeUnit = speedObj.timeUnit;
    return distance + " " + distanceUnit + " per " + timeUnit;
}

function doAttemptParseSpeedStr(speedStr) {
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

function toQueryStr(object) {
    var esc = encodeURIComponent;
    var query = Object.keys(object)
        .map(k => esc(k) + '=' + esc(object[k]))
        .join('&');
    return query;
}

// http://127.0.0.1:5000//api/v1.0/parseSpeedStr?speedStr=10kph
async function parseSpeedStr(iSpeedStr) {
    const queryData = {speedStr: iSpeedStr};
    const url = "http://127.0.0.1:5000//api/v1.0/parseSpeedStr?" + toQueryStr(queryData);
    console.log(url);
    const response = await fetch(url, {
        method: "GET"
    });
    return response.json();
}