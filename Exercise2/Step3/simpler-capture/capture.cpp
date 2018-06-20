/*
 *
 *  Example by Sam Siewert 
 *
 */
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <sys/time.h>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

#define NUMBER 200

int main( int argc, char** argv )
{
    cvNamedWindow("Capture Example", CV_WINDOW_AUTOSIZE);
    CvCapture* capture = cvCreateCameraCapture(0);
    IplImage* frame;

   	//Create an array of timevalues 
    struct timeval tim[NUMBER];
    //get the time of day at beggining of the code
    gettimeofday(&tim[0],NULL);    
    //start incrementer at 1 because we have already used 0
    int i=1;

    while(i<NUMBER)
    {
    	//obtain the frame
        frame=cvQueryFrame(capture);
     
        if(!frame) break;

        //get the time of day with the frame
		gettimeofday(&tim[i],NULL);
		i++;	

        cvShowImage("Capture Example", frame);

        char c = cvWaitKey(33);
        if( c == 27 ) break;
    }
    //bring incrementer back to the start
    i=0;
    //create an array of diff numbers, will be used to calculate difference in times
    int diff[NUMBER];
    //creating a temporary variable to get time differnece
    int temp;
    i++;
    //first diff is 0
    diff[0]=0;
    //create a total sec incrementer to get the total time elapsed
    int total_sec;

    while(i<NUMBER)
    {
    	//obtain the current secs in usecs by multiplying by value
    	temp= (tim[i].tv_sec - tim[i-1].tv_sec)*1000000;
    	//set diff time as seconds plus usecs
    	diff[i]=temp+(tim[i].tv_usec - tim[i-1].tv_usec);
		//add difference to total time
		total_sec += diff[i];
		i++;
    }
    //get the average frame rate by dividing total seconds by increments
    int avg_framerate = total_sec/i;
    printf("total=%i, i=%i, avg_framerate=%i\n", total_sec, i, avg_framerate);
    //set worst case as 0, so that it will start out as lowest value
    int worst_case = 0;
    //show the first
    printf("Frame: %d ,Jitter of Frame=%i\n",0, abs(avg_framerate- diff[0]));
    i=1;
    while(i<NUMBER)
    {
    	//print frame count, the difference from the average (jitter)
    	printf("Frame: %d ,Jitter of Frame=%i\n",i, abs(avg_framerate- diff[i]));
    	//check to see if the jitter is the worst case or not
    	if(abs((avg_framerate-diff[i]))> worst_case)
    	{
    		//make it the worst case if jitter is highest value
    		worst_case=abs(avg_framerate-diff[i]);
    	}
    	i++;
    }
    //print the worst case and the average framerate
    printf("Worst case=%i , Average Framerate = %i\n", worst_case, avg_framerate);


    cvReleaseCapture(&capture);
    cvDestroyWindow("Capture Example");
    
};
