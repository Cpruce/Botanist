var React = require('react');
var BaseWidget = require('BaseWidget');

//var Mongoose = require('mongoose');

var Widget = React.createClass({

  getInitialState: function(){
    return {name: "", data: []};
  },
  
  propTypes: {
    name: React.PropTypes.string,
    data: React.PropTypes.array
  },

  componentDidMount() {

    this.getUsers(); 
  }, 

  getUsers : function() { //we define a function for getting our users

   $.ajax({ //call ajax like we would in jquery
            url: '/allUsers',  //this is the url/route we stored our users on
            dataType: 'json',
            success: function(data) { //if we get a Success for our http get then..
               this.setState({user:data}); //set the state of our user array to whatever the url returned, in this case the json with all our users
               }.bind(this),
        error: function(xhr, status, err) { //error logging and err tells us some idea what to debug if something went wrong.
                console.log("error");
               console.error(this.props.url,status, err.toString());
            }.bind(this)
        });

   },

  render: function() {
    
    var devices = [{
      id: 1,
      name: "Item name 1",
      price: 100
    },{
      id: 2,
      name: "Item name 2",
      price: 100
    }];

    
    // mongoose stuff


    var style = { padding : '1rem' },
        widget = (
           <div style={ style }>
            <div className="rdb-widget">
                <div id={ this.props._id }> </div>
                <h2 className="table-name">
                    {this.props.name}
                </h2>
                <table className="table">
                    <tr>Name: 'Griffin Smith', Age: 18</tr>
                    <br/>
                    <tr>Age: 23,  Name: 'Lee Salminen' </tr>
                    <br/>
                    <tr>Age: 28, Position: 'Developer' </tr>
                    
                </table>
            </div>
          </div> 
                );    

    return (
      <BaseWidget { ...this.props } widget={ widget }/>
    );
  }
});

module.exports = Widget;
