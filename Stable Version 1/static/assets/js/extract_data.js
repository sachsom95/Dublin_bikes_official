/**
 * request real time data
 * @param station_number
 */
function updatestation(station_number) {
    $.ajax({
        url: "/realtime",
        type: "get",
        data: {
            "number": station_number
        },
        dataType: "json",
        success: function (result) {
            document.getElementById('bike_available').innerHTML = result['bike_available'];
            document.getElementById("station").innerHTML = result['station'];
            document.getElementById("status").innerHTML = result['status'];
            document.getElementById("stands").innerHTML = result['stands_available'];
            document.getElementById("weather_icon").src = "http://openweathermap.org/img/wn/" + result['icon'] + "@2x.png";
        }
    });
}// updatestation


function getStationId(stationName) {
        var stationId;
        for (var i = 0; i < stations.length; i++) {
            if (stations[i].name === stationName) {
                stationId = stations[i].number;
                return stationId;
            }
        }
        return stationId;
    }


/**
 * calculate the carbon emission
 * @param position1 type:LatLng
 * @param position2 type:LatLng
 */
function carbonDistance(position1, position2) {
    var distance = google.maps.geometry.spherical.computeDistanceBetween(position1, position2);
    return distance;
}


/*
submit button click event
 */
$("#submit_button").click(function () {
    get_data();
    return false;
});

/**
 * get prediction and update charts
 */
