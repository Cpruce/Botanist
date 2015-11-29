var React = require('react');
var Router = require('react-router');
var { Route, DefaultRoute, NotFoundRoute } = Router;
var ForceDirectedGraph = require('../../factories/force-directed-graph.jsx');
var BaseWidget = require('BaseWidget');
var d3 = require('d3');

var Widget = React.createClass({
  getDefaultProps: function(){
    return {
    
    }
  },
  
  propTypes: {
  
  },
  
  componentDidMount: function(){
    
  },
  
  componentWillUnmount: function(){

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
