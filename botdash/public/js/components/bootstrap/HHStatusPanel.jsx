import React from 'react';
import ReactDOM from 'react-dom';
import './css/dashboard.css';

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

var HHStatusPanel = React.createClass({
    render: function() {
        var panels = [];
        for (var i = 0; i < (HHStatusData.length / 3); i++) {
            var oneRow = [];
            for (var j = 0; j < 3; j++) {
                var hhindex = i * 3 + j;
                var onePanel = (
                    <div className="col-lg-3 col-md-6" key={HHStatusData[hhindex].hh_id}>
                        <div className="panel panel-primary">
                            <div className="panel-heading">
                                <div className="row">
                                    <div className="col-xs-3">
                                        <i className="fa fa-flash fa-5x"></i>
                                    </div>
                                    <div className="col-xs-9 text-right">
                                        <div>
                                            <div className="huge">
                                                {HHStatusData[hhindex].total_power} KW
                                            </div>
                                        </div>
                                        <div>{HHStatusData[hhindex].name}</div>
                                    </div>
                                </div>
                            </div>
                            <a href={'hh/' + HHStatusData[hhindex].hh_id}>
                                <div className="panel-footer">
                                    <span className="pull-left">View Details</span>
                                    <span className="pull-right"><i className="fa fa-arrow-circle-right"></i></span>
                                    <div className="clearfix"></div>
                                </div>
                            </a>
                        </div>
                    </div>
                );
                oneRow.push(onePanel);
                oneRow.key = i;
            };
            panels.push(oneRow);
        };

        var allPanels = panels.map(function(oneRow) {
                return (
                    <div className="col-lg-12" key={oneRow.key} >
                        {oneRow}
                    </div>
                );
        });

        return (
            <div>
                {allPanels}
            </div>
        );
    }
})


ReactDOM.render(
  <HHStatusPanel />,
  document.getElementById('react-HHStatusPannel')
);


