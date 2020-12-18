#include <math.h> 
//Importer la librairie Serial.2 
#include <DynamixelSerial2.h>
// declaration des variables 
// electroPin va être modélisé par une LED 
#define electroPin 10
int isMoving ; 
int Temperature2,Vitesse2,Temperature1,Vitesse1; 
int dynamixel1 = 1 , dynamixel2 = 2; 
String message = "";
char readbuffer[16] ;
float theta1, theta2;
int cmdvit=300;
// la variable 'mode' va déterminer si le stylo ( ou l'electroaimant ) est actif on non
int mode , z ;
float zcoordinate; 
int i = 0 ;

void setup() {
  // initialisation des communication avec l'interface graphique et les dynamixels
  pinMode(electroPin,OUTPUT);
  Serial.begin(115200);
  Dynamixel.begin(1000000,2); 
  delay(100);
  // Vitesses par defaut
  Dynamixel.moveSpeed(dynamixel1,512,cmdvit);
  delay(100);
  Dynamixel.moveSpeed(dynamixel2,512,cmdvit);
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
      zcoordinate = message.substring(message.lastIndexOf(' ')).toFloat();
      z = floor(zcoordinate);
      mode =round( (zcoordinate - z)*10) ; 
//      mode = message.substring(message.lastIndexOf(' ')).toInt();
//      Serial.println(mode);
      // adapter les valeurs des angles au valeurs réelles sur le dynamixel
      translationDesAngles();
}
// Fonction pour commander les servos 
void moveServo(){
  Temperature1 = Dynamixel.readTemperature(dynamixel1); // Request and Print the Temperature       
  Temperature2 = Dynamixel.readTemperature(dynamixel2); // Request and Print the Temperature
  Dynamixel.moveSpeed(dynamixel1,theta1*1023/300,cmdvit);       
  Dynamixel.moveSpeed(dynamixel2,theta2*1023/300,cmdvit);
  Vitesse1 = Dynamixel.readSpeed(dynamixel1);
  Vitesse2 = Dynamixel.readSpeed(dynamixel2);
  // On attend jusqu'à ce que les servos atteignent le point 
  waitForServo();
  // Cette fonction permet de savoir l'état du stylo ou de l'electroaimant (0 ou 1)
  handleMode();
  // Print the variables in the Serial Monitor
  Serial.print(z);
  Serial.print(" ");
  Serial.print(zcoordinate);
  Serial.print(" ");
  Serial.print(mode);
  Serial.print(" ");
  Serial.println(Vitesse2);
  
}

void handleMode(){
   if(mode==0){
      digitalWrite(electroPin,HIGH);
      delay(50);
      digitalWrite(electroPin,LOW);
    }
   if(mode==1){
    digitalWrite(electroPin,HIGH);
    delay(50);}
   if(mode==2){digitalWrite(electroPin,HIGH);delay(5000);}
   if(mode==3){digitalWrite(electroPin,HIGH);}
   if(mode==4){digitalWrite(electroPin,LOW); delay(5000);}
   if(mode==5){digitalWrite(electroPin,LOW);}
}
// fonction pour attendre les servos 
void waitForServo(){
  while(Dynamixel.moving(dynamixel1) == 1 or Dynamixel.moving(dynamixel2) == 1)delay(10);
}
void translationDesAngles(){
  int theta0 = 150 ;
  theta1 = theta1 + theta0 -90 ;
  if( theta1 > 300) theta1 -=300;
  theta2 = theta2 + theta0 -90 ;
  if( theta2 > 300) theta2 -=300;  
}
