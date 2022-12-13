// include the library code:
#include <LiquidCrystal.h>
#include <GFButton.h>
#include <RotaryEncoder.h> 


RotaryEncoder encoder(20, 21); 
int posicaoAnterior = 0;
int posicao;
int regulagem = 0;
int potenciometro = A10;
float valorFinal;
int cont = 0;

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

bool graus = false;
bool velocidade = false;

GFButton botaoEnviar(A0,E_GFBUTTON_PULLDOWN);
GFButton botaoGirar(A1,E_GFBUTTON_PULLDOWN);
GFButton botaoAvancar(A2,E_GFBUTTON_PULLDOWN);

void setup() {
  Serial.begin(9600);
  int origem1 = digitalPinToInterrupt(20);
  int origem2 = digitalPinToInterrupt(21);


  lcd.begin(16, 2);

  pinMode(6,OUTPUT);
  //analogWrite(6,50);
  
  lcd.print("Bem vindo!");
  
  botaoEnviar.setPressHandler(enviar); 
  botaoGirar.setPressHandler(funcoes); 

  
  attachInterrupt(origem1, tickDoEncoder, CHANGE);
  attachInterrupt(origem2, tickDoEncoder, CHANGE);

  pinMode(potenciometro, INPUT);  
  
  
}

void loop() {
  botaoEnviar.process();
  botaoGirar.process();
  botaoAvancar.process();
  
  if (cont%4 == 1){
    
    posicao = encoder.getPosition();
    
    if (posicao != posicaoAnterior) {
      
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Quantos graus?");
      if (posicao > 90){
        encoder.setPosition(90);
        }
      else if (posicao < -90){
        encoder.setPosition(-90);
        }
        
      lcd.setCursor(0,1);
      lcd.print(posicao);
      posicaoAnterior = posicao;
    }
     
    }
    
  else if (cont%4 == 2){
    
    
    int posicao = encoder.getPosition();
    if (posicao != posicaoAnterior) {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Velocidade?");
      if (posicao > 100){
        encoder.setPosition(100);
        }
       else if (posicao < 0){
        encoder.setPosition(0);
        }
      lcd.setCursor(0,1);
      lcd.print(posicao);
      posicaoAnterior = posicao;
  }
  }
  else if (cont%4 == 3){
    
    
    int posicao = encoder.getPosition();
    if (posicao != posicaoAnterior) {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Mover quanto?");
      if (posicao > 3){
        encoder.setPosition(3);
        }
       else if (posicao < 0){
        encoder.setPosition(0);
        }
      lcd.setCursor(0,1);
      lcd.print(posicao);
      posicaoAnterior = posicao;
  }
  }
   
}


void tickDoEncoder() {
  encoder.tick();
}


void enviar(){
  regulagem = posicao;
  
  if (cont % 4 == 1){
    String comando = "/turn/";
    String comando_final = comando + regulagem;
    Serial1.println(comando_final);
  }
   
  

  else if (cont % 4 == 2){
    String comando = "/speed/";
    String comando_final = comando + regulagem;
    Serial1.println(comando_final);
   }

  else if (cont % 4 == 3){
    
   if (regulagem >= 0){
     String comando = "/f/";
     String comando_final = comando + regulagem;
     Serial1.println(comando_final);
    
   }
   
   else if (regulagem < 0){
     String comando = "/t/";
     String comando_final = comando + regulagem;
     Serial1.println(comando_final);
    }
   
   
  }
  }
  
 


void funcoes(){
  lcd.clear();
  cont++;
  if (cont % 4 == 0){
    lcd.print("Bem vindo!");
  }
  
  else if (cont % 4 == 1){
    lcd.print("Qual angulo?");
  }

  else if (cont % 4 == 2){
    lcd.print("Qual velocidade?");
   }

  else if (cont % 4 == 3){
   lcd.print("Mover quanto?");
  }
  

  
  
}
