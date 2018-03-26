// Set up the points for the first visual graph
var visual1 = [];
for(var i = 0; i < calls.length; i++){
    visual1.push({x: i, y: calls[i]});
}
// Create the line graph
new Chartist.Line('#visual1', {
  series: [visual1]
}, {
  axisX: {
    type: Chartist.AutoScaleAxis,
    onlyInteger: true,
    low: 0
  }
});

// Set up the labels and amounts for visual graph #2
var visual2_labels = [];
var visual2_series = [];
for (var key in districts) {
    visual2_labels.push(key);
    visual2_series.push(districts[key]);
}
// Create the bar graph
new Chartist.Bar('#visual2', {
    labels: visual2_labels,
    series: [visual2_series]
}, {
    axisX: {
        onlyInteger: false
    }
});

//Set up the labels and amounts for visual char #3
var visual3_labels = [];
var visual3_series = [];
for (var key in units) {
    visual3_labels.push(key);
    visual3_series.push(units[key]);
}
// Create the pie chart
new Chartist.Pie('#visual3', {
    labels: visual3_labels,
    series: visual3_series
    }, {
      labelInterpolationFnc: function(value) {
        return value[0]
      }
    },
    // Add the labels onto the chart
    [['screen and (min-width: 640px)', {
        chartPadding: 30,
        labelOffset: 100,
        labelDirection: 'explode',
        labelInterpolationFnc: function(value) {
          return value;
        }
      }]
    ]
);
