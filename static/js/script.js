$( document ).ready(function() {
    $("#speedInput").on("keydown", function(event) {
        startSpeedInputKeyDownTimer();
    });

    $("#targetEventInput").on("keydown", function(event) {
        startTargetEventInputKeyDownTimer();
    });
});

function displayResultIfNeeded() {
    const enable = ($("#divParsedSpeed").text() !== "" && $("#divParsedTargetEvent").text() !== "");
    if (enable) {
        getEventTimeWithSpeed($("#speedInput").val(), $("#targetEventInput").val());
    } else {
        $("#divResult").text("");
    }
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

function doAttemptParseSpeedStr(iSpeedStr) {
    const queryData = {speedStr: iSpeedStr};
    queryAPINameWithData("parseSpeedStr", queryData)
        .then((data) => {
            if (data.exitcode === 0) {
                $("#divParsedSpeed").text(getStrFromSpeedObj(data.data));
            } else {
                $("#divParsedSpeed").text("");
            }

            displayResultIfNeeded();
        });
};


function doAttemptParseTargetEventStr(targetEventStr) {
    const queryData = {eventStr: targetEventStr};
    queryAPINameWithData("parseEventStr", queryData)
        .then((data) => {
            if (data.exitcode === 0) {
                $("#divParsedTargetEvent").text(getStrFromEventObj(data.data));
            } else {
                $("#divParsedTargetEvent").text("");
            }

            displayResultIfNeeded();
        });
}
