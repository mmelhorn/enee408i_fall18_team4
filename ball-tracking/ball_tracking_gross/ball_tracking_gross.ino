//#include "robotPins.h"
//#include "motorControls.h"

const byte inA1=12;
const byte inB1=11;

//Pins for right motor
const byte inA2=8;
const byte inB2=7;

const byte PWM1=5;  //PWM pin for left motor
const byte PWM2=3;  //PWM pin for right motor

const byte left_ping=8; //Pin for left ping sensor
const byte right_ping=13;  //Pin for right ping sensor
const byte front_ping=12; //Pin for left ping sensor

byte incomingByte=3;
byte buf=3;

void setup() {
  pinMode(inA1, INPUT);
  pinMode(inB2, INPUT);
  pinMode(inA2, INPUT);
  pinMode(inB2, INPUT);
  pinMode(PWM1, INPUT);
  pinMode(PWM2, INPUT);
  pinMode(left_ping, OUTPUT);
  pinMode(right_ping, OUTPUT);
  pinMode(front_ping, OUTPUT);
  Serial.begin(9600);
}

void loop() {
    incomingByte = Serial.read();
    if(buf != incomingByte && incomingByte != -1){
      buf = incomingByte;
      if(incomingByte == 0){
        turn_left(45);
      }
      else if(incomingByte == 1){
        forward(40, 37);
      }
      else if(incomingByte == 2){
        turn_right(45);
      }
      else if(incomingByte == 3){
        wheel_stop();
      }
    }
}

void left_wheel_forward(int speed){  //Move left wheel forward
  digitalWrite(inA1, 1);
  digitalWrite(inB1, 0);
  analogWrite(PWM1, speed);
}

void left_wheel_stop(){ //Stop left wheel
  digitalWrite(inA1, 0);
  digitalWrite(inB1, 0);
  analogWrite(PWM1, 0);
}

void right_wheel_forward(int speed){  //Move right wheel forward
  digitalWrite(inA2, 0);
  digitalWrite(inB2, 1);
  analogWrite(PWM2, speed);
}

void right_wheel_stop(){  //Stop right wheel
  digitalWrite(inA2, 0);
  digitalWrite(inB2, 0);
  analogWrite(PWM2, 0);
}

void right_wheel_backward(int speed){ //Move right wheel backwards
  digitalWrite(inA2, 1);
  digitalWrite(inB2, 0);
  analogWrite(PWM2, speed);
}

void left_wheel_backward(int speed){  //Move left wheel backwards
  digitalWrite(inA1, 0);
  digitalWrite(inB1, 1);
  analogWrite(PWM1, speed);
}

void forward(int leftSpeed, int rightSpeed){  //Move robot forward
  left_wheel_forward(leftSpeed);
  right_wheel_forward(rightSpeed);
}

void backward(int leftSpeed, int rightSpeed){ //Move robot backwards
  left_wheel_backward(leftSpeed);
  right_wheel_backward(rightSpeed);
}

void wheel_stop(){  //Stop robot
  left_wheel_stop();
  right_wheel_stop(); 
}

void turn_right(int speed){ //Robot pivot right
  left_wheel_forward(speed);
  right_wheel_backward(speed);
}

void turn_left(int speed){  //Robot pivot left
  right_wheel_forward(speed);
  left_wheel_backward(speed);
}

