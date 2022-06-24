#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "IMU.c"

// #define magXmax 2145
// #define magYmax 847
// #define magZmax 913
// #define magXmin -999
// #define magYmin -1829
// #define magZmin -4408

int file;

int main(int argc, char *argv[]) {
	int magRaw[3];
	int scaledMag[3];

	detectIMU();
	enableIMU();

	while(1) {
		readMAG(magRaw);

		// magRaw[0] -= (magXmin + magXmax) /2;
		// magRaw[1] -= (magYmin + magYmax) /2;
		// magRaw[2] -= (magZmin + magZmax) /2;

		printf("magRaw X %i    \tmagRaw Y %i \tMagRaw Z %i \n", magRaw[0],magRaw[1],magRaw[2]);

		//Compute heading
		float heading = 180 * atan2(magRaw[1],magRaw[0])/M_PI;
		float declination = 0.1353;
		heading += declination * 180/M_PI;
		//Convert heading to 0 - 360
		if (heading < 0) heading += 360;
		heading = 90 - heading;

		printf("heading %7.3f \t ", heading);

		usleep(25000);
	}
}