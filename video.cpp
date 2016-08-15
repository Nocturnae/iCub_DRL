#include <stdio.h>
#include <yarp/os/all.h>
#include <yarp/sig/all.h>

using namespace yarp::os;
using namespace yarp::sig;

int main() {
	Network yarp;
	BufferedPort<ImageOf<PixelRgp> > imagePort;
	imagePort.open("/tutorial/image/in");
	while (1) {
		ImageOf<PixelRgp> *image = imagePort.read();
		if (image != NULL) {
			printf("We got an image of size %dx%d\n", image->width(), image->height());
		}
	}
	return 0;
}