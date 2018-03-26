// Set up the input and button for picking the time
$('#timeInput').timepicker();
$('#timeButton').on('click', function (){
    $('#timeInput').timepicker('setTime', new Date());
});

// Marker for the map
var marker;

// Create the map
function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 11.7,
          center: {lat: 37.7749, lng: -122.4194}
    });
    var geocoder = new google.maps.Geocoder();
    // Place a marker at the address in the input
    document.getElementById('submit').addEventListener('click', function() {
          geocodeAddress(geocoder, map);
    });
}

//Get the location of the address the user gave
function geocodeAddress(geocoder, resultsMap) {
    var address = document.getElementById('address').value;
    geocoder.geocode({'address': address}, function(results, status) {
        if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            if(marker != null){
                // Only allow one marker at a time
                marker.setMap(null);
            }
            marker = new google.maps.Marker({
              map: resultsMap,
              position: results[0].geometry.location
            });
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

// Once choices made, and user submits, send the data
function submit() {

    if(marker == null){
        alert("Error: No location chosen");
        return;
    }
    // Give latitudes and longitudes of marker
    var lat = marker.getPosition().lat();
    var lng = marker.getPosition().lng();

    // Get time given in input
    var time = $('#timeInput').val();
    if(time == "") {
        alert("Error: No time chosen");
        return;
    }

    // Find the result and print the information to the page accordingly
    $.ajax({url: "interactive_data", data: {lat: lat, lng: lng, time: time}, success: function(result) {
        if(result == "") {
            $('#header_result').text("No results found");
            $('#body_result').text("No results have been found for this area and time combination. Try another!");
        } else if(result == "MEDIC") {
            $('#header_result').text("Medic");
            $('#body_result').text("The most likely dispatch given your location and time inputs would be a medical " +
                                    "unit. This means someone on the scene was injured in some way and requires " +
                                    "medical assistance. This is one of the most common forms of dispatch. " +
                                    "If you want to see another result, just pick a new location and/or time, " +
                                    " then click submit again!");
        } else if(result == "ENGINE"){
            $('#header_result').text("Engine");
            $('#body_result').text("The most likely dispatch given your location and time inputs would be a engine " +
                                    "unit. This means that a fire most likely occurred, and a fire engine is " +
                                    "required to come put it out. There are a variety of fire engines that could " +
                                    "be dispatched, but nonetheless this is the most common form of dispatch. " +
                                    "If you want to see another result, just pick a new location and/or time, " +
                                    "then click submit again!");
        } else if(result == "CHIEF"){
            $('#header_result').text("Chief");
            $('#body_result').text("The most likely dispatch given your location and time inputs would a chief. " +
                                    "This means that the chief of police is coming out to the scene as part of " +
                                    "the dispatch. This could occur due to a crime or other matter with which the " +
                                    "police cannot handle only on their own. " +
                                    "If you want to see another result, just pick a new location and/or time, " +
                                    "then click submit again!");
        } else if(result == "PRIVATE"){
            $('#header_result').text("Private");
            $('#body_result').text("The most likely dispatch given your location and time inputs would be a private " +
                                    "unit. This could occur for a variety of reasons, including at request of the " +
                                    "caller. A private unit means they are coming from a private, not city or state " +
                                    "unit. " +
                                    "If you want to see another result, just pick a new location and/or time, " +
                                    "then click submit again!");
        } else if(result == "RESCUE SQUAD"){
            $('#header_result').text("Rescue Squad");
            $('#body_result').text("The most likely dispatch given your location and time inputs would be a rescue " +
                                    "squad. This would come along with a fire engine and be a group of firefighters " +
                                    "who are meant to rescue anyone stuck in a fire or other event. " +
                                    "If you want to see another result, just pick a new location and/or time, " +
                                    "then click submit again!");
        } else if(result == "TRUCK"){
            $('#header_result').text("Truck");
            $('#body_result').text("The most likely dispatch given your location and time inputs would be a truck. " +
                                    "This could mean a variety of trucks, and will have the truck that is most " +
                                    "needed for the dispatch to be sent out. " +
                                    "If you want to see another result, just pick a new location and/or time, " +
                                    "then click submit again!");
        } else if(result == "SUPPORT"){
            $('#header_result').text("Support");
            $('#body_result').text("The most likely dispatch given your location and time inputs would be a support " +
                                    "unit. This means a group of people meant to support the dispatch will go to " +
                                    "the scene. " +
                                    "If you want to see another result, just pick a new location and/or time, " +
                                    "then click submit again!");
        } else if(result == "RESCUE CAPTAIN"){
            $('#header_result').text("Rescue Captain");
            $('#body_result').text("The most likely dispatch given your location and time inputs would be a rescue " +
                                    "captain. This means that the specific captain of a rescue squad is going to " +
                                    "the scene. This could occur if a specific skill the captain has is needed " +
                                    "If you want to see another result, just pick a new location and/or time, " +
                                    "then click submit again!");
        } else if(result == "INVESTIGATION"){
            $('#header_result').text("Investigation");
            $('#body_result').text("The most likely dispatch given your location and time inputs would be an " +
                                    "investigation unit. This occurs if there is a crime that will need an " +
                                    "investigation to occur to find the culprit or just gather evidence.  " +
                                    "If you want to see another result, just pick a new location and/or time, " +
                                    "then click submit again!");
        }
    }});
}