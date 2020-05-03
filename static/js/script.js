$( document ).ready(function() {
    $("#speedPaceInput").on("keydown", function(event) {
        startSpeedPaceInputKeyDownTimer();
    });

    $("#targetEventInput").on("keydown", function(event) {
        startTargetEventInputKeyDownTimer();
    });

    $('#selectSpeedPace').change(function () {
        switchBetweenPaceAndSpeedIfNeeded();
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
                $("#divResult").text("");
            }
        });
}

function getApiNameAndQueryDataForSpeedPace(iSpeedPaceStr) {
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

function switchBetweenPaceAndSpeedIfNeeded() {
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
    console.log(apiName);
    console.log(queryData);
    queryAPINameWithData(apiName, queryData)
        .then((data) => {
            if (data.exitcode === 0) {
                updateSpeedPaceStringsWithData(data.data);
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
