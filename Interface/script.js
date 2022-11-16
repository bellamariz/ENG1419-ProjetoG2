
console.log("Funcionando");

Blockly.Blocks.teste_blockly = {
  // Block for text to sleep.
  init() {
    this.setColour(290);
    this.appendValueInput('ELAPSE')
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
  const elapse = Blockly.Python.valueToCode(block, 'ELAPSE',
    Blockly.Python.ORDER_NONE) || '\'\'';
  return `qualquer coisa\n`;
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


const pythonCode = Blockly.Python.workspaceToCode(workspace);

