#ifndef Radiation_H
#define Radiation_H

using namespace std;

class Radiation {
public:


 double1D j,g,qrad;
Radiation(double1D Area, double2D Factor, double1D Emissivity,double1D &Temp,double1D &j,double1D &g, double1D &t) {
//j = vector<double> (5,300);
//g = vector<double> (5,300);
int size = 8;
qrad= vector<double> (size,0);
double kbol = 5.67*pow(10,-8);
//for (int i = 0; i<=100; i++) {
//radiation 
//Temp[0]=Temp[3];

j[0] = Emissivity[0]*kbol*pow(Temp[0],4) + (1-Emissivity[0]-t[0])*(g[0]) + t[0]*g[4] /*+t[0]*Factor[0][0]*j[0]*/ ; 
j[1] = Emissivity[1]*kbol*pow(Temp[1],4) + (1-Emissivity[1])*(g[1]); 
j[2] = Emissivity[2]*kbol*pow(Temp[2],4) + (1-Emissivity[2])*(g[2]); 
j[3] = Emissivity[3]*kbol*pow(Temp[3],4) + (1-Emissivity[3]- t[3])*(g[3]) + t[3]*g[5] /*+t[3]*Factor[3][3]*j[3]*/; 
j[4] = Emissivity[4]*kbol*pow(Temp[4],4) + (1-Emissivity[4]-t[4])*(g[4])  + t[4]*g[0] /*+t[4]*Factor[4][4]*j[4]*/; 
j[5] = Emissivity[5]*kbol*pow(Temp[5],4) + (1-Emissivity[5]-t[5])*(g[5])  + t[5]*g[3] /*+t[5]*Factor[3][3]*j[3]*/;
j[6] = Emissivity[6]*kbol*pow(Temp[6],4) + (1-Emissivity[6])*(g[6]);
j[7] = Emissivity[7]*kbol*pow(Temp[7],4) + (1-Emissivity[7])*(g[7]);
//cout<<"j[2] "<<j[2]<<endl;

g[0] = Factor[0][1]*j[1] + Factor[0][2]*j[2] + Factor[0][0]*j[0] + Factor[0][3]*j[3] + Factor[0][7]*j[7];
g[1] = Factor[1][1]*j[1] + Factor[1][2]*j[2] + Factor[1][0]*j[0] + Factor[1][3]*j[3] + Factor[1][7]*j[7];
g[2] = Factor[2][1]*j[1] + Factor[2][2]*j[2] + Factor[2][0]*j[0] + Factor[2][3]*j[3] + Factor[2][7]*j[7];
g[3] = Factor[3][1]*j[1] + Factor[3][2]*j[2] + Factor[3][0]*j[0] + Factor[3][3]*j[3] + Factor[3][7]*j[7];
g[7] = Factor[7][1]*j[1] + Factor[7][2]*j[2] + Factor[7][0]*j[0] + Factor[7][3]*j[3] + Factor[7][7]*j[7];

g[4] = Factor[4][4]*j[4] + Factor[4][5]*j[5] +  Factor[4][6]*j[6] ;
g[5] = Factor[5][4]*j[4] + Factor[5][5]*j[5] +  Factor[5][6]*j[6] ;
g[6] = Factor[6][4]*j[4] + Factor[6][5]*j[5] +  Factor[6][6]*j[6] ;

qrad[0]=j[0]-g[0];
qrad[1]=j[1]-g[1];
qrad[2]=j[2]-g[2];
qrad[3]=j[3]-g[3];
qrad[7]=j[7]-g[7];
cout<<"coverouter emitted "<<j[0]<<" received "<<g[0]<<endl;
cout<<"soil emitted "<<j[6]<<" received "<<g[6]<<endl;
cout<<"cover inner g[4] "<<j[4]<< "side inner g[5] "<<j[5]<<endl;
cout<<"coverinner emitted "<<j[4]<<" received "<<g[4]<<endl;
qrad[4]=j[4]-g[4];
qrad[5]=j[5]-g[5];
qrad[6]=j[6]-g[6];
/*cout<<"qrad0 "<<qrad[0]<<endl;
cout<<"qrad1 "<<qrad[1]<<endl;
cout<<"qrad2 "<<qrad[2]<<endl;
cout<<"qrad3 "<<qrad[3]<<endl;
cout<<"qrad4 "<<qrad[4]<<endl;
cout<<"qrad5 "<<qrad[5]<<endl;
cout<<"qrad6 "<<qrad[6]<<endl;*/






  

}
~Radiation(){};
vector<double> qradiation();
};


#endif
