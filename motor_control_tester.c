//motor control tester
#include <stdio.h>
//#include "motor_control.c"

int main()
{
	int in[] = {0,0,0,0,0,0};
	move(0,0,.5,in);
	printf("%d\n",in[0]);
	printf("%d\n",in[3]);
	return 0;
}