function get_data() {

    var start_station;
    var destination_station;
    var day_of_travel;
    var hour_of_travel;
    var minute_of_travel;
    start_station = document.getElementById("start_point_template").value;
    destination_station = document.getElementById("destination_template").value;
    day_of_travel = document.getElementById("date_dropdown").value;
    hour_of_travel = document.getElementById("hour_dropdown").value;
    minute_of_travel = document.getElementById("min_dropdown").value;

    /* dropdowns option content check */
    if (start_station === "") {
        alert("Please choose a start point");
        return false;
    }
    if (destination_station === "") {
        alert("Please choose your destination");
        return false;
    }
    if (day_of_travel === "") {
        alert("Please specify a day");
        return false;
    }
    if (hour_of_travel === "") {
        alert("Please choose specify an hour");
        return false;
    }

    /* loader */
    loader_generate();

    /*
         request for daily prediction data
          */
    $.ajax({
        url: "/pred",
        type: "get",
        data: {
            "start_station": start_station
            , "destination_station": destination_station
            , "day_of_travel": day_of_travel
            , "hour_of_travel": hour_of_travel
        },
        dataType: "text",
        success: function (result) {
            final = JSON.parse(result);

            document.getElementById('predict_bike').innerHTML = final['bike_available'];
            document.getElementById("predict_stands").innerHTML = final['stands_available'];
            document.getElementsByClassName('start_station')[0].innerHTML = start_station;
            document.getElementsByClassName('start_station')[1].innerHTML = start_station;
            document.getElementsByClassName('end_station')[0].innerHTML = destination_station;
            document.getElementsByClassName('end_station')[1].innerHTML = destination_station;
            document.getElementsByClassName('hour_to_travel')[0].innerHTML = hour_of_travel;
            document.getElementsByClassName('hour_to_travel')[1].innerHTML = hour_of_travel;
            document.getElementsByClassName('day_of_travel')[0].innerHTML = day_of_travel;
            document.getElementsByClassName('day_of_travel')[1].innerHTML = day_of_travel;

            /*
             update the line chart - daily
             */
            var $line_child = $("#line_chart canvas");
            var line_canvas_value = $line_child.attr("data-bs-chart");
            var line_convas_data = JSON.parse(line_canvas_value);
            line_convas_data['data']['labels'] = [final['x_axis'][0], final['x_axis'][1], final['x_axis'][2], final['x_axis'][3], final['x_axis'][4], final['x_axis'][5], final['x_axis'][6]];
            line_convas_data['data']['datasets'][0]['data'] = [final['y_axis_bike'][0], final['y_axis_bike'][1], final['y_axis_bike'][2], final['y_axis_bike'][3], final['y_axis_bike'][4], final['y_axis_bike'][5], final['y_axis_bike'][6]];
            $line_child.remove();
            $("#line_chart").append("<canvas></canvas>");

            var $new_line_chart = $("#line_chart canvas");
            $new_line_chart.attr("data-bs-chart", JSON.stringify(line_convas_data));
            var myLineChart = new Chart($new_line_chart[0].getContext("2d"), line_convas_data);

            /*
             update the bar chart - daily
             */
            var $bar_child = $("#bar_chart canvas");
            var bar_canvas_value = $bar_child.attr("data-bs-chart");
            var bar_convas_data = JSON.parse(bar_canvas_value);
            bar_convas_data['data']['labels'] = [final['x_axis'][0], final['x_axis'][1], final['x_axis'][2], final['x_axis'][3], final['x_axis'][4], final['x_axis'][5], final['x_axis'][6]];
            bar_convas_data['data']['datasets'][0]['data'] = [final['y_axis_stands'][0], final['y_axis_stands'][1], final['y_axis_stands'][2], final['y_axis_stands'][3], final['y_axis_stands'][4], final['y_axis_stands'][5], final['y_axis_stands'][6]];
            $bar_child.remove();
            $("#bar_chart").append("<canvas></canvas>");
            var $new_bar_chart = $("#bar_chart canvas");
            $new_bar_chart.attr("data-bs-chart", JSON.stringify(bar_convas_data));
            var myBarChart = new Chart($new_bar_chart[0].getContext("2d"), bar_convas_data);

            /*
            show weather warning info
             */
            var description = final['description'];

            if (description == 1) {
                document.getElementById("weather_warning").innerHTML = "Drizzle is expected today";
            } else if (description == 2) {
                document.getElementById("weather_warning").innerHTML = "Watch out! Rain is expected today!";
            } else if (description == 0) {
                document.getElementById("weather_warning").innerHTML = "Expect a Cloudy day";
            }

        }

    });

    /* hourly data prediction */
    $.ajax({
        url: "/predict_all",
        type: "get",
        data: {
            "start_station": start_station
            , "destination_station": destination_station
            , "day_of_travel": day_of_travel
            , "hour_of_travel": hour_of_travel
        },
        dataType: "text",
        success: function (result) {
            final = JSON.parse(result);

            /*
            update the line chart - hourly
            */
            var $line_child = $("#line_chart1 canvas");
            var line_canvas_value = $line_child.attr("data-bs-chart");
            var line_convas_data = JSON.parse(line_canvas_value);
            line_convas_data['data']['labels'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23];
            line_convas_data['data']['datasets'][0]['data'] = [final['24hour_bikes'][0], final['24hour_bikes'][1], final['24hour_bikes'][2], final['24hour_bikes'][3], final['24hour_bikes'][4], final['24hour_bikes'][5], final['24hour_bikes'][6], final['24hour_bikes'][7], final['24hour_bikes'][8], final['24hour_bikes'][9], final['24hour_bikes'][10], final['24hour_bikes'][11], final['24hour_bikes'][12], final['24hour_bikes'][13], final['24hour_bikes'][14], final['24hour_bikes'][15], final['24hour_bikes'][16], final['24hour_bikes'][17], final['24hour_bikes'][18], final['24hour_bikes'][19], final['24hour_bikes'][20], final['24hour_bikes'][21], final['24hour_bikes'][22], final['24hour_bikes'][23]];
            $line_child.remove();
            $("#line_chart1").append("<canvas></canvas>");
            var $new_line_chart = $("#line_chart1 canvas");
            $new_line_chart.attr("data-bs-chart", JSON.stringify(line_convas_data));
            var myLineChart = new Chart($new_line_chart[0].getContext("2d"), line_convas_data);

            /*
            update the bar chart - hourly
            */
            var $line_child = $("#bar_chart1 canvas");
            var line_canvas_value = $line_child.attr("data-bs-chart");
            var line_convas_data = JSON.parse(line_canvas_value);
            line_convas_data['data']['labels'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23];
            line_convas_data['data']['datasets'][0]['data'] = [final['24hour_stands'][0], final['24hour_stands'][1], final['24hour_stands'][2], final['24hour_stands'][3], final['24hour_stands'][4], final['24hour_stands'][5], final['24hour_stands'][6], final['24hour_stands'][7], final['24hour_stands'][8], final['24hour_stands'][9], final['24hour_stands'][10], final['24hour_stands'][11], final['24hour_stands'][12], final['24hour_stands'][13], final['24hour_stands'][14], final['24hour_stands'][15], final['24hour_stands'][16], final['24hour_stands'][17], final['24hour_stands'][18], final['24hour_stands'][19], final['24hour_stands'][20], final['24hour_stands'][21], final['24hour_stands'][22], final['24hour_stands'][23]];
            $line_child.remove();
            $("#bar_chart1").append("<canvas></canvas>");
            var $new_line_chart = $("#bar_chart1 canvas");
            $new_line_chart.attr("data-bs-chart", JSON.stringify(line_convas_data));
            var myLineChart = new Chart($new_line_chart[0].getContext("2d"), line_convas_data);
        }
    });

    setTimeout(function () {
        $(".chart_container").css('display', 'block')
    }, 3000);

    /*resume last direction Icon */
    var directionObject = JSON.parse(localStorage.getItem("last_direction"));
    if(directionObject != null){
    var lastStartName = directionObject.start;
    var lastEndName = directionObject.end;
    var lastStartId = getStationId(lastStartName);
    var lastEndId = getStationId(lastEndName);
    resumeIcon(lastStartId);
    resumeIcon(lastEndId);
    }

    /* find two new number and set Icon*/
    var startMarkerId = getStationId(start_station);
    var endMarkerId = getStationId(destination_station);

    var startMarker = findTargetMarker(startMarkerId);
    var endMarker = findTargetMarker(endMarkerId);
    startMarker.marker.setIcon("http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png");
    endMarker.marker.setIcon("http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png");

    /*
    save the direction that the user set last time
     */
    var last_direction = {start: start_station, end: destination_station};
    localStorage.setItem("last_direction", JSON.stringify(last_direction));

    /* distance and carbon emission data computation */
    var startMarkerPostion = new google.maps.LatLng({
        lat: startMarker.marker.getPosition().lat(),
        lng: startMarker.marker.getPosition().lng()
    });
    var endMarkerPosition = new google.maps.LatLng({
        lat: endMarker.marker.getPosition().lat(),
        lng: endMarker.marker.getPosition().lng()
    });
    var carbonCalDistance = carbonDistance(startMarkerPostion, endMarkerPosition);
    $("#distance").html("Expected Travel Distance: " + carbonCalDistance.toFixed(2) + " m");
    var carbon = carbonCalDistance / 1000 * 118;
    $("#carbon").html("You have prevented " + carbon.toFixed(2) + "g CO2 going to the atmosphere for this journey");

} // get_data()

/* generate loaders */
function loader_generate() {
    var template = "<div class=\"lds-spinner\"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div> "
    document.getElementById("predict_stands").innerHTML = template;
    document.getElementById("predict_bike").innerHTML = template;
}
