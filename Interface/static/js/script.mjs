function setupComands() {
    //Gera o bloco de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
    Blockly.Blocks.fwdDistanceMeters = {
        init() {
            this.setColour(290);
            this.appendDummyInput()
            .appendField("Andar em frente por")
            .appendField(new Blockly.FieldNumber(1, 1, 1000, 1), "Distance")
            .appendField("cm");
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setInputsInline(true);
        },
    };

    //Gera o codigo python de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
    Blockly.Python.fwdDistanceMeters = function (block) {
        const distance = block.getFieldValue('Distance') || '\'\'';
        //return `frente()\n`;
        return `car.setDistance(${distance})\nexecute(car.move)\n`;
    };


    //Gera o bloco de andar em um sentido por uma distancia infinitesimal
    Blockly.Blocks.moveDirection = {
        init() {
            this.setColour(290);
            this.appendDummyInput()
                .appendField("Andar para")
                .appendField(new Blockly.FieldDropdown([["Frente", "Frente"], ["Tras", "Tras"]]), "SENTIDO");
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setInputsInline(true);
        },
    };

    //Gera o codigo python de andar em um sentido por uma distancia infinitesimal
    Blockly.Python.moveDirection = function (block) {
        const sentido = block.getFieldValue('SENTIDO');
        if (sentido == "Frente") {
            return `car.setDirection("F")\ncar.setDistance(1)\nexecute(car.move)\n`;
        }

        return `car.setDirection("T")\ncar.setDistance(1)\nexecute(car.move)\n`;
    };


    //Gera o bloco de virar em alguma direcao em um angulo infinitesimal
    Blockly.Blocks.turnLeftOrRight = {
        init() {
            this.setColour(290);
            this.appendDummyInput()
                .appendField("Virar para")
                .appendField(new Blockly.FieldDropdown([["Esquerda", "Esquerda"], ["Direita", "Direita"]]), "DIRECAO");
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setInputsInline(true);
        },
    };

    

    //Gera o codigo python de andar em um sentido por uma distancia infinitesimal
    Blockly.Python.turnLeftOrRight = function (block) {
        const direcao = block.getFieldValue('DIRECAO');
        if (direcao == "Esquerda") {
            return `car.setAngle(-90)\nexecute(car.turn)\n`;
        }

        return `car.setAngle(90)\nexecute(car.turn)\n`;
    };


    //Gera o bloco de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Blocks.turnAngle = {
        init() {
            Blockly.FieldAngle.OFFSET = 90;
            Blockly.FieldAngle.CLOCKWISE = true;
            Blockly.FieldAngle.ROUND = 1;
            this.setColour(290);
            this.appendDummyInput()
                .appendField("Virar em")
                .appendField(new Blockly.FieldAngle(0), "GRAUS")
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setInputsInline(true);
        },
    };

    //Gera o codigo python de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Python.turnAngle = function (block) {
        let graus = block.getFieldValue('GRAUS');
        if (graus >= 180) {
            graus = graus-360;
        }
        return `car.setAngle(${graus})\nexecute(car.turn)\n`;
    };


    //Gera o bloco de ate/enquanto do sensor
    Blockly.Blocks.whileUntil = {
        init() {
            this.appendDummyInput()
                .appendField(new Blockly.FieldDropdown([["Enquanto", "WHILE"], ["Até", "UNTIL"]]), "MODE")
                .appendField("o sensor captar luz");
            this.appendStatementInput("DO")
                .setCheck(null)
                .appendField("O carrinho deve");
            this.setInputsInline(false);
            this.setPreviousStatement(true, null);
            this.setNextStatement(true, null);
            this.setColour(230);
            this.setTooltip("");
            this.setHelpUrl("");
        },
    };

    //Gera o codigo python de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Python.whileUntil = function (block) {
        const until = block.getFieldValue('MODE') === 'UNTIL';
        let argument0 = "car.sensing_light"
        let branch = Blockly.Python.statementToCode(block, 'DO');
        branch = Blockly.Python.addLoopTrap(branch, block) || Blockly.Python.PASS;
        if (until) {
            argument0 = 'not ' + argument0;
        }
        return 'while ' + argument0 + ':\n' + branch;
    };
    
    //Gera o bloco de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
    Blockly.Blocks.setSpeed = {
        init() {
            this.setColour(290);
            this.appendDummyInput()
            .appendField("Define velocidade para")
            .appendField(new Blockly.FieldNumber(30, 1, 100, 1), "Speed")
            .appendField("%");
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setInputsInline(true);
        },
    };
    
    //Gera o codigo python de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
    Blockly.Python.setSpeed = function (block) {
        const speed = block.getFieldValue('Speed') || '\'\'';
        return `car.setSpeed(${speed/100})\n`;
    };

    Blockly.Blocks.genericWhile = {
        init: function() {
          this.appendValueInput("CONDITIONAL")
              .setCheck("Boolean")
              .appendField("Enquanto");
          this.appendStatementInput("DO")
              .setCheck(null)
              .appendField("O carrinho deve");
          this.setInputsInline(false);
          this.setColour(230);
          this.setPreviousStatement(true, null);
          this.setNextStatement(true, null);
        this.setTooltip("");
        this.setHelpUrl("");
        }
      };

    //Gera o codigo python de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Python.genericWhile = function (block) {

        let conditional = Blockly.Python.statementToCode(block, 'CONDITIONAL')|| 'False';
        let branch = Blockly.Python.statementToCode(block, 'DO');
        branch = Blockly.Python.addLoopTrap(branch, block) || Blockly.Python.PASS;
        return 'while (' + conditional + '):\n' + branch;
    };

    

    Blockly.Blocks.genericFor = {
        init: function() {
            this.appendDummyInput()
                .appendField("Repetir")
                .appendField(new Blockly.FieldNumber(1, 0, 100, 1), "Iteration")
                .appendField("vezes :");
            this.appendStatementInput("DO")
                .setCheck(null);
            this.setInputsInline(false);
            this.setColour(230);
            this.setPreviousStatement(true, null);
            this.setNextStatement(true, null);
            this.setTooltip("");
            this.setHelpUrl("");
        }
      };


    Blockly.Python.genericFor = function (block) {
        let i = block.getFieldValue('Iteration')|| '0';
        let branch = Blockly.Python.statementToCode(block, 'DO');
        branch = Blockly.Python.addLoopTrap(branch, block) || Blockly.Python.PASS;
        return `for _ in range(${i}):\n${branch}`;
    };


    Blockly.Blocks.genericIf = {
        init: function() {
          this.appendValueInput("CONDITIONAL")
              .setCheck("Boolean")
              .appendField("Se");
          this.appendStatementInput("DO")
              .setCheck(null)
              .appendField("O carrinho deve");
          this.setInputsInline(false);
          this.setColour(230);
          this.setPreviousStatement(true, null);
          this.setNextStatement(true, null);
        this.setTooltip("");
        this.setHelpUrl("");
        }
      };

    //Gera o codigo python de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Python.genericIf = function (block) {

        let conditional = Blockly.Python.statementToCode(block, 'CONDITIONAL')|| 'False';
        let branch = Blockly.Python.statementToCode(block, 'DO');
        branch = Blockly.Python.addLoopTrap(branch, block) || Blockly.Python.PASS;
        return 'if (' + conditional + '):\n' + branch;
    };

    Blockly.Blocks.genericElse = {
        init: function() {
          this.appendDummyInput()
              .appendField("Senão");
          this.appendStatementInput("DO")
              .setCheck(null)
              .appendField("O carrinho deve");
          this.setInputsInline(false);
          this.setColour(230);
          this.setPreviousStatement(true, null);
          this.setNextStatement(true, null);
        this.setTooltip("");
        this.setHelpUrl("");
        }
      };

    //Gera o codigo python de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Python.genericElse = function (block) {

        let branch = Blockly.Python.statementToCode(block, 'DO');
        branch = Blockly.Python.addLoopTrap(branch, block) || Blockly.Python.PASS;
        return 'else:\n' + branch;
    };

    Blockly.Blocks.lightSensorBool = {
        init: function() {
            this.appendDummyInput()
                .appendField("O sensor")
                .appendField(new Blockly.FieldDropdown([["captar", "True"], ["não captar", "False"]]), "MODE")
                .appendField("luz");
            this.setOutput(true, null);
            this.setInputsInline(false);
            this.setColour(130);
            this.setTooltip("");
            this.setHelpUrl("");
        }
      };

    //Gera o codigo python de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Python.lightSensorBool = function (block) {
        let argument0 = "car.light_sensor == " + block.getFieldValue('MODE');
        return argument0;
    };

    Blockly.Blocks.distSensorBool = {
        init: function() {
            this.appendDummyInput()
                .appendField("O sensor")
                .appendField(new Blockly.FieldDropdown([["captar", "True"], ["não captar", "False"]]), "MODE")
                .appendField("um obstaculo a")
                .appendField(new Blockly.FieldNumber(10, 0, 100, 1), "Distance")
                .appendField("cm de distância");
            this.setOutput(true, null);
            this.setInputsInline(false);
            this.setColour(130);
            this.setTooltip("");
            this.setHelpUrl("");
        }
      };

    //Gera o codigo python de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Python.distSensorBool = function (block) {
        const dist = block.getFieldValue('Distance') || '\'\'';
        return `car.checkDistSensor(${dist/100}) ==  ${block.getFieldValue('MODE')}`;
    };

    Blockly.Blocks.andOrBlock = {
        init: function() {
            this.appendValueInput("CONDITIONAL1")
                .setCheck("Boolean");
            this.appendDummyInput()
                .appendField(new Blockly.FieldDropdown([["e", "and"], ["ou", "or"]]), "MODE");
            this.appendValueInput("CONDITIONAL2")
                .setCheck("Boolean");
            this.setOutput(true, null);
            this.setInputsInline(true);
            this.setColour(290);
            this.setTooltip("");
            this.setHelpUrl("");
        }
      };

    //Gera o codigo python de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Python.andOrBlock = function (block) {
        
        let conditional1 = Blockly.Python.statementToCode(block, 'CONDITIONAL1')|| ' False';
        let conditional2 = Blockly.Python.statementToCode(block, 'CONDITIONAL2')|| ' False';
        let operator = block.getFieldValue('MODE');
        return conditional1 + " " + operator + conditional2;
    };
    
}
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
      "type": "genericFor"
    },
    {
      "kind": "block",
      "type": "genericIf"
    },
    {
      "kind": "block",
      "type": "genericElse"
    },
    {
      "kind": "block",
      "type": "distSensorBool"
    },
    {
      "kind": "block",
      "type": "andOrBlock"
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