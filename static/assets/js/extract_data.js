//Author : Sachin April 5 last update

//function gets all values after submit button pressed
//important ids for reference
//start destination- "start_point_template"
//destination_station - id = "destination_template"
//day_of_travel - id="date_dropdown" 
//hour_of_travel -id="hour_dropdown"
//minute_of_travel - id="min_dropdown"

    /*
    submit button click event
     */
    $("#submit_button").click(function () {
        var distanceInfo = get_data();
        console.log("distanceInfo=====" + distanceInfo);
        return false;
    });


    var start_station;
    var destination_station;
    var day_of_travel;
    var hour_of_travel;
    var minute_of_travel;

    function get_data() {
        console.log("Submit button pressed");
        start_station = document.getElementById("start_point_template").value;

        destination_station =
            document.getElementById("destination_template").value;

        day_of_travel =
            document.getElementById("date_dropdown").value;

        hour_of_travel =
            document.getElementById("hour_dropdown").value;

        minute_of_travel =
            document.getElementById("min_dropdown").value;

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
                document.getElementById('start_station').innerHTML = start_station;
                document.getElementById('end_station').innerHTML = destination_station;

                /*
                 update the line chart
                 */
                var $line_child = $("#line_chart canvas");
                var line_canvas_value = $line_child.attr("data-bs-chart");
                var line_convas_data = JSON.parse(line_canvas_value);
                line_convas_data['data']['labels'] = [final['x_axis'][0], final['x_axis'][1], final['x_axis'][2], final['x_axis'][3], final['x_axis'][4], final['x_axis'][5], final['x_axis'][6]];
                // console.log(convas_data['data']['datasets'][0]['data']);
                line_convas_data['data']['datasets'][0]['data'] = [final['y_axis_bike'][0], final['y_axis_bike'][1], final['y_axis_bike'][2], final['y_axis_bike'][3], final['y_axis_bike'][4], final['y_axis_bike'][5], final['y_axis_bike'][6]];
                // console.log(JSON.stringify(line_convas_data));
                $line_child.remove();
                $("#line_chart").append("<canvas></canvas>");
                // return false;
                var $new_line_chart = $("#line_chart canvas");
                $new_line_chart.attr("data-bs-chart", JSON.stringify(line_convas_data));
                var myLineChart = new Chart($new_line_chart[0].getContext("2d"), line_convas_data);


                /*
                 update the bar chart
                 */
                var $bar_child = $("#bar_chart canvas");
                var bar_canvas_value = $bar_child.attr("data-bs-chart");
                var bar_convas_data = JSON.parse(bar_canvas_value);
                bar_convas_data['data']['labels'] = [final['x_axis'][0], final['x_axis'][1], final['x_axis'][2], final['x_axis'][3], final['x_axis'][4], final['x_axis'][5], final['x_axis'][6]];
                // console.log(convas_data['data']['datasets'][0]['data']);
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
                console.log("weather description===" +description);

                if(description == 1){
                    document.getElementById("weather_warning").innerHTML = "Drizzle is expected today";
                }else if(description == 2){
                    document.getElementById("weather_warning").innerHTML = "Watch out! Rain is expected today!";
                }else if(description == 0){
                    document.getElementById("weather_warning").innerHTML = "Expect a Cloudy day";
                }

            }

        });
        return getDistance(stations);
    } // get_data()


function getDistance(stations = stations){
        // alert("getDistance!");
                /*
                //calculate distance between myPosition LatLng and destination LatLng
                 */

                var stationAndDistance = [];

                 // the argument is the user's coordinate in get_user_location.js/geoSuccess callback function
                var positionAfterMove = JSON.parse(sessionStorage.getItem("myPosition"));
                console.log("1====" + positionAfterMove.lat);
                console.log("2====" + positionAfterMove.lng);

                var distanceCalculateStart = new google.maps.LatLng({lat: positionAfterMove.lat,lng: positionAfterMove.lng});

                for(var i=0; i<stations.length; i++){
                    var lat = stations[i]["latitude"];
                    var lng = stations[i]["longitude"];
                    var name = stations[i]["name"];
                    var distanceCalculateStartDest = new google.maps.LatLng({lat:lat,lng:lng});
                    var distance = google.maps.geometry.spherical.computeDistanceBetween(distanceCalculateStart, distanceCalculateStartDest);

                     stationAndDistance[i] = {name:name.toString(), distance:distance.toString()};

                }
                return stationAndDistance;



}

