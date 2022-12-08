export function setupComands() {
    //Gera o bloco de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
    Blockly.Blocks.fwdDistanceMeters = {
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

    //Gera o codigo python de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
    Blockly.Python.fwdDistanceMeters = function (block) {
        const distance = Blockly.Python.valueToCode(block, 'Distance',
            Blockly.Python.ORDER_NONE) || '\'\'';
        return `frente()\n`;
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
}

//Gera o bloco de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
Blockly.Blocks.setSpeed = {
    init() {
        this.setColour(290);
        this.appendValueInput('Speed')
            .setCheck('Number')
            .appendField("Define velocidade para");
        this.appendDummyInput()
            .appendField("teemos/ticks");
        this.setPreviousStatement(true);
        this.setNextStatement(true);
        this.setInputsInline(true);
    },
};

//Gera o codigo python de andar pra frente (forward/fwd) por uma distancia definido pelo usuario
Blockly.Python.setSpeed = function (block) {
    const speed = Blockly.Python.valueToCode(block, 'Speed',
        Blockly.Python.ORDER_NONE) || '\'\'';
    return `car.setSpeed(${speed})\n`;
};
