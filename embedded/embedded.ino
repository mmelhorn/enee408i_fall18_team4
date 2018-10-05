/* Embedded systems
 
 */

#include "arduinoPins.h"
#include "motor_control.c"

int ping_right_dist;
int ping_left_dist;
int ping_center_dist;
double BOT_WIDTH = 33.02; //cm

//motor_values contain the values to be sent from the arduino to the motor controller
int motor_values[6];

void setMotorValues();
void getPing();

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  pinMode(IN_A_R, OUTPUT);
  pinMode(IN_B_R, OUTPUT);
  pinMode(IN_A_L, OUTPUT);
  pinMode(IN_B_L, OUTPUT);
  pinMode(PWM_R, OUTPUT);
  pinMode(PWM_L, OUTPUT);

  motor_values[0] = 0;
  motor_values[1] = 0;
  motor_values[2] = 0;
  motor_values[3] = 0;
  motor_values[4] = 0;
  motor_values[5] = 0;
}

unsigned char in = 0;
int in_lin, in_ang;

void loop() { 

  /* TEST CODE
   Serial.print(ping_left_dist);
   Serial.print("in to left, ");
   Serial.print(ping_right_dist);
   Serial.print("in to right");
   Serial.print(ping_center_dist);
   Serial.print("in to center, ");
   Serial.println();
   */

  // loop until a command is recieved
  while(Serial.available() == 0){ 
    //Serial.println("waiting for command");
    //delay(1000);
    }

    // when command is recieved, get integer command
    in = Serial.parseInt();

  getPing();

  if(in == 0){
    //stop bot movement
    move(0,0,.5,motor_values);
    Serial.write(250);            //write 250 if successful move
  }
  else if (in > 0 && in < 110){
    //calc values
    in_lin = in/10;
    in_ang = in % 10;
    //make sure that angle value is correct
    if(in_ang == 0)
      in_ang = 1;
    //set movement
    move((double)in_lin/10, (double)(in_ang-5), .5, motor_values);
    Serial.write(250);            //write 250 if successful move
  }
  /*else if (in == 200){
    Serial.write(ping_left_dist);
  }
  else if (in == 201){
    Serial.write(ping_center_dist);
  }
  else if (in == 202){
    Serial.write(ping_right_dist);
  }*/
  else {
    Serial.write(251);          //write 255 if command not recognized
  }

  setMotorValues();
  delay(10);
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

