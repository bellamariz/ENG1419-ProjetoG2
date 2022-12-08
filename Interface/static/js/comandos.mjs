export function setupComands() {
    //Gera o bloco de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
    Blockly.Blocks.fwdDistanceMeters = {
        init() {
            this.setColour(290);
            this.appendDummyInput()
            .appendField("Andar em frente por")
            .appendField(new Blockly.FieldNumber(1, 0, 10000, 0.01), "Distance")
            .appendField("Metros");
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setInputsInline(true);
        },
    };

    //Gera o codigo python de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
    Blockly.Python.fwdDistanceMeters = function (block) {
        const distance = block.getFieldValue('Distance') || '\'\'';
        //return `frente()\n`;
        return `car.forward(${distance})\n`;
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
            return `car.setDirection("F")\ncar.move()\n`;
        }

        return `car.setSpeed("T")\ncar.move()\n`;
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
            return `car.turn(-90)\n`;
        }

        return `car.turn(90)\n`;
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
        return `car.turn(${graus})\n`;
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
            .appendField(new Blockly.FieldNumber(0.3, 0, 1, 0.1), "Speed")
            .appendField("teemos/ticks");
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setInputsInline(true);
        },
    };
    
    //Gera o codigo python de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
    Blockly.Python.setSpeed = function (block) {
        const speed = block.getFieldValue('Speed') || '\'\'';
        return `car.setSpeed(${speed})\n`;
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

    Blockly.Blocks.lightSensorBool = {
        init: function() {
            this.appendDummyInput()
                .appendField("Sensor")
                .appendField(new Blockly.FieldDropdown([["está", "True"], ["não está", "False"]]), "MODE")
                .appendField("captando luz");
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
                .appendField("Sensor de distancia")
                .appendField(new Blockly.FieldDropdown([["está", "True"], ["não está", "False"]]), "MODE")
                .appendField("captando algum obstaculo");
            this.setOutput(true, null);
            this.setInputsInline(false);
            this.setColour(130);
            this.setTooltip("");
            this.setHelpUrl("");
        }
      };

    //Gera o codigo python de virar em alguma direcao em um angulo especificado pelo usuario
    Blockly.Python.distSensorBool = function (block) {
        let argument0 = "car.dist_sensor == " + block.getFieldValue('MODE');
        return argument0;
    };
    
}