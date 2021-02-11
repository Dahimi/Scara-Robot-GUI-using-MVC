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
  cmdvit = 100;
    delay(100);
  Serial.println("communication is set ") ; 
}
void loop() {
  // put your main code here, to run repeatedly:
  // s'il y a des données sur le port on les lit
  if(Serial.available() > 0  ) {  
      // fonction pour traiter les données reçues à partir du moniteur ( surtout le format)     
      handleComingData();
      // Envoyer la commande aux servos 
      moveServo();
     

  }    

}
// Traiter les messages reçues à partir du port 
void handleComingData(){
  
  int readCharacter = Serial.readBytesUntil('\n', readbuffer, 20); 
      message = ""; 
      for(int i = 0 ; i< readCharacter; i++){
        message += readbuffer[i];
      }
      // le format du message reçu est de la forme : "theta1 theta2 mode"
      // affecter à chaque variable sa valeur correspondante 
      //  23.67 23.90 23.4
      theta1 = message.substring(0,message.indexOf(' ')).toFloat();
      theta2 = message.substring(message.indexOf(' '),message.lastIndexOf(' ')).toFloat(); 
      mode = message.substring(message.lastIndexOf(' ')).toInt();
      translationDesAngles();
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

//void handleMode(){
//   if(mode==0){
//      digitalWrite(electroPin,HIGH);
//      delay(50);
//      digitalWrite(electroPin,LOW);
//    }
//   if(mode==1){
//    digitalWrite(electroPin,HIGH);
//    delay(50);}
//   if(mode==2){digitalWrite(electroPin,HIGH);delay(5000);}
//   if(mode==3){digitalWrite(electroPin,HIGH);}
//   if(mode==4){digitalWrite(electroPin,LOW); delay(5000);}
//   if(mode==5){digitalWrite(electroPin,LOW);}
//}
void handleMode(){
   if(mode==0){
    if (b ==0) {
        descente();
        delay(1000);
        monter();
        }  
     else {
      monter();  
       b=0;     
     }    
   }
   if(mode==1){
    if (b==1) {}
  else {
    descente();
    delay(1000);
  b=1;
  }
   }
   if(mode==2){
    Dynamixel.turn(3,RIGTH,1023);
    delay(2900);
    Dynamixel.turn(3,RIGTH,0);
    digitalWrite(electroPin,HIGH);delay(3000);
     Dynamixel.turn(3,LEFT,1023);
      delay(2900);
     Dynamixel.turn(3,RIGTH,0);}
   if(mode==3){
  digitalWrite(electroPin,HIGH);}
   if(mode==4){
    Dynamixel.turn(3,RIGTH,1023);
    delay(2900);
    Dynamixel.turn(3,RIGTH,0);
    digitalWrite(electroPin,LOW); delay(3000);
     Dynamixel.turn(3,LEFT,1023);
    delay(2900);
    Dynamixel.turn(3,RIGTH,0);
    }
   if(mode==5){
  digitalWrite(electroPin,LOW);}
}
// fonction pour attendre les servos 
void waitForServo(){
  while(Dynamixel.moving(dynamixel1) == 1 or Dynamixel.moving(dynamixel2) == 1)delay(10);
}
void translationDesAngles(){
  theta1 = 360 - theta1;
  theta2 = 180 -theta2;
   
}
void descente(){
        Dynamixel.turn(3,RIGTH,1023);
        delay(2900*2);
        Dynamixel.turn(3,RIGTH,0);
}
void monter(){
  Dynamixel.turn(3,LEFT,1023);
        delay(2900*2); 
       Dynamixel.turn(3,LEFT,0);
}
