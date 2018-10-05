/* Motor Controller */


#include <stdlib.h>


#define MAX_VELOCITY 200		// reduces maximum velocity from 255 to 200

void direct_motor_control(int vel_l, int vel_r, int[]);
void move(float, float, float, int[]);


/* 
	IN: lin_vel_in: double {0 to 1}: 1 is full power, 0 is no linear power
	IN: ang_vel_in: double {-2 to 2}: 0 is no turn, -2 full power to right, 2 full power to left
	IN: balance: double {0 to 1}: .5 is balanced, 1 right wheel powers turn, 0 left wheel powers turn
	OUT: array of values for motor
	int[] out = {pwm_r, r_in_a, r_in_b, pwm_l, l_in_a, l_in_b};
	
*/
void move(float lin_vel_in, float ang_vel_in, float balance, int out[])
{
	int vel_R, vel_L, vel_lin, vel_ang;
	
	// Convert velocities from 0-1 to 0-MAX_VELOCITY
	vel_lin = lin_vel_in * MAX_VELOCITY;
	vel_ang = ang_vel_in * MAX_VELOCITY;
	
	// Calculate velocities for each wheel
	vel_R = vel_lin + (vel_ang*balance);
	vel_L = vel_lin - (vel_ang*(1-balance));
	
	//Limit excessive velocity
	if(vel_R>MAX_VELOCITY)
		vel_R = MAX_VELOCITY;
	else if (vel_L>MAX_VELOCITY)
		vel_L = MAX_VELOCITY;
		
	direct_motor_control(vel_L, vel_R, out);
}

/* 
	Accepts velocities for each motor and outputs pin values for motors
	NO BRAKE COMMAND HAS BEEN IMPLEMENTED
*/
void direct_motor_control(int vel_L, int vel_R, int out[])
{
	/* 
		Determine values of in_x variables. 
		Right wheel moves forward when in_a = LOW, in_b = HIGH
		Left wheel moves forward when in_a = HIGH, in_b = LOW
	*/
	
	if(vel_L > 0){				//LEFT WHEEL FORWARD
		out[4] = 1;				//L_in_a
		out[5] = 0;				//L_in_b
		out[3] = vel_L;			//Left pwm
		
	} else if(vel_L < 0){		//LEFT WHEEL BACKWARD
		out[4] = 0;				//L_in_a
		out[5] = 1;				//L_in_b
		out[3] = abs(vel_L);	//Left pwm	
	}
	
	if(vel_R > 0){				//RIGHT WHEEL FORWARD
		out[1] = 0;				//R_in_a
		out[2] = 1;				//R_in_b
		out[0] = vel_R;			//Right PWM
		
	} else if(vel_R < 0){		//RIGHT WHEEL BACKWARD
		out[1] = 1;				//R_in_a
		out[2] = 0;				//R_in_b
		out[0] = abs(vel_R);	//Right PWM
	}
}
