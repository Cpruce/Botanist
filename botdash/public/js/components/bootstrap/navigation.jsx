import React from 'react';
import ReactDOM from 'react-dom';
import './css/dashboard.css';

var navEntries = [
    {
        "id" : 1,
        "text": " Dashboard ",
        "link": "index.html"
    },
    {
        "id" : 2,
        "text": " Home Hubs ",
        "link": "#"
    },
    {
        "id" : 3,
        "text": " Map ",
        "link": "maps.html"
    },
    {
        "id" : 4,
        "text": " Aggregation ",
        "link": "aggregation.html"
    }
];

//So update this dynamically
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


var NavTopbar = React.createClass({
  render : function() {
    return (
      <div className="navbar-header">
        <a className="navbar-brand" href="/">Powernet Dashboard</a>
      </div>
    );
  }
});

var NavSidebar = React.createClass({

  /*_nav_change : function(){
    var path = window.location.pathname;
    console.log(path);
    switch(path){


    }
  }*/

  render : function() {
    var secondLevelLinkForHH = HHStatusData.map(function(item) {
      return (
        <li key={item.hh_id} >
          <a href={'hh/' + item.hh_id}> {item.name} </a>
        </li>
      );
    });

    navEntries.map(function(navEntry) {
      if (navEntry.id === 2) {
        navEntry.hasSecondLevel = true;
      };
    });

    var navSidebarItems = navEntries.map(function(item) {
      if (item.hasSecondLevel === true) {
        return(
          <li key={item.id}>
            <a href={item.link}>
              <i className="fa fa-dashboard fa-fw"></i>
              {item.text}
              <span className="fa arrow"></span>
            </a>
            <ul className="nav nav-second-level collapse">
              {secondLevelLinkForHH}
            </ul>
          </li>
        )
      } else {
        return(
          <li key={item.id}>
            <a href={item.link}>
              <i className="fa fa-dashboard fa-fw"></i>
              {item.text}
            </a>
          </li>
        )
      }
    });

    return (
      <div className="navbar-default sidebar" role="navigation">
        <div className="sidebar-nav navbar-collapse">
            <ul className="nav" id="side-menu">
                {navSidebarItems}
            </ul>
        </div>
      </div>
    );
  }
});

var navigationStyle = {
  margin: 0
};

var Navigation = React.createClass({
  render : function() {
    return (
        <nav className="navbar navbar-default navbar-static-top" role="navigation" style={navigationStyle}>
            <NavTopbar />
            <NavSidebar />
        </nav>
    );
  }
})

ReactDOM.render(
  <Navigation />,
  document.getElementById('react-navigation')
);
