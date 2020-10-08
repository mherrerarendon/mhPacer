function toQueryStr(object) {
    var esc = encodeURIComponent;
    var query = Object.keys(object)
        .map(k => esc(k) + '=' + esc(object[k]))
        .join('&');
    return query;
}

async function queryAPINameWithData(apiName, data) {
    hostName = "http://127.0.0.1:5000/api/";
    apiVersion = "v1.0/";
    const url = hostName + apiVersion + apiName + "?" + toQueryStr(data);
    const response = await fetch(url, {
        method: "GET"
    });
    return response.json();
}