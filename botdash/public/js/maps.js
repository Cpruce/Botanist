import NavSidebar from './components/bootstrap/navigation.jsx';

import React from 'react';
import { render } from 'react-dom';
import PowernetMap from './components/mapwidget/simple';

import "../bower_components/leaflet/dist/leaflet.css";
import "../css/maps.css"

const examples = (
  <div>
    <PowernetMap />
  </div>
);

render(examples, document.getElementById('map-container'));
