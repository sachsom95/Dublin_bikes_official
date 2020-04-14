window.onload = function () {
    sessionStorage.clear();
    /*
    get the direction that the user set last time
     */
    var last_direction = localStorage.getItem("last_direction");
    if (last_direction != null) {
        var start = JSON.parse(last_direction).start;
        var end = JSON.parse(last_direction).end;
        document.getElementById("start_point_template").value = start;
        document.getElementById("destination_template").value = end;
    }

     /*
    All distances and static info stored in an Array
     */
    distances = getDistance(stations);
    for(var i=0;i<distances.length;i++){
        console.log(distances[i].name + " " + distances[i].distance);
    }
    /*

    myPosition marker setting
    hard-coded initial position: {lat: 53.34279722411591, lng = -6.267303794653323}
    mimic user position at Dublin Catsle
     */
    var myPosition = {lat: 53.34279722411591, lng: -6.267303794653323};
    var iconBase = "http://maps.google.com/mapfiles/kml/shapes/man.png"; // marker icon url

    myPositionMarker = new google.maps.Marker({
        position: myPosition,
        // for more icons: https://developers.google.com/maps/documentation/javascript/custom-markers
        icon: {url: iconBase, scaledSize: new google.maps.Size(40, 40)}
    });
    myPositionMarker.setMap(map);
    myPositionMarker.setTitle("My Position");
    myPositionMarker.setDraggable(true);

    /*
     get new marker coordinate and update distances after being dragged
     */
    myPositionMarker.addListener("dragend", function () {

        var new_position = myPositionMarker.getPosition();
        myPosition = new_position;
        myPosition = new_position;

        var new_lat = myPosition.lat();
        var new_lng = myPosition.lng();
        distances = getDistance(stations, new_lat, new_lng);
    });



    /*
    onclick buttons: I want to use a bike/ I want to return a bike
     */
    $(".col-md-12").click(function(){
        /*
        get previous marker Id and turn it back
         */
        var id = parseInt(sessionStorage.getItem("id"));
        console.log("id=== " + typeof(id));
        console.log("id====" + id);
        if(! isNaN(id)){
            var previousMarker = findTargetMarker(id);
            var icon = previousMarker.iconType;
            // var bikes =
            console.log("Type==== " + icon);
            if(icon === "red"){
                previousMarker.marker.setIcon("http://maps.google.com/mapfiles/kml/paddle/red-diamond.png");
            }else if(icon === "yellow"){
                previousMarker.marker.setIcon("http://maps.google.com/mapfiles/kml/paddle/orange-diamond.png");
            }else{
                previousMarker.marker.setIcon("http://maps.google.com/mapfiles/kml/paddle/grn-diamond.png");
            }
        }

        /*
        handle two options
         */
        var text = $(this).text(); // use or return
        var index = 0;
        while(index < distances.length){
            var nearestStation = distances[index++];
            var nearestStationNumber = nearestStation.number;
            if(text.includes("use")) {
                //take a bike / bike number
                //alert("use bike");
                //get dynamic info by stationNumber
                var targetUseMarkerObj = findTargetMarker(nearestStationNumber);
                console.log(typeof(targetUseMarkerObj.bikesNum) + " &&& "+ targetUseMarkerObj.bikesNum);
                if(targetUseMarkerObj.bikesNum !== 0){
                    var targetUseMarker = targetUseMarkerObj.marker;
                    //get coordinates of the targetMarker
                    var nearestStationUseCoor = {lat: targetUseMarker.position.lat(), lng: targetUseMarker.position.lng()};
                    map.setCenter(nearestStationUseCoor);
                    map.setZoom(16);
                    targetUseMarker.setIcon("http://maps.google.com/mapfiles/kml/shapes/cycling.png");

                    var useInfo = "Nearest Station: " + nearestStation.name
                        + "\nDistance: " + nearestStation.distance.toFixed(2) + " meters"
                        + "\nBikes Available: " + targetUseMarkerObj.bikesNum;
                    $("#station_info_body").html(useInfo);

                    /*
                    store the previous marker
                    */
                    sessionStorage.clear();
                    sessionStorage.setItem("id", nearestStationNumber.toString());
                    return;
                }
            }

            //return a bike/ bike stands
            if (text.includes("return")) {
                //alert("return bike");
                var targetReturnMarkerObj = findTargetMarker(nearestStationNumber);
                if (targetReturnMarkerObj.standsNum !== 0) {
                    var targetReturnMarker = targetReturnMarkerObj.marker;
                    //get coordinates of the targetMarker
                    var nearestStationReturnCoor = {lat: targetReturnMarker.position.lat(), lng: targetReturnMarker.position.lng()};
                    map.setCenter(nearestStationReturnCoor);
                    map.setZoom(16);
                    targetReturnMarker.setIcon("http://maps.google.com/mapfiles/kml/shapes/parking_lot.png");
                    var returnInfo = "Nearest Station: " + nearestStation.name
                        + "\nDistance: " + nearestStation.distance.toFixed(2) + "meters"
                        + "\nStands Available: " + targetReturnMarkerObj.standsNum;
                    $("#station_info_body").html(returnInfo);

                    /*
                    store the previous marker
                    */
                    sessionStorage.clear();
                    sessionStorage.setItem("id", nearestStationNumber.toString());
                    return;
                }
            }

        }// while

    });// two Buttons click

};//window.onload

        /*
        function to get target marker to resume the icon
         */
        function findTargetMarker(markerId){
            var target;
            for(var i=0; i<markers.length;i++){
                if(markers[i].id === markerId){
                    target = markers[i];
                    break;
                }
            }
            return target;
        }

    // /*
    //  get the nearestStation via comparing distances
    //  */
    // function getNearestStation(distancesArray) {
    //     var nearest = distancesArray[0];
    //     for (var i = 1; i < distancesArray.length; i++) {
    //         nearest = (distancesArray[i].distance - nearest.distance < 0) ? distancesArray[i] : nearest;
    //     }
    //     console.log("In Function, nearest station ==== " + nearest.name + "& distance=== " + nearest.distance);
    //     return nearest;
    // }

    /*
    //calculate distance between myPosition LatLng and destination LatLng
    with static stations info
    */
function getDistance(stations = stations, lat = 53.34279722411591, lng = -6.267303794653323) {

    var stationAndDistance = [];

    var distanceCalculateStart = new google.maps.LatLng({lat: lat, lng: lng});

    for (var i = 0; i < stations.length; i++) {
        var number = stations[i]["number"];
        var lat = stations[i]["latitude"];
        var lng = stations[i]["longitude"];
        var name = stations[i]["name"];
        var distanceCalculateStartDest = new google.maps.LatLng({lat: lat, lng: lng});
        var distance = google.maps.geometry.spherical.computeDistanceBetween(distanceCalculateStart, distanceCalculateStartDest);

        //create object
        stationAndDistance[i] = {
            number:number,
            distance: distance,
            name: name.toString(),
            lat:lat,
            lng:lng
        };

    }

    //sort by distances
    stationAndDistance.sort((marker1,marker2)=>(marker1.distance - marker2.distance));

    return stationAndDistance;



} // getDistance()
