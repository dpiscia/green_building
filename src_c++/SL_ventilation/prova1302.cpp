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
text_file = "./green_in";
cout<<"argc"<<argc;
if (argc==2) {cout<<"File Name "<<argv[1]<<endl;
              text_file = argv[1];
             }
if (argc==1) {  cout<<"nothing passes standard input file is green.in"<<endl;}
 
//cout<<ventilation(3,30)<<endl;
greenhouse prova_green(text_file);
prova_green.solver(420,4000);

}
