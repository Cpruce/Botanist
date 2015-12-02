var React = require('react');
var ChartMixin = require('../../mixins/rdb-chart-mixin.js');
var BaseWidget = require('BaseWidget');

var Widget = React.createClass({
  mixins: [ChartMixin],
  
  getDefaultProps: function(){
    return {
        data : [{ data1: 0.30, d2: 0.2, d3: 0.5 },{ data2: .20 },{ data3: .5 }]
    }
  },
  
  propTypes: {
    data: React.PropTypes.array
  },
  
  componentDidMount: function () {
    this.chart = this.createChart({ type : 'pie' });
  },
  
  componentWillUnmount: function(){
     this.chart = this.chart.destroy();
  },
  
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
