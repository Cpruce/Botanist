module.exports = {
  name: 'Powernet',
  style: {
    font: 'Roboto',
    titlecol : 'green',
    titlebg : '#fff'
  },
  boards: [
    {
      name: 'Geolocation ',
      widgets: [
        { type: 'map' }       
      ]
    }, {
      name: 'Aggregation',
      widgets: [
        { type: 'barchart', properties: { title : 'Bar Chart Widget' } },
        { type: 'linechart' }
      ]
    }, {
      name: 'Search',
      widgets: [
        { type: 'piechart', properties: { title : 'Pie Chart Widget' } },
        { type: 'scatterplot' }
      ]
    }, {
      name: 'Power Consumption',
      widgets: [
        { type: 'gaugechart', properties: { title : 'Pie Chart Widget' } },
        { type: 'table', properties: { name: 'Device List' } }
      ]
    }, {
      name: 'Price Levels',
      widgets: [
        { type: 'piechart', properties: { title : 'Pie Chart Widget' } },
        { type: 'fdgraph' }
      ]
    }]
};
