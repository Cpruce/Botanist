var jsonfile = require('jsonfile')

var file = './data.json'
var output = []
var tsNow = Date.now()

var output  = [];
for (var i = 0; i < 3; i++) {
  output.push([]);
}

for (var i = 0; i < 20; i++) {
  tsNow = tsNow + Math.floor((Math.random() * 100000) + 1);
  for (var j = 0; j < 3; j++) {
    output[j].push([tsNow, Math.floor((Math.random() * 100) + 1)]);
  }
}

var obj = [{key: "Slac", values : output[0]}, {key: "CMU sv", values : output[1]}, {key: "Yizhe Home", values : output[2]}]

jsonfile.writeFile(file, obj, function (err) {
  console.error(err)
})
