const GCODE = require("./gCodeReader.js");                                //imports file to use its gcode reading functions
const { parseGCode } = require("./Worker.js");                            //imports file to use it s gcode analysis functions

// console.log("GCODE is undefined Dexter: ", GCODE);

var printModelInfo = function (fileContent) {                             //what is called from app.js, where it takes in a file, analyses it and then returns model info.
  const message = GCODE.loadFile(fileContent);
  parseGCode(message);
  var resultSet = [];
  var modelInfo = GCODE.getModelInfo();
  var gCodeOptions = GCODE.getOptions();

  let totalFilament = modelInfo.totalFilament;
  let totalWeight = modelInfo.totalWeight;
  let filamentByExtruder = modelInfo.filamentByExtruder;
  if (gCodeOptions.volumetricE) {
    let fCrossSection = Math.PI * Math.pow(gCodeOptions.filamentDia / 2.0, 2);
    totalFilament /= fCrossSection;
    totalWeight /= fCrossSection;
    for (let k in filamentByExtruder) filamentByExtruder[k] /= fCrossSection;
  }

  resultSet.push(
    "Model size is: " +
      modelInfo.modelSize.x.toFixed(2) +
      "x" +
      modelInfo.modelSize.y.toFixed(2) +
      "x" +
      modelInfo.modelSize.z.toFixed(2) +
      "mm"
  );
  resultSet.push("Total filament used: " + totalFilament.toFixed(2) + "mm");
  resultSet.push("Total filament weight used: " + totalWeight.toFixed(2) + "grams");
  var i = 0,
    tmp = [];
  for (var key in modelInfo.filamentByExtruder) {
    i++;
    tmp.push("Filament for extruder '" + key + "': " + filamentByExtruder[key].toFixed(2) + "mm");
  }
  if (i > 1) {
    resultSet.push(tmp.join(""));
  }
  resultSet.push(
    "Estimated print time: " +
      parseInt(parseFloat(modelInfo.printTime) / 60 / 60) +
      ":" +
      parseInt((parseFloat(modelInfo.printTime) / 60) % 60) +
      ":" +
      parseInt(parseFloat(modelInfo.printTime) % 60) +
      ""
  );
  resultSet.push("Estimated layer height: " + modelInfo.layerHeight.toFixed(2) + "mm");
  resultSet.push(
    "Layer count: " +
      modelInfo.layerCnt.toFixed(0) +
      "printed, " +
      modelInfo.layerTotal.toFixed(0) +
      "visited"
  );
  resultSet.push(
    "Time cost: " + ((modelInfo.printTime * gCodeOptions.hourlyCost) / 60 / 60).toFixed(2)
  );
  resultSet.push("Filament cost: " + (totalWeight * gCodeOptions.filamentPrice).toFixed(2));
  console.log(resultSet);
};

module.exports.printModelInfo = printModelInfo;
