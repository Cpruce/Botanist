var React = require('react');
var BaseWidget = require('BaseWidget');

var L = require('leaflet');
require('../../../../node_modules/leaflet/dist/leaflet.css');
L.Icon.Default.imagePath = 'images';

var Widget = React.createClass({
  getDefaultProps: function(){
    return {
      center : [37.410401,-122.060032],
      marker : [
            {
                'latlng': [37.410401,-122.060032], 
                'text': 'CMU'
            },
            {
                'latlng': [37.4201052, -122.2021446],
                'text' : 'SLAC'
            }
      ],
      zoomLevel : 10,
      wmsTileLayerUrl : 'http://tile.stamen.com/toner/{z}/{x}/{y}.png'
    }
  },
  
  propTypes: {
    center: React.PropTypes.array,
    marker : React.PropTypes.array,
    zoomLevel : React.PropTypes.number,
    wmsTileLayerUrl : React.PropTypes.string
  },
  
  componentDidMount: function(){
    this.zoomControlOptions = { position: 'bottomright' };
    this.mapDefaultOptions = {zoomControl : false};

    this.createMap();
  },
  
  componentWillUnmount: function(){
    this.map.remove();
  },
  
  createMap : function(){
      
    this.map = L.map(this.props._id, this.mapDefaultOptions)
      .setView(this.props.center, this.props.zoomLevel)
      .addControl(L.control.zoom(this.zoomControlOptions))
      .addLayer(L.tileLayer(this.props.wmsTileLayerUrl, {maxZoom: 18}))
                
    this.createMarker();
  },
  
  createMarker : function(){
    if(this.props.marker){
      this.props.marker.forEach(function(marker,i){
        var mapMarker = L.marker(marker.latlng, {title: marker.text}).addTo(this.map);
        
        if(marker.text){
          mapMarker.bindPopup(marker.text)
        }
      }.bind(this));
    }
  },

  
  render: function() {
    
    var style = { height : '100%' },
      widget = (
      <div className="botanist-widget-map">
        <div style={ style } id={ this.props._id }></div>
      </div>
    );

    return (
      <BaseWidget { ...this.props } widget={ widget }/>
    );
  }

});

module.exports = Widget;
