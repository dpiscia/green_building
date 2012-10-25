#ifndef Convection_H
#define Convection_H

using namespace std;

class Convection {
public:
double1D qconv;
Convection(double1D alpha,double T_air,double1D Temp,double T_air_inside){

int size = 9;
qconv = vector<double> (size,300);
qconv[1]=0;
qconv[7]=0;
qconv[0]= alpha[0]*(Temp[0]-T_air);
qconv[2]= alpha[2]*(Temp[2]-T_air);
qconv[3]= alpha[3]*(Temp[3]-T_air);
qconv[5]= alpha[5]*(Temp[5]-T_air_inside);
qconv[4]= alpha[4]*(Temp[4]-T_air_inside);
qconv[6]= alpha[6]*(Temp[6]-T_air_inside);



};
~Convection(){};
vector<double> qconvection();
};


#endif
