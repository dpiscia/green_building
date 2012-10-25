#include <iostream>
#include <fstream>
#include <vector>
#include <vector_ddp.H>
#include <cassert>
#include <math.h>
#include <cstdlib> 
#include <sstream>
#include <Radiation.H>
#include <Radiation.C>
#include <Convection.H>
#include <Convection.C>
#include <Function.H>
#include <Function.C>
#include <Read.H>
#include <greenhouse.H>
#include <greenhouse.C>



using namespace std;

int main(int argc, char **argv)
{
char *text_file;
text_file = "/home/dpiscia/workapsce_java/prova/output/green_in";
cout<<"argc"<<argc;
if (argc==2) {cout<<"File Name "<<argv[1]<<endl;
              text_file = argv[1];
             }
if (argc==1) {  cout<<"nothing passes standard input file is green.in"<<endl;}
 

greenhouse prova_green(text_file);
prova_green.solver(300,4000);
/*cout << "humidity ratio"<< humidity_ratio(283,0.8) << endl;
cout << "humidity ratio cover"<< humidity_ratio(274,1) << endl;

cout << "condesation is "<< condensation(274,283,0.8,1.2,800)<<endl;
cout <<"RH is "<<Relative_Humidity(283,humidity_ratio(283,0.8))<< endl;*/
}
