import React from 'react';
import ReactDOM from 'react-dom';
import NVD3Chart from './lib/react-nvd3.js';
import $ from 'jquery';
import './css/nv.d3.min.css';

var HHStatusData = [
    {
        'hh_id':'1',
        'name':'Slac',
        'online':'true',
        'total_power':'89'
    },
    {
        'hh_id':'2',
        'name':'CMU sv',
        'online':'true',
        'total_power':'304'
    },
    {
        'hh_id':'3',
        'name':'Yizhe Home',
        'online':'false',
        'total_power':'30'
    }
];

var DonutPieChartBox = React.createClass({
  getX: function(d) {
    return d.label;
  },
  getY: function(d) {
    return d.value;
  },
  getInitialState: function() {
    return {data: []};
  },
  render: function() {
    var pieData = HHStatusData.map( function(hhinfo) {
      return (
        {
          "label" : hhinfo.name,
          "value" : hhinfo.total_power
        }
      );
    });

    return (
      <NVD3Chart
        type="pieChart"
        datum={pieData}
        x={this.getX}
        y={this.getY}
        duration="1300"
        donut="true"
        donutRatio="0.35" />
    );
  }
});

export default DonutPieChartBox;
