function initMap() {
    var sanfran = {lat: 37.7749, lng: -122.4194};

    // Set up map for Dispatch Times tab
    // Initialize the map location and zoom
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11.7,
        center: sanfran
    });
    // Overlay the zipcode blocks
    map.data.loadGeoJson('/static/zip.geojson');
    map.data.setStyle(function(feature) {
        var zipcode = feature.getProperty('zip_code');
        var color = "gray";
        var opacity = 0.5;
        if (highest.indexOf(parseInt(zipcode)) != -1) {
            // If this zipcode is one of the results, highlight it in red
            color = "red";
            opacity = 0.7;
        }
        return {
            // Fill the map colors for each section accordingly
            fillColor: color,
            strokeWeight: 1,
            fillOpacity: opacity
        }
    });

    // Set up map for Heat Map tab
    // Initialize the map location and zoom
    var heat_map = new google.maps.Map(document.getElementById('heat_map'), {
        zoom: 11.7,
        center: sanfran,
        mapTypeId: 'satellite'
    });
    // Create a heat map using the data
    heatmap = new google.maps.visualization.HeatmapLayer({
        map: heat_map,
        data: getPoints()
    });

    // Set up map for Safe Neighborhoods tab
    // Initialize the map location and zoom
    var neigh_map = new google.maps.Map(document.getElementById('neighborhood_map'), {
        zoom: 11.7,
        center: sanfran
    });
    // Overlay the neighborhood blocks
    neigh_map.data.loadGeoJson('/static/neighborhoods.geojson');
    neigh_map.data.setStyle(function(feature) {
        var neighborhood = feature.getProperty('nhood');
        var color = "gray";
        var opacity = 0.5;
        if (safest.indexOf(neighborhood) != -1) {
            // If this neighborhood is one of the safest, highlight it in red
            color = "red";
            opacity = 0.7;
        }
        return {
            // Fill the map colors for each section accordingly
            fillColor: color,
            strokeWeight: 1,
            fillOpacity: opacity
        }
    });

    // Set up map for Increasing Dispatches tab
    // Initialize the map location and zoom
    var incr_map = new google.maps.Map(document.getElementById('increase_map'), {
        zoom: 11.7,
        center: sanfran
    });
    // Overlay the zipcode blocks
    incr_map.data.loadGeoJson('/static/zip.geojson');
    incr_map.data.setStyle(function(feature) {
        var zipcode = feature.getProperty('zip_code');
        var color = "gray";
        var opacity = 0.5;
        if (increases.indexOf(parseInt(zipcode)) != -1) {
            // If this zipcode is one of the results, highlight it in red
            color = "red";
            opacity = 0.7;
        }
        return {
            // Fill the map colors for each section accordingly
            fillColor: color,
            strokeWeight: 1,
            fillOpacity: opacity
        }
    });
}

// Gets the data for the heat map in proper form using the latitude and longitudes from each call
function getPoints() {
    var result = [];
    for (var i = 0; i < lat_long.length; i++){
        result.push(new google.maps.LatLng(lat_long[i]));
    }
    return result;
}