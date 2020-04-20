$( document ).ready(function() {
    $("#btnResult").on("click", function() {
        getEventTimeWithSpeed($("#speedInput").val(), $("#targetEventInput").val());
        // $("<p>")
        //     .text($("#speedInput").val())
        //     .addClass("crocodile")
        //     .appendTo("#divResult");
    });

    $("#speedInput").on("keydown", function(event) {
        startSpeedInputKeyDownTimer();
    });

    $("#targetEventInput").on("keydown", function(event) {
        startTargetEventInputKeyDownTimer();
    });

    enableResultBtnIfNeeded();
});

function enableResultBtnIfNeeded() {
    const enable = ($("#divParsedSpeed").text() !== "" && $("#divParsedTargetEvent").text() !== "");
    $("#btnResult").prop('disabled', !enable); 
}

function getEventTimeWithSpeed(iSpeedStr, iEventStr) {
    const queryData = {speedStr: iSpeedStr, eventStr: iEventStr};
    queryAPINameWithData("getEventTimeWithSpeed", queryData)
        .then((data) => {
            if (data.exitcode === 0) {
                $("#divResult").text(getStrFromTimeObj(data.data));
            } else {
                console.log("got this back: " + data.data);
                $("#divParsedTargetEvent").text("");
            }
        });
}

function getStrFromTimeObj(timeObj) {
    const time = timeObj.time;
    const timeUnit = timeObj.unit;
    return time + " " + timeUnit;
}

var speedInputTimer;
var targetEventInputTimer;
const timerWaitTime = 250;

function startSpeedInputKeyDownTimer() {
    clearTimeout(speedInputTimer)
    speedInputTimer = setTimeout(function() {
        var fullStr = $("#speedInput").val();
        doAttemptParseSpeedStr(fullStr);
    }, timerWaitTime);
}

function startTargetEventInputKeyDownTimer() {
    clearTimeout(targetEventInputTimer)
    targetEventInputTimer = setTimeout(function() {
        var fullStr = $("#targetEventInput").val();
        doAttemptParseTargetEventStr(fullStr);
    }, timerWaitTime);
}

function getStrFromSpeedObj(speedObj) {
    const distance = speedObj.event.distance;
    const distanceUnit = speedObj.event.unit;
    const time = speedObj.time.time;
    const timeUnit = speedObj.time.unit;
    return distance + " " + distanceUnit + " per " + timeUnit;
}

function doAttemptParseSpeedStr(speedStr) {
    parseSpeedStr(speedStr)
        .then((data) => {
            if (data.exitcode === 0) {
                $("#divParsedSpeed").text(getStrFromSpeedObj(data.data));
            } else {
                $("#divParsedSpeed").text("");
            }

            enableResultBtnIfNeeded();
        });
};

async function parseSpeedStr(iSpeedStr) {
    const queryData = {speedStr: iSpeedStr};
    return await queryAPINameWithData("parseSpeedStr", queryData);
}

function getStrFromEventObj(eventObj) {
    const distance = eventObj.distance;
    const distanceUnit = eventObj.unit;
    return distance + " " + distanceUnit;
}

function doAttemptParseTargetEventStr(targetEventStr) {
    parseTargetEventStr(targetEventStr)
        .then((data) => {
            if (data.exitcode === 0) {
                $("#divParsedTargetEvent").text(getStrFromEventObj(data.data));
            } else {
                $("#divParsedTargetEvent").text("");
            }

            enableResultBtnIfNeeded();
        });
}

async function parseTargetEventStr(targetEventStr) {
    const queryData = {eventStr: targetEventStr};
    return await queryAPINameWithData("parseEventStr", queryData);
}

function toQueryStr(object) {
    var esc = encodeURIComponent;
    var query = Object.keys(object)
        .map(k => esc(k) + '=' + esc(object[k]))
        .join('&');
    return query;
}

async function queryAPINameWithData(apiName, data) {
    hostName = "http://127.0.0.1:5000//api/";
    apiVersion = "v1.0/";
    const url = hostName + apiVersion + apiName + "?" + toQueryStr(data);
    const response = await fetch(url, {
        method: "GET"
    });
    return response.json();
}