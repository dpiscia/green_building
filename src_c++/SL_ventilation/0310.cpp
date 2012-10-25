#include <iostream>
#include <fstream>
#include <vector>
#include <vector_ddp.H>
#include <cassert>
#include <math.h>
#include <cstdlib> 
#include <sstream>
#include <viewFactor.H>
#include <viewFactor.C>
#include <Radiation.H>
#include <Radiation.C>
#include <Convection.H>
#include <Convection.C>
#include <Function.H>
#include <Function.C>
#include <Read.H>




using namespace std;

int main(int argc, char **argv)
{


int time;

double span_height,span_width,cover_height,domain_height,ext_land;
double rho;
double cp;
int span_number;

double1D j,g,T,e,A,qrad,qcond,qconv,alpha,T0,t,T_ins_evo, T_cover;

double deltaT = 60;
T_ins_evo = vector<double> (60,283);
T_cover = vector<double> (60,283);


Read read_prova(text_file);




int pausesd;
cout<<"qua si dferma";



 

j = vector<double> (size,0);
g = vector<double> (size,100);
T = vector<double> (size,280);
e = vector<double> (size,0);
A = vector<double> (size,0);
t = vector<double> (size,0);
alpha = vector<double>(size,5);
qrad = vector<double> (size,0);
qcond = vector<double> (size,0);
qconv = vector<double> (size,0);
T0 = vector<double> (size,280);
  
A = prova.Area_calculation();

double T_inside0 , T_iter_0;
cout<<"A[0] "<<A[0]<<"A[1] "<<A[1]<<"A[2] "<<A[2]<<endl;

double emissivity_soil;
emissivity_soil = 1;

cout<<"tramissione"<<t[0]<<endl;

double soil_heat;

double prova_coef=convective_coef_forced(ext_land,2); 
cout<<"prova_copef "<<prova_coef<<endl;


double prova_coef_nat;
double pause;






T_inside0 = T_air_inside;//T_air_inside-1;
T_air_inside = 300;



T_iter_0 = T_air_inside;
for ( time=0; time<=60; time++){


for (int i=0; i<=4000; i++) {
cout<<"giro"<<T_air_inside<<endl;
cout<<"T_inside0 "<<T_inside0<<endl;

T0=T;

T[0]=T[4];
T[5]=T[3];
Radiation radia(A,F,e,T,j,g,t);
alpha[4]= convective_coef_natural_2(4.5,T_air_inside,T[6]);
alpha[5]= alpha[6]=alpha[4]=2.13;
alpha[6]=1.246*pow(fabs(T[6]-T_air_inside),0.33);
alpha[5]=1.246*pow(fabs(T[5]-T_air_inside),0.33);
alpha[4]=1.246*pow(fabs(T[4]-T_air_inside),0.33);;

alpha[4] = 2.2;
alpha[5] = 1.54;
alpha[6] = 2.76;
alpha[0] = 4.85;
alpha[3] = 3.09;

Convection conve(alpha,T_air,T,T_air_inside);
qrad = radia.qradiation();
qconv = conve.qconvection();
T[6]= ((qcond[6]+alpha[6]*T_air_inside+e[6]*g[6])/(e[6]*kbol*pow(T[6],3)+alpha[6])); //soil conditions


T[4]= (e[0]*g[0]+alpha[0]*T_air+e[4]*g[4]+alpha[4]*T_air_inside -t[0]*j[4]+t[0]*j[0] - t[4]*j[0] +t[4]*j[4])/(e[0]*kbol*pow(T[4],3)+alpha[0]+alpha[4]+e[4]*kbol*pow(T[4],3)); //cover condition

T[3]= (e[5]*g[5]+alpha[5]*T_air_inside+e[3]*g[3]+alpha[3]*T_air -t[5]*j[3]+t[5]*j[5] - t[3]*j[5] +t[3]*j[3])/(e[5]*kbol*pow(T[3],3)+alpha[5]+alpha[3]+e[3]*kbol*pow(T[3],3)); //sidewall condition

T_air_inside = (alpha[5]*T[5]*A[5]+alpha[4]*T[4]*A[4]+alpha[6]*T[6]*A[6]+(rho*cp*Vol*T_inside0/deltaT))/(alpha[5]*A[5]+alpha[4]*A[4]+alpha[6]*A[6]+ (rho*cp*Vol/deltaT));

int pause;
double relax = 0.25;

T[6] = T0[6] + relax*(T[6]-T0[6]);
T[4] = T0[4] + relax*(T[4]-T0[4]);
T[3] = T0[3] + relax*(T[3]-T0[3]);
cout<<"qrad sum ext"<<qrad[0]*A[0]+qrad[1]*A[1]+qrad[2]*A[2]+qrad[3]*A[3]+qrad[7]*A[7]<<endl;
cout<<"qrad sum int"<<qrad[4]*A[4]+qrad[5]*A[5]+qrad[6]*A[6]<<endl;
cout<<"qrad sum 4 "<<qrad[4]*A[4]<<endl;
cout<<"qrad sum 5"<<qrad[5]*A[5]<<endl;
cout<<"qrad sum 6"<<qrad[6]*A[6]<<endl;
cout<<"qconv sum "<<qconv[4]*A[4]+qconv[5]*A[5]+qconv[6]*A[6]<<endl;
cout<<"qconv sum 4 "<<qconv[4]*A[4]<<endl;
cout<<"qconv sum 5"<<qconv[5]*A[5]<<endl;
cout<<"qconv sum 6"<<qconv[6]*A[6]<<endl;
cout<<"(T_air_inside-T_inside0)*(cp*rho*Vol)/(60)"<<(T_air_inside-T_inside0)*(cp*rho*Vol)/(60)<<endl;
cout<<"T_iter_0"<<T_iter_0<<endl;
cout<<"fabs(T_iter_0-T_air_inside)"<<fabs(T_iter_0-T_air_inside)<<endl;
cout<<"(fabs(qconv.."<<fabs(qconv[4]*A[4]+qconv[5]*A[5]+qconv[6]*A[6])-(T_air_inside-T_inside0)*(cp*rho*Vol)/(60)<<endl;
if (fabs(T_iter_0-T_air_inside)<=0.000001 && ((fabs((qconv[4]*A[4]+qconv[5]*A[5]+qconv[6]*A[6])-(T_air_inside-T_inside0)*(cp*rho*Vol)/(60)))<=0.000001))  {
cout<<"iteration "<<i<<endl;

cout<<"T_air_inside "<<T_air_inside<<endl;
cout<<"T_inside0 "<<T_inside0<<endl;
cout<<"T_iter_0 "<<T_iter_0<<endl;
cout<<"energy saving"<<(T_air_inside-T_inside0)*(cp*rho*Vol)/(60)<<endl;
cout<<"converged"<<endl;
T_cover[time] = T[0];
T_ins_evo[time]=T_inside0 = T_air_inside;
cout<<"bingo"<<endl; /*cin>>pause;*/ break;}

T_iter_0 = T_air_inside;


};

int pause;

};
cout<<"time is "<<(time)<<" minutes and internal air temperature is "<<T_ins_evo[time]<<endl;
print_result(T_cover,T_ins_evo,T_ins_evo,T_ins_evo,(time+1));

}

