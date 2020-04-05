//Author : Sachin April 5 last update

//function gets all values after submit button pressed
//important ids for reference
//start destination- "start_point_template"
//destination_station - id = "destination_template"
//day_of_travel - id="date_dropdown" 
//hour_of_travel -id="hour_dropdown"
//minuite_of_travel - id="min_dropdown"


var start_station;
var destination_station;
var day_of_travel;
var hour_of_travel;
var minuite_of_travel;

function get_data()
{
    console.log("Submit button pressed");
    start_station = document.getElementById("start_point_template").value;
    console.log("Start station:",start_station);
    
    destination_station =
    document.getElementById("destination_template").value;
    console.log("End station:",destination_station);
    
    day_of_travel =
        document.getElementById("date_dropdown").value;
    console.log("Day of travel",day_of_travel);
    
    hour_of_travel =
        document.getElementById("hour_dropdown").value;
    console.log("Hour of travel:",hour_of_travel);
    
    minuite_of_travel = 
        document.getElementById("min_dropdown").value;
    console.log("Minuite of travel",minuite_of_travel)
    
}