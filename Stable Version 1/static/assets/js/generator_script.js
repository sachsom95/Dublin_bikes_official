//this js is used to generate templates for website mainly the contents of dropdowns

//Author : sachin soman

//Using xmlHttp Request API to read json
var httpobj = new XMLHttpRequest();

var url ="static/assets/json/dublin.json"

httpobj.onreadystatechange = function()
{
    if(this.readyState == 4 && this.status == 200){
         var parsedObj = JSON.parse(httpobj.responseText);    

        generate_stations(parsedObj)
        generate_time()
    }
}

httpobj.open("GET",url,true)
httpobj.send();


//<option value="13">This is item 2</option>
//<option value="" selected="" hidden>Starting Point</option>


function generate_stations(data)
{   
    
    var template_start ="<option value=\"\" selected=\"\" hidden>Starting Point</option>"
    var template_end ="<option value=\"\" selected=\"\" hidden>Destination</option>"

    var length = data.length
    console.log( length)
    
    //template
    //"<option value=\""+data[1]["name"]+"\" selected=\"" +data[1]["name"]+"\"</option>"

    //for loop that makes the template
    for (var i = 0 ; i < length; i++) {
            var info = data[i]["name"];
            
            var temp = 
            
            "<option value=\""+info+"\">"+info+"</option>"
            

            template_start = template_start.concat(temp)
            template_end = template_end.concat(temp)
        }
    
   document.getElementById("start_point_template").innerHTML= template_start;
    
    document.getElementById("destination_template").innerHTML = template_end;
    
    
}



function generate_time() {
    var template = "<option value=\"\" selected=\"\" hidden>Hour of travel </option>";
    
    for (var i = 0 ; i <= 23 ; i++) {
            var temp = "<option value=\""+i+"\">"+i+"</option>";
            template = template.concat(temp)
        }

    document.getElementById("hour_dropdown").innerHTML=template;
    
    
    
}







