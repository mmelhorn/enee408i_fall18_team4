/*
  Embedded systems
*/

#include "arduinoPins.h"
#include "motor_control.c"

int ping_right_dist;
int ping_left_dist;
int ping_center_dist;
double BOT_WIDTH = 33.02; //cm
const int SAFETY_RADIUS = 1;

//motor_values contain the values to be sent from the arduino to the motor controller
int motor_values[] = {0,0,0,0,0,0};

unsigned char in = 0;

int magnitude_value, direction_value;
unsigned long time;
int i;


void setMotorValues();
void getPing();
void stop();

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
  while(Serial.available() > 0){
    in = Serial.parseInt();
  }

  /*
    Interpret Command Codes
    0-9 move forward
    10-19 move left
    20-29 move right
  */
  
  //set bot movement to zero
  /*if(in == 0){
    move(0,0,.5,motor_values);
  }
  //set bot movement to a given linear and angular velocity
  else if (in > 0 && in <30){
    //get angle and magnitude
    magnitude_value = in % 10;
    direction_value = in/10;
    //set movement
    switch(direction_value){
      case 0 :
        move((float)magnitude_value*(10/9)/10, 0, .5, motor_values);
        break;
      case 1 :
        move(0, (float)magnitude_value*(10/9)/10, .5, motor_values);
        break;
      case 2 :
        move(0, (-1)*(float)magnitude_value*(10/9)/10, .5, motor_values);
        break;
        
    }*/
    
    switch(in){
       case 0:
         move(0, 0, .5, motor_values);
         break;
       case 1:
         move(.2, 0, .5, motor_values);
         break;
       case 2:
         move(.5, 0, .5, motor_values);
         break;
       case 3:
         move(1, 0, .5, motor_values);
         break;
       case 11:
         move(0, .2, .5, motor_values);
         break;
       case 12:
         move(0, .5, .5, motor_values);
         break;
       case 13:
         move(0, 1, .5, motor_values);
         break;
       case 21:
         move(0, -.2, .5, motor_values);
         break;
       case 22:
         move(0, -.5, .5, motor_values);
         break;
       case 23:
         move(0, -1, .5, motor_values);
         break;
    }
    
  }
  
  //apply motor values
  setMotorValues();
}

void safetyCheck(void){
  if(ping_left_dist < SAFETY_RADIUS  || ping_center_dist < SAFETY_RADIUS  || ping_right_dist < SAFETY_RADIUS){
    move(0,0,.5,motor_values);
    setMotorValues();
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
  //long durationL, durationR, durationC, inchesL, inchesR, inchesC;

  // sending left side pulsevoid getPing(){
  long durationL, durationR, durationC, inchesL, inchesR, inchesC;

  // sending left side pulse
  pinMode(leftPing, OUTPUT);
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

