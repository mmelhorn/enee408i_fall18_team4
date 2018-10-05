/* Motor Controller */


#include <stdlib.h>


#define MAX_VELOCITY 200		// reduces maximum velocity from 255 to 200

int convert_velocity(double in);
void direct_motor_control(int vel_l, int vel_r, int[]);
void move(double, double, double, int[]);


/* 
	IN: lin_vel_in: double {0 to 1}: 1 is full power, 0 is no linear power
	IN: ang_vel_in: double {-2 to 2}: 0 is no turn, -2 full power to right, 2 full power to left
	IN: balance: double {0 to 1}: .5 is balanced, 1 right wheel powers turn, 0 left wheel powers turn
	OUT: array of values for motor
	int[] out = {pwm_r, r_in_a, r_in_b, pwm_l, l_in_a, l_in_b};
	
*/
void move(double lin_vel_in, double ang_vel_in, double balance, int out[])
{
	int vel_R, vel_L, vel_lin, vel_ang;
	
	// Convert velocities from 0-1 to 0-255
	vel_lin = convert_velocity(lin_vel_in);
	vel_ang = convert_velocity(ang_vel_in);
	
	// Calculate velocities for each wheel
	vel_R = vel_lin + (vel_ang*balance);
	vel_L = vel_lin - (vel_ang*(1-balance));
	
	//Limit excessive velocity
	if(vel_R>255)
		vel_R = 255;
	else if (vel_L>255)
		vel_L = 255;
		
	direct_motor_control(vel_L, vel_R, out);
}

/* 
	Accepts velocities for each motor and outputs pin values for motors
	NO BRAKE COMMAND HAS BEEN IMPLEMENTED
*/
void direct_motor_control(int vel_L, int vel_R, int out[])
{
	int R_in_a, R_in_b, L_in_a, L_in_b;
	int R_pwm, L_pwm;
	
	/* 
	Determine values of in_x variables. 
	Right wheel moves forward when in_a = LOW, in_b = HIGH
	Left wheel moves forward when in_a = HIGH, in_b = LOW
	*/
	
	if(vel_L > 0){				//Left forward
		L_in_a = 1;
		L_in_b = 0;
		L_pwm = vel_L;
	} else if(vel_L < 0){		//Left backward
		L_in_a = 0;
		L_in_b = 1;
		L_pwm = abs(vel_L);
	}
	
	if(vel_R > 0){				//Right forward
		R_in_a = 0;
		R_in_b = 1;
		R_pwm = vel_R;
	} else if(vel_R < 0){		//Right backward
		R_in_a = 1;
		R_in_b = 0;
		R_pwm = abs(vel_R);
	}
	
	out[0] = R_pwm;
	out[1] = R_in_a;
	out[2] = R_in_b;
	out[3] = L_pwm;
	out[4] = L_in_a;
	out[5] = L_in_b;
}

//Convert velocity from range of {0-1} to {0-MAX_VELOCITY}
int convert_velocity(double in)
{ 
  return in*MAX_VELOCITY;
}