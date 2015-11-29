/**
 * Widgets can use this class to display their content.
 * Usage: <BaseWidget { ...this.props } widget={ widget }/>
 */

var React = require('react');
var BaseWidget = require('BaseWidget');

var BotGraph = React.createClass({

  render: function() {    
    
      
    return (
    <BaseWidget />);
  }

});

module.exports = BaseWidget;
