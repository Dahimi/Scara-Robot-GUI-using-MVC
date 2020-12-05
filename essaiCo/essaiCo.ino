#include <DynamixelSerial2.h>
#define electroPin 10
int isMoving ; 
int Temperature2,Vitesse2,Temperature1,Vitesse1; 
int dynamixel1 = 1 , dynamixel2 = 2; 
String message = "";
char readbuffer[16] ;
float theta1, theta2;
int cmdvit=300;
int mode ; 
int i = 0 ;
 
void setup() {
  pinMode(electroPin,OUTPUT);
  Serial.begin(115200);
  Dynamixel.begin(1000000,2); 
  delay(100);
  Dynamixel.moveSpeed(dynamixel1,512,cmdvit);
  delay(100);
  Dynamixel.moveSpeed(dynamixel2,512,cmdvit);
    delay(100);
  Serial.println("communication is set ") ; 
}
void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0  ) {      
      handleComingData();
      moveServo();
      
  }    
  
}
void handleComingData(){
  int readCharacter = Serial.readBytesUntil('\n', readbuffer, 16); 
      message = ""; 
      for(int i = 0 ; i< readCharacter; i++){
        message += readbuffer[i];
      }
      theta1 = message.substring(0,message.indexOf(' ')).toFloat();
      
      theta2 = message.substring(message.indexOf(' '),message.lastIndexOf(' ')).toFloat(); 
      mode = message.substring(message.lastIndexOf(' ')).toInt();
}
void moveServo(){
  Temperature1 = Dynamixel.readTemperature(dynamixel1); // Request and Print the Temperature       
  Temperature2 = Dynamixel.readTemperature(dynamixel2); // Request and Print the Temperature
  Dynamixel.moveSpeed(dynamixel1,theta1*1023/300,cmdvit);       
  Dynamixel.moveSpeed(dynamixel2,theta2*1023/300,cmdvit);
  Vitesse1 = Dynamixel.readSpeed(dynamixel1);
  Vitesse2 = Dynamixel.readSpeed(dynamixel2);
  waitForServo();
  handleMode();
  // Print the variables in the Serial Monitor
  Serial.print(Temperature1);
  Serial.print(" ");
  Serial.print(Temperature2);
  Serial.print(" ");
  Serial.print(Vitesse1);
  Serial.print(" ");
  Serial.print(Vitesse2);
  Serial.print("mode");
  Serial.println(mode);
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
void waitForServo(){
  while(Dynamixel.moving(dynamixel1) == 1 or Dynamixel.moving(dynamixel2) == 1)delay(10);
}
