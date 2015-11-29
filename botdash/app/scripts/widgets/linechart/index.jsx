var React = require('react');
var ChartMixin = require('../../mixins/rdb-chart-mixin.js');
var BaseWidget = require('BaseWidget');

/*var moment = require('moment');
var Actions = require('../../actions/ChartActions.jsx');
var GraphStore = require('../../stores/ChartStore.jsx');
var _ = require('lodash');
*/

var Widget = React.createClass({
  mixins: [ChartMixin],
  
  getDefaultProps: function(){
    return {
      data : [{ alpha: 100, beta : 120, gamma: 110 },{ alpha: 120, beta : 110, gamma: 90 },{ alpha: 75, beta : 100,gamma: 80 }, { alpha: 100, beta : 120, gamma: 110 },{ alpha: 120, beta : 110, gamma: 90 },{ alpha: 75, beta : 100,gamma: 80 }]
    }
  },

  /*getInitialState: function(){

  }*/
  
  propTypes: {
    data: React.PropTypes.array
  },

  /*componentWillMount: function() {
    

  },*/

  componentDidMount: function () {
     this.chart = this.createChart({ type : 'line' });

     //setInterval(update, 3000);
  },
  
  componentWillUnmount: function(){
     this.chart = this.chart.destroy();
  },

  /*update: function(){
    
    var updatedata = 

    this.chart.load({
        columns: updatedata
    });
  },*/

  render: function() {
    
    var style = { padding : '1rem' },
        widget = (
          <div style={ style }>
            <div className="rdb-widget">
              <div id={ this.props._id }></div>
            </div> 
          </div>);

    return (
      <BaseWidget { ...this.props } widget={ widget }/>
    );
  }
});

module.exports = Widget;
