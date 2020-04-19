//this js is used to generate templates for website mainly the contents of dropdowns

//Using xmlHttp Request API to read json
var httpobj = new XMLHttpRequest();

var url = "static/assets/json/dublin.json";

httpobj.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var parsedObj = JSON.parse(httpobj.responseText);

        generate_stations(parsedObj);
        generate_time();
    }
};

httpobj.open("GET", url, true);
httpobj.send();

/**
 * station dropdowns
 * @param data
 */
function generate_stations(data) {

    var template_start = "<option value=\"\" selected=\"\" hidden>Starting Point</option>";
    var template_end = "<option value=\"\" selected=\"\" hidden>Destination</option>";

    var names = [];
    for (var i = 0; i < data.length; i++) {
        names[i] = data[i].name;
    }
    names.sort();

    //template
    //"<option value=\""+data[1]["name"]+"\" selected=\"" +data[1]["name"]+"\"</option>"

    //for loop that makes the template
    for (var i = 0; i < names.length; i++) {
        var info = names[i];

        var temp = "<option value=\"" + info + "\">" + info + "</option>";

        template_start = template_start.concat(temp);
        template_end = template_end.concat(temp);
    }

    document.getElementById("start_point_template").innerHTML = template_start;
    document.getElementById("destination_template").innerHTML = template_end;
}

/**
 * generate hour dropdown
 */
function generate_time() {
    var template = "<option value=\"\" selected=\"\" hidden>Hour of travel </option>";

    for (var i = 0; i <= 23; i++) {
        var temp = "<option value=\"" + i + "\">" + i + "</option>";
        template = template.concat(temp);
    }
    document.getElementById("hour_dropdown").innerHTML = template;
}


