
function updatestation(station_number) {
            $.ajax({
                url: "/ajax",
                type: "get",
                data: {
                    "number": station_number
                },
                dataType: "json",
                success: function (result) {
                    console.log("return!!!" + result);
                    // result = JSON.parse(result);
                    document.getElementById('bike_available').innerHTML = result['bike_available'];
                    document.getElementById("station").innerHTML = result['station'];
                    document.getElementById("status").innerHTML = result['status'];
                    document.getElementById("stands").innerHTML = result['stands_available'];
                }
            });
        }

/*
     Initialize and add the map
     */
    markers = [];
    console.log(typeof(realtime_data));
    console.log(realtime_data);

    function initMap() {
        alert("called map");
        // The location of Uluru
        var uluru = {lat: 53.3488, lng: -6.281637};

        // The map, centered at Uluru
        map = new google.maps.Map(
            document.getElementById('MAP_DIV'), {zoom: 13, center: uluru});
        // The marker, positioned at Uluru
        var marker_center = new google.maps.Marker({position: uluru, map: map});

        /*
        different marker colors    red: <= 30%; yellow: 30% to 60%; green: >=60%
         */
        var greenUrl = "http://maps.google.com/mapfiles/kml/paddle/grn-diamond.png";
        var redUrl = "http://maps.google.com/mapfiles/kml/paddle/red-diamond.png";
        var yellowUrl = "http://maps.google.com/mapfiles/kml/paddle/orange-diamond.png";

        for (var i = 0; i < realtime_data.length; i++) {
            var time = realtime_data[i][0];
            var markerId = realtime_data[i][1];
            var name = realtime_data[i][2];
            console.log("namess " + name);
            var address = realtime_data[i][3];
            var lat = parseFloat(realtime_data[i][4]);
            var lng = parseFloat(realtime_data[i][5]);
            var bikeStandNum = realtime_data[i][8];
            var standsNum = realtime_data[i][9];
            var bikesNum = realtime_data[i][10];
            var status = realtime_data[i][11];
            var iconType = "";
            console.log("lat == " + realtime_data[i][4] + "type == " + typeof(realtime_data[i][4]));
            console.log("lng == " + realtime_data[i][5]);
            var near1 = {lat: lat, lng: lng};
            var marker = new google.maps.Marker({position: near1, map: map});

            var infowindow = new google.maps.InfoWindow();

            if (bikesNum <= bikeStandNum * 0.3) {
                marker.setIcon({url: redUrl, size: new google.maps.Size(50, 60)});
                iconType = "red";
            } else if (bikesNum < bikeStandNum * 0.6) {
                marker.setIcon({url: yellowUrl, size: new google.maps.Size(50, 60)});
                iconType = "yellow";
            } else {
                marker.setIcon({url: greenUrl, size: new google.maps.Size(50, 60)});
                iconType = "green";
            }

            marker.setMap(map);
            markers.push({
                id: markerId, marker: marker,
                bikesNum: bikesNum,
                standsNum: standsNum,
                iconType: iconType
            });

            marker.addListener('click', function () {
                // infowindow.setContent('Time :' + time + ' , Number :' + markerId + ' , Name :' + name +
                //     ', Address :' + address + ', bike_stands :' +
                //     bikeStandNum + ',  available_bike_stands :' + standsNum
                //     + ', Available_bikes :' + bikesNum + 'Station_status :' + status);
                alert(name);
                infowindow.setContent("<div><ul><li>Time :" + time + "</li>" +
                    "<li>Number :" +  markerId + "</li>" +
                    "<li>Name :" +  name + "</li>" +
                    "<li>Address :" +  address + "</li>" +
                    "<li>bike_stands :" +  bikeStandNum + "</li>" +
                    "<li>available_bike_stands :" + standsNum + "</li>" +
                    "<li>Available_bikes :" + bikesNum + "</li>" +
                    "<li>Station_status :" + status + "</li>" +
                    "<ul>" +
                    "</div>");
                // infowindow.setPosition(new google.maps.LatLng(realtime_data[i][1][4], realtime_data[i][1][5]));
                infowindow.setPosition(near1);
                infowindow.open(map);
                updatestation(markerId);
                document.getElementById("realtime_info").style.visibility = "visible";
            });
            // var markerId = {{ i[1] }};//number
            // var bikesNum = {{ i[10] }};//availble bikes
            // var standsNum = {{ i[9] }}; // available number
            //  var bikeStandNum = {{ i[8] }}; //total stands number
            // var iconType = "";
            // var near1 = {lat: {{ i[4] }}, lng: {{ i[5] }} };
            // var marker = new google.maps.Marker({position:near1,map: map});
            // var infowindow = new google.maps.InfoWindow();

        }
          marker_center.setMap(map);
    }