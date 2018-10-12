/*
  Embedded systems
*/

#include "arduinoPins.h"
#include "motor_control.c"
#include <Wire.h>

int ping_right_dist;
int ping_left_dist;
int ping_center_dist;
double BOT_WIDTH = 33.02; //cm

//motor_values contain the values to be sent from the arduino to the motor controller
int motor_values[] = {0,0,0,0,0,0};

unsigned char in = 0;

int in_lin, in_ang;
unsigned long time;
int i;
unsigned char out[] = {0,0};  //out[0] is ready flag (1 == ready), out[1] is data


void setMotorValues();
void getPing();

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  //initialize values for the motor control pins
  pinMode(IN_A_R, OUTPUT);
  pinMode(IN_B_R, OUTPUT);
  pinMode(IN_A_L, OUTPUT);
  pinMode(IN_B_L, OUTPUT);
  pinMode(PWM_R, OUTPUT);
  pinMode(PWM_L, OUTPUT);
  Wire.begin(42);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  time = millis();
  i=0;
}


void loop() { 

  // loop until a command is recieved
  while(Serial.available() == 0){ 
    //Serial.println("waiting for command");        //TEST CODE
    //delay(1000);
    }

    // when command is recieved, fetch command code
    in = Serial.parseInt();
    
  
  //Internal latency Test
  //About 6-7ms per command
  /*
  in = 200;
  if(i < 10){
    i++;
  }else{
    time = millis() - time;
    Serial.println(time);
    time = millis();
    i=0;
  }
  */
  
  getPing();
  
  //apply motor values
  setMotorValues();
}

void receiveEvent(int howMany){
 //Get input
 unsigned char in;
  while(Wire.available()){
   in = Wire.read();
   Serial.println(in);
   
 }
 Serial.println(in);
 
 getPing();
  
  /*
    Interpret Command Codes
    If motor control is requested, execute motor control, and write value of 250 to the Jetson to indicate that the action is complete.
    If ping value is requested, write ping value.
    If sent command is invalid, write value of 255
  */
 //set bot movement to zero
  if(in == 0){
    move(0,0,.5,motor_values);
    out[1] = 250;            //write 250 if successful move
    out[0] = 1;
  }
  //set bot movement to a given linear and angular velocity
  else if (in > 0 && in < 110){
    //calc values
    in_lin = in/10;
    in_ang = in % 10;
    //make sure that angle value is correct
    if(in_ang == 0)
      in_ang = 1;
    //set movement
    move((float)in_lin/10, (float)(in_ang-5)/-5, .5, motor_values);
    out[1] = 250;            //write 250 if successful move
    out[0] = 1;
  }
  else if (in == 200){
    out[1] = ping_left_dist;
    out[0] = 1;
  }
  else if (in == 201){
    out[1] = ping_center_dist;
    out[0] = 1;
  }
  else if (in == 202){
    out[1] = ping_right_dist;
    out[0] = 1;
  }
  //Send error code
  else {
    out[1] = 255;
    out[0] = 1;
  }
  Serial.println(out[0]);
  Serial.println(out[1]);
  
  //apply motor values
  setMotorValues();
 
}

void requestEvent(){
  if(out[0] == 1){
    Wire.write(byte(out[1]));
    out[0] = 0;
  }
}

void setMotorValues()
{
  analogWrite(PWM_R, motor_values[0]);
  digitalWrite(IN_A_R, motor_values[1]);
  digitalWrite(IN_B_R, motor_values[2]);
  analogWrite(PWM_L, motor_values[3]);
  digitalWrite(IN_A_L, motor_values[4]);
  digitalWrite(IN_B_L, motor_values[5]);
}


void getPing(){
  long durationL, durationR, durationC, inchesL, inchesR, inchesC;

  // sending left side pulse
  pinMode(leftPing, OUTPUT);
  digitalWrite(leftPing, LOW);
  delayMicroseconds(2);
  digitalWrite(leftPing, HIGH);
  delayMicroseconds(5);
  digitalWrite(leftPing, LOW);

  // left pulse receive
  pinMode(leftPing, INPUT);
  durationL = pulseIn(leftPing, HIGH);

  // sending right side pulse
  pinMode(rightPing, OUTPUT);
  digitalWrite(rightPing, LOW);
  delayMicroseconds(2);
  digitalWrite(rightPing, HIGH);
  delayMicroseconds(5);
  digitalWrite(rightPing, LOW);

  // right pulse receive
  pinMode(rightPing, INPUT);
  durationR = pulseIn(rightPing, HIGH);

  // sending center side pulse
  pinMode(centerPing, OUTPUT);
  digitalWrite(centerPing, LOW);
  delayMicroseconds(2);
  digitalWrite(centerPing, HIGH);
  delayMicroseconds(5);
  digitalWrite(centerPing, LOW);

  // center pulse receive
  pinMode(centerPing, INPUT);
  durationC = pulseIn(centerPing, HIGH);

  //left distance
  inchesL = microsecondsToInches(durationL);

  //right distance
  inchesR = microsecondsToInches(durationR);

  //center distance
  inchesC = microsecondsToInches(durationC);

  ping_right_dist = inchesR;
  ping_left_dist = inchesL;
  ping_center_dist = inchesC;

}


long microsecondsToInches(long microseconds) {
  // According to Parallax's datasheet for the PING))), there are 73.746
  // microseconds per inch (i.e. sound travels at 1130 feet per second).
  // This gives the distance travelled by the ping, outbound and return,
  // so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}

