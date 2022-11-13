import * as leaflet from '/static/libs/leaflet/dist/leaflet.js';

const osm_map = new L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
});


const map = new L.Map('map', {
  layers: [osm_map] // Add the OSM layer to the map
});

map.setView([
  35.0667, 33.3467 //Center coordinates - Cyprus
  ],
  9 //Zoom level
);

const marker_icon = L.icon({
  iconUrl: '/static/img/truck_green.png',
  shadowUrl: '/static/img/marker-shadow.png',

  iconSize: [40, 44], // size of the icon
  shadowAnchor: [14,20],  // the same for the shadow
});

//Function to load all trucks from the database
function loadTrucks() {
  $.ajax({
    url: '/fleet/load_trucks/',
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      for (const element of data) {
        let truck = element;
        let marker = L.marker([truck.lat, truck.lng], {icon: marker_icon}).addTo(map);
        marker.bindPopup(truck.name);
      }
    },
    error: function (data) {
      console.log('Error:', data);
    }
  })}

//Function to add a new truck via HTML debug form
function addTruck() {
  let latit = document.getElementById("lat").value;
  let longit = document.getElementById("lon").value;
  //if either of the fields is empty, return
  if (latit == "" || longit == "") {
    return false;
  }
  let _name = "DEBUG TRUCK";
  let _info = "Name Surname";
  let newMarker = L.marker([latit, longit], {icon: marker_icon,riseOnHover: true}).addTo(map);
  newMarker.bindPopup("<b>" + _name + "</b><br>" + _info);
  newMarker.on('mouseover', function (e) {
    this.openPopup();
  });
  newMarker.on('mouseout', function (e) {
    this.closePopup();
  });
  return true;
}

document.getElementById("add_point").addEventListener("click", addTruck);