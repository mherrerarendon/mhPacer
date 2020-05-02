$( document ).ready(function() {
    $("#speedPaceInput").on("keydown", function(event) {
        startSpeedPaceInputKeyDownTimer();
    });

    $("#targetEventInput").on("keydown", function(event) {
        startTargetEventInputKeyDownTimer();
    });

    $('#selectSpeedPace').change(function () {
        switch($(this).val()) {
        case 'selectSpeed':
            console.log("selected speed")
            break;
        case 'selectPace':
            console.log("selected pace")
            break;
        }
    })
});

function displayResultIfNeeded() {
    const enable = ($("#divParsedSpeedPace").text() !== "" && $("#divParsedTargetEvent").text() !== "");
    if (enable) {
        getEventTimeWithSpeed($("#speedPaceInput").val(), $("#targetEventInput").val());
    } else {
        $("#divResult").text("");
    }
}

var speedInputTimer;
var targetEventInputTimer;
const timerWaitTime = 250;

function startSpeedPaceInputKeyDownTimer() {
    clearTimeout(speedInputTimer)
    speedInputTimer = setTimeout(function() {
        var fullStr = $("#speedPaceInput").val();
        doAttemptParseSpeedPaceStr(fullStr);
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
                $("#divResult").text("Event time: " + getStrFromTimeObj(data.data));
            } else {
                console.log("got this back: " + data.data);
                $("#divParsedTargetEvent").text("");
            }
        });
}

function getApiNameAndQueryData(iSpeedPaceStr) {
    var apiName = null;
    var queryData = null;
    switch($("#selectSpeedPace").val()) {
        case 'selectSpeed':
            apiName = "parseSpeedStr";
            queryData = {speedStr: iSpeedPaceStr};
            break;
        case 'selectPace':
            apiName = "parsePaceStr";
            queryData = {paceStr: iSpeedPaceStr};
            break;
        }
    return [apiName, queryData];
}

function displaySpeedPaceStrings(data) {
    switch($("#selectSpeedPace").val()) {
        case 'selectSpeed':
            $("#divParsedSpeedPace").text(getStrFromSpeedObj(data.speed));
            $("#divConversion").text("Pace: " + getStrFromPaceObj(data.pace));
            break;
        case 'selectPace':
            $("#divParsedSpeedPace").text(getStrFromPaceObj(data.pace));
            $("#divConversion").text("Speed: " + getStrFromSpeedObj(data.speed));
            break;
        }
}

function clearSpeedPaceStrings() {
    $("#divParsedSpeedPace").text("");
    $("#divConversion").text("");
}

function doAttemptParseSpeedPaceStr(iSpeedPaceStr) {
    const [apiName, queryData] = getApiNameAndQueryData(iSpeedPaceStr);
    queryAPINameWithData(apiName, queryData)
        .then((data) => {
            if (data.exitcode === 0) {
                displaySpeedPaceStrings(data.data);
            } else {
                clearSpeedPaceStrings();
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
