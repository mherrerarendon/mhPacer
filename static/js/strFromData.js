function getStrForUnitAmount(amount, unitStr) {
    str = "";
    if (amount > 0) {
        str = amount.toString() + " " + unitStr;
    }

    if (amount > 1) {
        str += "s";
    }

    return str;
}

function getHourMinSecValues(totalSeconds) {
	var secondsRemaining = totalSeconds;
	const hours = Math.floor(secondsRemaining / 3600);
    secondsRemaining = secondsRemaining % 3600;
    const minutes = Math.floor(secondsRemaining / 60);
    secondsRemaining = secondsRemaining % 60;
    return [hours, minutes, secondsRemaining];
}

function getStrFromTimeObj(timeObj) {
    // Assume timeObj.time is in minutes for now
    const totalSeconds = Math.round(timeObj.time * 60);
    const [hours, minutes, seconds] = getHourMinSecValues(totalSeconds);
    var timeStr = "";
    timeStr += getStrForUnitAmount(hours, "hour") + " ";
    timeStr += getStrForUnitAmount(minutes, "minute") + " ";
    timeStr += getStrForUnitAmount(seconds, "second");
    return timeStr;
}

function getStrFromSpeedObj(speedObj) {
    var speedStr = "";
    distance = round2Decimals(speedObj.event.distance);
    speedStr += getStrForUnitAmount(distance, speedObj.event.unit) + " ";
    speedStr += "per ";

    // Assume 1 time unit for now
    speedStr += speedObj.time.unit; 
    return speedStr;
}

function round2Decimals(myFloat) {
    return Math.round(myFloat * 100) / 100  // result .12
}

function getStrFromPaceObj(paceObj) {
    var paceStr = "";
    time = round2Decimals(paceObj.time.time);
    paceStr += getStrForUnitAmount(time, paceObj.time.unit) + " ";
    paceStr += "per ";

    // Assume 1 time unit for now
    paceStr += paceObj.event.unit; 
    return paceStr;
}

function getStrFromEventObj(eventObj) {
    return getStrForUnitAmount(eventObj.distance, eventObj.unit)
}