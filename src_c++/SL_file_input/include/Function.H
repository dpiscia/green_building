#ifndef Function_H
#define Function_H

using namespace std;

double convective_coef_forced(double X,double v); 

double convective_coef_natural(double X,double T_wall,double T_fluid); //two plate, X=distance between plate,colder on the upper side

double convective_coef_natural_2(double X,double T_wall,double T_fluid); //heated horizontalplate facing upward

void print_result(vector<double> Temp_solid,vector<double> Temp_fluid,vector<double> Pressure, vector<double> velocity, int size);

void print_result_humidity(vector<double> Temp_solid,vector<double> Temp_fluid,vector<double> Pressure, vector<double> velocity, vector<double> RH, vector<double> condensation, int size);
 
double pressure_sat(double T);

double humidity_ratio(double T, double RH);

double condensation(double Tcover,double Tinside, double RH, double density,double volume);

#endif
