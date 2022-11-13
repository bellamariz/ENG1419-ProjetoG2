
console.log("Funcionando");

Blockly.Blocks.teste_blockly = {
  // Block for text to sleep.
  init() {
    this.setColour(290);
    this.appendValueInput('Distance')
      .setCheck('Number')
      .appendField("Andar em frente por");
      this.appendDummyInput()
        .appendField("Metros");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setInputsInline(true);
  },
};

Blockly.Python.teste_blockly = function (block) {
  // Generate Python for sleeping.
  const distance = Blockly.Python.valueToCode(block, 'Distance',
    Blockly.Python.ORDER_NONE) || '\'\'';
  return `car.foward(${distance})\n`;
};

var toolbox = {
  "kind": "flyoutToolbox",
  "contents": [
    {
      "kind": "block",
      "type": "controls_if"
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
      "type": "teste_blockly",
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
    }
  ]
}
let workspace = Blockly.inject('blocklyDiv', {toolbox: toolbox});
let bloco = document.getElementById("blocklyDiv")
console.log(bloco)

function updateCode(event) {
  const pythonCode = Blockly.Python.workspaceToCode(workspace);
  document.getElementById('blocklyDiv').value = pythonCode;
  console.log(pythonCode);
}
workspace.addChangeListener(updateCode);