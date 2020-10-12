$( document ).ready(function() {
    $("#speedPaceInput").on("keydown", function(event) {
        startSpeedPaceInputKeyDownTimer();
    });

    $("#targetEventInput").on("keydown", function(event) {
        startTargetEventInputKeyDownTimer();
    });

    $('#selectSpeedPace').change(function () {
        switchBetweenPaceAndSpeed();
    })
});

function getCurrentSpeedStr() {
    var speedStr = null;
    switch($("#selectSpeedPace").val()) {
        case 'selectSpeed':
            speedStr = $("#speedPaceInput").val();
            break;
        case 'selectPace':
            speedStr = $("#divConversion").text();
            break;
        }
    return speedStr;
}

function displayResultIfNeeded() {
    const enable = ($("#divParsedSpeedPace").text() !== "" && $("#divParsedTargetEvent").text() !== "");
    if (enable) {
        speedStr = getCurrentSpeedStr();
        getEventTimeWithSpeed(speedStr, $("#targetEventInput").val());
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
    queryAPINameWithData("speedmath/getEventTimeWithSpeed", queryData)
        .then((responseBody) => {
            if (responseBody.time) {
                $("#divResult").text("Event time: " + getStrFromTimeObj(responseBody.time));
            } else {
                $("#divResult").text("");
            }
        });
}

function getApiNameAndQueryDataForSpeedPace(iSpeedPaceStr) {
    var apiName = null;
    var queryData = null;
    switch($("#selectSpeedPace").val()) {
        case 'selectSpeed':
            apiName = "parser/parseSpeedStr";
            queryData = {speedStr: iSpeedPaceStr};
            break;
        case 'selectPace':
            apiName = "parser/parsePaceStr";
            queryData = {paceStr: iSpeedPaceStr};
            break;
        }
    return [apiName, queryData];
}

function updateSpeedPaceStringsWithData(data) {
    var parsedSpeedPace = null;
    var conversionLabel = null;
    var conversion = null;
    switch($("#selectSpeedPace").val()) {
        case 'selectSpeed':
            parsedSpeedPace = getStrFromSpeedObj(data.speed)
            conversionLabel = "Pace: ";
            conversion = getStrFromPaceObj(data.pace);
            break;
        case 'selectPace':
            parsedSpeedPace = getStrFromPaceObj(data.pace);
            conversionLabel = "Speed: ";
            conversion = getStrFromSpeedObj(data.speed);
            break;
        }

    $("#divParsedSpeedPace").text(parsedSpeedPace);
    $("#divConversion").text(conversionLabel);
    $("<span>")
        .text(conversion)
        .attr("id", "spanConversion")
        .appendTo("#divConversion");
}

function switchBetweenPaceAndSpeed() {
    const newSpeedPaceStr = $("#spanConversion").text();
    $("#speedPaceInput").val(newSpeedPaceStr);
    doAttemptParseSpeedPaceStr(newSpeedPaceStr);
}

function clearSpeedPaceStrings() {
    $("#divParsedSpeedPace").text("");
    $("#divConversion").text("");
}

function doAttemptParseSpeedPaceStr(iSpeedPaceStr) {
    const [apiName, queryData] = getApiNameAndQueryDataForSpeedPace(iSpeedPaceStr);
    queryAPINameWithData(apiName, queryData)
        .then((responseBody) => {
            if (responseBody.completeRequest) {
                updateSpeedPaceStringsWithData(responseBody);
            } else {
                clearSpeedPaceStrings();
            }

            displayResultIfNeeded();
        });
};


function doAttemptParseTargetEventStr(targetEventStr) {
    const queryData = {eventStr: targetEventStr};
    queryAPINameWithData("parser/parseEventStr", queryData)
        .then((responseBody) => {
            if (responseBody.completeRequest) {
                $("#divParsedTargetEvent").text(getStrFromEventObj(responseBody.event));
            } else {
                $("#divParsedTargetEvent").text("");
            }

            displayResultIfNeeded();
        });
}
