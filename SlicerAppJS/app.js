const info = require("./info");                           //impots info.js file so we can call related functions

const readline = require("readline");                     
const fs = require("fs");                                 

const rl = readline.createInterface({                     //takes in path as keyboard input.
  input: process.stdin,
  output: process.stdout,
});

rl.question("Input File Path of Gcode file: ", (path) => { //prompt for file path.
  const fileContents = fs.readFileSync(path, "utf8");      //reads the file located at specified path.

  info.printModelInfo(fileContents);                       //passes the content of the file to printmodelinfo which process and prints info about model.
                                                           //the printModuleInfo is located in gCodeReader file.

  rl.close();                                              
});

// /Users/dexter/Downloads/low_poly_unicorn.gcode
// /Users/dexter/Downloads/low_poly_unicorn_0.4n_0.2mm_ABS_MK4_3h19m.gcode
