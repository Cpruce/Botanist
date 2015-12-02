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

var HHDevicesStatus = [
    {
        "id" : 1,
        "device_type" : "Generator",
        "device_name" : "Champion Power Equipment Model 41537",
        "device_status" : "on"
    },
    {
        "id" : 2,
        "device_type" : "Load",
        "device_name" : "Super awesome fan",
        "device_status" : "on"
    },
    {
        "id" : 3,
        "device_type" : "Generator",
        "device_name" : "Champion Power Equipment Model 41537",
        "device_status" : "on"
    },
    {
        "id" : 4,
        "device_type" : "Storage",
        "device_name" : "Champion Power Equipment Model 41537",
        "device_status" : "off"
    },
    {
        "id" : 5,
        "device_type" : "Generator",
        "device_name" : "Champion Power Equipment Model 41537",
        "device_status" : "on"
    }
]

var HHStatusTable = React.createClass({
    render: function() {
        var tableRows = HHDevicesStatus.map(
            function(entry) {
                var rowType;
                if (entry.device_type === "Load") {
                    rowType = "success"
                }
                 else if (entry.device_type === "Generator" ) {
                    rowType = "warning"
                } else {
                    rowType = "info"
                }
                return (
                    <tr className={rowType} key={entry.id}>
                        <td> { entry.device_name } </td>
                        <td> { entry.device_type } </td>
                        <td> { entry.device_status } </td>
                    </tr>
                );
            }
        );
        return (
            <div className = "row" >
                <div className="col-lg-6">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            Context classNames
                        </div>
                        <div className="panel-body">
                            <div className="table-responsive">
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th>Device Name</th>
                                            <th>Device Type</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {tableRows}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
})


ReactDOM.render(
  <HHStatusTable />,
  document.getElementById('react-HHStatusTable')
);
