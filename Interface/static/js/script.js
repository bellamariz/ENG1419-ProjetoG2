import { setupComands } from "./comandos.js";
console.log("Funcionando");

console.log("antes")
setupComands();

console.log("dps")
var toolbox = {
  "kind": "flyoutToolbox",
  "contents": [
    {
      "kind": "block",
      "type": "controls_if"
    },
    {
      "kind": "block",
      "type": "controls_whileUntil"
    },
    {
      "kind": "block",
      "type": "controls_repeat_ext"
    },
    {
      "kind": "block",
      "type": "logic_compare"
    },
    {
      "kind": "block",
      "type": "math_number"
    },
    {
      "kind": "block",
      "type": "math_arithmetic"
    },
    {
      "kind": "block",
      "type": "text"
    },
    {
      "kind": "block",
      "type": "text_print"
    },
    {
      "kind": "block",
      "type": "text_trim"
    },
    {
      "kind": "block",
      "type": "moveSense"
    },
    {
      "kind": "block",
      "type": "turnDirection"
    },
    {
      "kind": "block",
      "type": "whileUntil"
    },
    {
      "kind": "block",
      "type": "fwdDistanceMeters",
      "inputs": {
        "Distance": {
          "shadow": {
            "kind": "block",
            "type": "math_number",
            "fields": {
              "NUM": "1.0"
            }
          }
        }
      }
    },
    {
      "kind": "block",
      "type": "setSpeed",
      "inputs": {
        "Speed": {
          "shadow": {
            "kind": "block",
            "type": "math_number",
            "fields": {
              "NUM": "1.0"
            }
          }
        }
      }
    }
  ]
}
let workspace = Blockly.inject('blocklyDiv', {toolbox: toolbox});
let bloco = document.getElementById("blocklyDiv")
console.log(bloco)

function updateCode(event) {
  const pythonCode = Blockly.Python.workspaceToCode(workspace);
  document.getElementById('blocklyDiv').value = pythonCode;
  console.log(document.getElementById('blocklyDiv').value);
}
workspace.addChangeListener(updateCode);

function buttonCodeSubmitClickHandler(){
  let pythonCode = document.getElementById('blocklyDiv').value;
  
  fetch("http://127.0.0.1:5000", {
    method: 'post',
    body: pythonCode,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    }).then((res) => {
        if (res.status === 201) {
            console.log("Post successfully created!")
        }
    }).catch((error) => {
        console.log(error)
    });
    console.log("ta indo");
}

document.getElementById('buttonCodeSubmit').addEventListener("click", buttonCodeSubmitClickHandler);