window.onload = function () {

    var startPos;
    var geoOptions = {
        timeout: 10 * 3000
    };

    var geoSuccess = function (position) {
        console.log("enter geoSuccess");
        startPos = position;
        document.getElementById('currentLat').innerHTML = startPos.coords.latitude;
        document.getElementById('currentLon').innerHTML = startPos.coords.longitude;
        var myPosition = {lat: startPos.coords.latitude, lng: startPos.coords.longitude};

        // sessionStorage.setItem("myPosition",JSON.stringify(google.maps.LatLng(myPosition)));
        // var initialDistance = getDistance(stations);
        // alert(initialDistance);
        /*
        myPosition marker setting
         */
        var iconBase = "http://maps.google.com/mapfiles/kml/shapes/cycling.png"; // marker icon url

        myPositionMarker = new google.maps.Marker({
            position: myPosition,
            map: map,
            // for more icons: https://developers.google.com/maps/documentation/javascript/custom-markers
            icon: {url: iconBase, scaledSize: new google.maps.Size(40, 40)}
        });
        myPositionMarker.setTitle("My Position");
        myPositionMarker.setDraggable(true);

        /*
         get new marker coordinate after being dragged
         */
        myPositionMarker.addListener("dragend", function () {
            var new_position = myPositionMarker.getPosition();
            myPosition = new_position;
            myPosition = new_position;
            // alert(myPosition instanceof google.maps.LatLng);
            sessionStorage.clear();
            // sessionStorage key and value must be string type
            sessionStorage.setItem("myPosition",JSON.stringify(myPosition));
            console.log("set here, after move" + myPosition.lat() + " " + myPosition.lng());

            document.getElementById('currentLat').innerHTML = myPosition.lat();
            document.getElementById('currentLon').innerHTML = myPosition.lng();

            // renew new position and calculated distances
            var renewDistance = getDistance(stations);

            console.log("renewDistance===" + renewDistance);
            console.log("name====" + renewDistance[0].name + "Distance===" + renewDistance[0].distance);
        });
        console.log("get icon");

    };
    var geoError = function (error) {
        console.log('Error occurred. Error code: ' + error.code);
        // error.code can be:
        //   0: unknown error
        //   1: permission denied
        //   2: position unavailable (error response from location provider)
        //   3: timed out
    };

    var watch = function (position) {
        console.log(position.coords.latitude + " " + position.coords.longitude);
        document.getElementById('currentLat').innerHTML = position.coords.latitude;
        document.getElementById('currentLon').innerHTML = position.coords.longitude;
    };
    setInterval(function () {
        navigator.geolocation.watchPosition(watch);
    }, 3000);
    console.log("123123" + navigator.geolocation);


    navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);



};
