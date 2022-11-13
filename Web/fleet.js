import './fleet.css';
import {Map, View} from 'ol';
import OSM from 'ol/source/OSM';
import Feature from 'ol/Feature';
import Overlay from 'ol/Overlay';
import Point from 'ol/geom/Point';
import TileJSON from 'ol/source/TileJSON';
import VectorSource from 'ol/source/Vector';
import {Icon, Style} from 'ol/style';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';

const map = new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM()
    })
  ],
  view: new View({
    center: [3710000, 4160000],
    zoom: 9
  })
}); 

const iconFeature = new Feature({
  geometry: new Point([3710000, 4160000]),
  name: 'Truck 1',
  info: "Christos Christou",
});

const iconStyle = new Style({
  image: new Icon({
    scale: 0.4,
    anchor: [0.5, 46],
    anchorXUnits: 'fraction',
    anchorYUnits: 'pixels',
    src: 'data/truck_green.png',
  }),
});

iconFeature.setStyle(iconStyle);

const vectorSource = new VectorSource({
  features: [iconFeature],
});

const vectorLayer = new VectorLayer({
  source: vectorSource,
});

const rasterLayer = new TileLayer({
  source: new TileJSON({
    url: 'https://a.tiles.mapbox.com/v3/aj.1x1-degrees.json?secure=1',
    crossOrigin: '',
  }),
});

map.addLayer(vectorLayer, rasterLayer);

//Function to refresh the points
function refreshPoints() {
  //Get all the points from the map
  let features = vectorSource.getFeatures();
  //Loop through the points
  let string1 = "<table><tr><th>Truck</th><th>Driver</th><th>Location</th></tr>";
  let string2 = "";
  for (const element of features) {
    //Get the current point
    let feature = element;
    //Get the current point's Name 
    let name = feature.get('name');
    //Get the current point's Info
    let info = feature.get('info');
    //Get the current point's coordinates
    let coordinates = feature.getGeometry().getCoordinates();
    //Add point to html
    string2 += "<tr><td>" + name + "</td><td>" + info + "</td><td>" + coordinates + "</td></tr>";
  }
  string2 += "</table1>";
  //Add the points to the html
  document.getElementById("fleet-table").innerHTML = string1 + string2;
}

window.addEventListener('load', refreshPoints);


//Function to add a new truck
function addTruck() {
  let latit = document.getElementById("lat").value;
  let longit = document.getElementById("lon").value;
  //if either of the fields is empty, return
  if (latit == "" || longit == "") {
    return false;
  }
  let _name = "Truck 2";
  let _info = "Christos Christou";
  const newTruck = new Feature({
    geometry: new Point([longit, latit]),
    name: _name,
    info: _info,
  });
  newTruck.setStyle(iconStyle);
  vectorSource.addFeature(newTruck);
  vectorLayer.setSource(vectorSource);
  refreshPoints();
  return true;
}

document.getElementById("add_point").addEventListener("click", addTruck);

const overlayContainerElement = document.querySelector('.overlay-container');
const overlayLayer = new Overlay({
  element: overlayContainerElement
})

map.addOverlay(overlayLayer);
const overlayFeatureName = document.getElementById('feature-name');
const overlayFeatureInfo = document.getElementById('feature-info');


map.on('pointermove', function(evt) {
  if (evt.dragging) {
    overlayLayer.setPosition(undefined);
    return;
  }
  map.getTargetElement().style.cursor = map.hasFeatureAtPixel(evt.pixel) ? 'pointer' : '';

  overlayLayer.setPosition(undefined);

  map.forEachFeatureAtPixel(evt.pixel, function(feature, layer) {
    let clickedCoordinate = evt.coordinate
    let clickedFeatureName = feature.get('name');
    let clickedFeatureInfo  = feature.get('info');
    console.log(clickedFeatureName, clickedFeatureInfo);
    overlayLayer.setPosition(clickedCoordinate);
    overlayFeatureName.innerHTML = clickedFeatureName;
    overlayFeatureInfo.innerHTML = clickedFeatureInfo;
  })
});





