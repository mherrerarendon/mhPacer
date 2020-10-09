async function queryAPINameWithData(apiName, data) {
    hostName = "http://127.0.0.1:5000/api/";
    apiVersion = "v1.0/";
    const url = hostName + apiVersion + apiName;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}