var DataBox = React.createClass({
  getX: function(d) {
    return d[0]
  },
  getY: function(d) {
    return d[1]
  },
  chartConfigure: function(chart) {
    chart.xAxis.tickFormat(function(d) { return d3.time.format('%x')(new Date(d)) });
    chart.yAxis.tickFormat(d3.format(',.4f'));
    chart.legend.vers('furious');
  },
  getInitialState: function() {
    return {data: []};
  },
  loadDatasFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function() {
    this.loadDatasFromServer();
    setInterval(this.loadDatasFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <NVD3Chart
        type="stackedAreaChart"
        datum={this.state.data}
        x={this.getX}
        y={this.getY}
        controlLabels={{stacked:"Stacked"}}
        duration="300"
        configure = {this.chartConfigure}/>
    );
  }
});

ReactDOM.render(
  <DataBox url="/api/data" pollInterval={2000} />,
  document.getElementById('barChart')
);
