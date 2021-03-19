#include <math.h> 
//Importer la librairie Serial.2 
#include <MX_AX_Serial1.h>
//#include <DynamixelSerial2.h>
// declaration des variables 
// electroPin va être modélisé par une LED 
#define electroPin 10
int isMoving ; 
int b=1;
int Temperature2,Vitesse2,Temperature1,Vitesse1; 
int dynamixel1 = 1 , dynamixel2 = 2; 
String message = "";
char readbuffer[16] ;
float theta1, theta2;
int cmdvit=50;
float position1, position2 ;
boolean isTorque = true, isRecord = false ;
// la variable 'mode' va déterminer si le stylo ( ou l'electroaimant ) est actif on non
int mode ;
int i = 0 ;

void setup() {
  // initialisation des communication avec l'interface graphique et les dynamixels
  pinMode(electroPin,OUTPUT);
  Serial.begin(115200);
  Dynamixel.begin(1000000,2); 
  delay(100);
  // Vitesses par defaut
  //Dynamixel.moveSpeed(dynamixel1,0,cmdvit);
  delay(100);
  //Dynamixel.moveSpeed(dynamixel2,2047,cmdvit);
  Dynamixel.setEndless(dynamixel1, OFF ,ON);
  Dynamixel.setEndless(dynamixel2, OFF ,ON);

  cmdvit = 75;
    delay(100);
  Serial.println("communication is set ") ; 
}
void loop() {
  // put your main code here, to run repeatedly:
  // s'il y a des données sur le port on les lit
  if(Serial.available() > 0  ) {  
      // fonction pour traiter les données reçues à partir du moniteur ( surtout le format)     
      handleComingData();
      
  }    
  if(isRecord == true ){
    if( isTorque == true){
         Dynamixel.torqueStatus(dynamixel1, OFF );
         Dynamixel.torqueStatus(dynamixel2, OFF )  ;
         isTorque = false;
      }   
        position1 = 360 - Dynamixel.readPosition(dynamixel1)* 360.0/4096;
        position2 = 180 - Dynamixel.readPosition(dynamixel2)* 360.0/4096;
        Serial.print(position1);
        Serial.print(" ");
        Serial.println(position2);
        delay(100);
  }
}
// Traiter les messages reçues à partir du port 
void handleComingData(){
  
  int readCharacter = Serial.readBytesUntil('\n', readbuffer, 20); 
      message = ""; 
      for(int i = 0 ; i< readCharacter; i++){
        message += readbuffer[i];
      }
      if (message == "." ){        
       isRecord = true;
     }
     else if(message == ","){
      isRecord = false;
      Serial.println("ok"); 
     }
     else {
      isRecord = false;
      if( isTorque == false){
         Dynamixel.torqueStatus(dynamixel1, ON );
         Dynamixel.torqueStatus(dynamixel2, ON )  ;
         isTorque = true;
      }
      theta1 = message.substring(0,message.indexOf(' ')).toFloat();
      theta2 = message.substring(message.indexOf(' '),message.lastIndexOf(' ')).toFloat(); 
      mode = message.substring(message.lastIndexOf(' ')).toInt();
      translationDesAngles();

      if(mode == 7 or mode == 8){
        if(b ==1){
          monter();
          delay(500);
          b= 0;
        }
      }
      if(mode == 7 ){
        mode = 0;
      }
      if(mode == 8 ){
        mode = 1;
      }
      // Envoyer la commande aux servos 
      moveServo();
     }
}
// Fonction pour commander les servos 
void moveServo(){
  Temperature1 = Dynamixel.readTemperature(dynamixel1); // Request and Print the Temperature       
  Temperature2 = Dynamixel.readTemperature(dynamixel2); // Request and Print the Temperature
  Dynamixel.moveSpeed(dynamixel1,theta1*4095/360,cmdvit);       
  Dynamixel.moveSpeed(dynamixel2,theta2*4095/360,cmdvit);
  Vitesse1 = Dynamixel.readSpeed(dynamixel1);
  Vitesse2 = Dynamixel.readSpeed(dynamixel2);
  // On attend jusqu'à ce que les servos atteignent le point 
  waitForServo();
  // Cette fonction permet de savoir l'état du stylo ou de l'electroaimant (0 ou 1)
  handleMode();
  // Print the variables in the Serial Monitor
  Serial.print(Temperature2);
  Serial.print(" ");
  Serial.print(Temperature2);
  Serial.print(" ");
  Serial.print(Vitesse1);
  Serial.print(" ");
  Serial.println(Vitesse2);
  
}
//}
void handleMode(){
   if(mode==0){
    if (b ==0) {
        descente();
        delay(1000);
        monter();
        delay(100);
        }  
     else {
      monter();
      delay(100);  
       b=0;     
     }    
   }
   if(mode==1){
    if (b==1) {}
  else {
    descente();
    delay(1000);
  b=1;
  } }
}
// fonction pour attendre les servos 
void waitForServo(){
  while(Dynamixel.moving(dynamixel1) != 0 or Dynamixel.moving(dynamixel2) != 0)delay(10);
}
void translationDesAngles(){
  theta1 = 360 - theta1;
  theta2 = 180 -theta2;
   
}
void descente(){
        Dynamixel.turn(3,RIGTH,1023);
        delay(3500);//2900*2
        Dynamixel.turn(3,RIGTH,0);
}
void monter(){
  Dynamixel.turn(3,LEFT,1023);
        delay(3500); 
       Dynamixel.turn(3,LEFT,0);
}
