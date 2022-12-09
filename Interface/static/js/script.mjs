import { setupComands } from "./comandos.mjs";
console.log("Funcionando");

console.log("antes")
setupComands();

console.log("dps")
var toolbox = {
  "kind": "flyoutToolbox",
  "contents": [
    {
      "kind": "block",
      "type": "moveDirection"
    },
    {
      "kind": "block",
      "type": "turnLeftOrRight"
    },
    {
      "kind": "block",
      "type": "turnAngle"
    },
    {
      "kind": "block",
      "type": "fwdDistanceMeters",
    },
    {
      "kind": "block",
      "type": "setSpeed",
    },
    {
      "kind": "block",
      "type": "genericWhile"
    },
    {
      "kind": "block",
      "type": "lightSensorBool"
    },
    {
      "kind": "block",
      "type": "distSensorBool"
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
  
  fetch("/", {
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
