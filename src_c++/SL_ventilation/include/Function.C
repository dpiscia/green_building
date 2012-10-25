#include <Function.H>
#include <iomanip>

using namespace std;



double convective_coef_forced(double X,double v) {
double Pr =0.7;
double rho = 1.2;
double viscosity = 1.8*pow(10,-5);
double Re =(X*rho*v)/viscosity;
cout<<"reynold is "<<Re<<endl;
double Nu;
Nu = 0.037*pow(Re,0.8)*pow(Pr,0.3333);
cout<<"Nusselt is "<<Nu<<endl;
double k=0.024;
double coef;
coef = k*Nu/X;
cout<<"coef "<<coef<<endl;
return coef;
};

//Two horizontal parallel plates, cold plate uppermost Wong(1977) which will account for soil and roof convective


double convective_coef_natural(double X,double T_wall,double T_fluid){
double k=0.024;
double Pr=0.7;
double rho = 1.2;
double viscosity = 1.8*pow(10,-5);
double g = 9.8;
double Gr;
double T_ref = 283;
double beta = 1/T_ref;
double deltaT = fabs(T_wall-T_fluid);
Gr = g*beta*pow(rho,2)*deltaT*pow(X,3)/(pow(viscosity,2));
//cout<<"Gr "<<Gr<<endl;
double  C,n,K;
C = 0.068;
n = 0.3333;
K = pow(Pr,-0.3333);
double Nu = C*pow((Gr*Pr),n)*K;
//cout<<"Nu is "<<Nu<<endl;
double coef = k*Nu/X;
//cout<<"coef "<<coef<<endl;
//two horizontal parallel plates cold plate upper most
return coef;
};
//Heated horizontal plate facing downward Wong(1977) which will account for inner roof convective heat coeﬃcient
double convective_coef_natural_2(double X,double T_wall,double T_fluid){
double k=0.024;
double Pr=0.7;
double rho = 1.2;
double viscosity = 1.8*pow(10,-5);
double g = 9.8;
double Gr;
double T_ref = 283;
double beta = 1/T_ref;
double deltaT = fabs(T_wall-T_fluid);
Gr = g*beta*pow(rho,2)*deltaT*pow(X,3)/(pow(viscosity,2));
//cout<<"Gr "<<Gr<<endl;
double  C,n,K;
C = 0.14;
n = 0.3333;
K = 1;
double Nu = C*pow((Gr*Pr),n)*K;
//cout<<"Nu is "<<Nu<<endl;
double coef = k*Nu/X;
//cout<<"coef "<<coef<<endl;
//two horizontal parallel plates cold plate upper most
return coef;
};

//Vertical plate formula Wong(1977) which computesidewalls convective heat coeﬃcient
double convective_coef_natural_3(double X,double T_wall,double T_fluid){
double k=0.024;
double Pr=0.7;
double rho = 1.2;
double viscosity = 1.8*pow(10,-5);
double g = 9.8;
double Gr;
double T_ref = 283;
double beta = 1/T_ref;
double deltaT = fabs(T_wall-T_fluid);
Gr = g*beta*pow(rho,2)*deltaT*pow(X,3)/(pow(viscosity,2));
//cout<<"Gr "<<Gr<<endl;
double  C,n,K;
C = 0.246;
n = 0.4;
K = pow((pow(Pr,0.16)/(1+0.494*pow(Pr,0.66))),0.4);
double Nu = C*pow((Gr*Pr),n)*K;
//cout<<"Nu is "<<Nu<<endl;
double coef = k*Nu/X;
//cout<<"coef "<<coef<<endl;
//two horizontal parallel plates cold plate upper most
return coef;
};

void print_result(vector<double> Temp_solid,vector<double> Temp_fluid,vector<double> Pressure, vector<double> velocity, int size)

{
int place;
place = size;
/*int iter = 1;
string s;
stringstream out;
out << iter;
s = out.str();*/

ofstream ofs;
ofstream results;
ofstream sim;
sim.open("sim.log", ios::out | ios::binary);
if (ofs.fail()) { cout<<"error ofs.open"<<endl;
                  exit(-1);  }
//myfile.open ("example.bin", ios::out | ios::app | ios::binary); 	
//if ((size-1)==0) ofs.open("Solid_Temperature_distribution.txt");
ofs.open("results_ES.txt", ios::out | ios::binary);
if (ofs.fail()) { cout<<"error ofs.open"<<endl;
                  exit(-1);  }
results.open("results.txt", ios::out | ios::binary);
if (results.fail()) { cout<<"error ofs.open"<<endl;
                  exit(-1);  }
for ( place=0; place<(size-1); place++) {
//cout<<"Temp_solid[place]"<<Temp_fluid[60]<<endl;
if (place==0)
   {
	 ofs<<" Temperature cover||temperature fluid||minute time "<<endl;
    }
else {
	  ofs<<Temp_solid[place]<<"||"<<Temp_fluid[place]<<"||"<<place <<endl;

       if (place==(size-3))
                     {
    	              results<< setprecision (9) <<"Temperature cover="<<-Temp_solid[place]<<endl;
                      results<< setprecision (9) <<"Temperature inside="<<-Temp_fluid[place]<<endl;
                     }
      }
    }
ofs.close();
sim.close();
//echo "Dummy file, needed since GenOpt needs a simulation log file" > sim.log;

//myfile.open ("example.bin", ios::out | ios::app | ios::binary);
//if ((size-1)==0) ofs.open("Solid_Temperature_distribution.txt");

//cout<<"Temp_solid[place]"<<Temp_fluid[60]<<endl;



results.close();


}

double pressure_sat(double T) {
double pressure;
pressure = (exp((77.3450+0.0057*T-7.235/T)))/pow(T,8.2);

return pressure;
};

double humidity_ratio(double T, double RH) {
    double pws = 0;
    double pw = 0;
    const double C8 = -5.8002206*pow(10,3);
    const double C9 = 1.3914993;
    const double C10 = -4.8640239*pow(10,-2);
    const double C11 = 4.1764768*pow(10,-5);
    const double C12 = -1.4452093*pow(10,-8);
    const double C13 = 6.5459673;
    double W = 0;
    int i = 0;
    pws = C8/T + C9 + C10*T + C11*pow(T,2)+C12*pow(T,3) +C13*log(T);
    //cout << exp << endl;
    pw = exp(pws) * RH;
    W = (0.62918 * (pw/(101325-pw)));
         
    return W;



}

double condensation(double Tcover,double Tinside, double RH,double density,double volume) {
     double condensation = 0;
     double hum_ratio_air = humidity_ratio(Tinside,RH);
     double hum_ratio_cover = humidity_ratio(Tcover,1);
     if (hum_ratio_cover < hum_ratio_air) {
       condensation = (hum_ratio_air - hum_ratio_cover)*density*volume;
 

      }

      return condensation;


}

double ventilation(double wind,double degree) {
     double ventilation = 0;
     double sin_angle = sin(degree*3.14/180);
     double BF1 = max(0.0, sin_angle -0.258690844053802);
     double BF2 = max(0.0, 0.258690844053802 - sin_angle);
     double BF3 = BF1 * max(0.0, wind -2);
     double BF4 = max(0.0, wind -2);
     double BF5 = max(0.0, 2 - wind);
     double BF6 = BF4 * max(0.0, sin_angle -0.499770102643102);
     double BF7 = BF4 * max(0.0, 0.499770102643102 - sin_angle);
     double BF8 = max(0.0, 0.865759839492344 - sin_angle);
     double BF9 = BF8 * max(0.0, 2 - wind);
     ventilation = 19.3941877273305 + 15.0399995903575*BF1 -22.5664934534249*BF2
                   -4.50069762381828*BF3 +9.85686151491185*BF4 -14.6458277948187*BF5 +19.1931416709916*BF6 -19.418993497707*BF7    
                   -15.074984018779*BF8 +16.4915503604416*BF9;
      return ventilation/12; //divide by greenhose lenght


} 
/* [1,1] = BF1 = max(0, x2 -0.258690844053802)
 [1,2] = BF2 = max(0, 0.258690844053802 -x2)
 [1,3] = BF3 = BF1 * max(0, x1 -2)
 [1,4] = BF4 = max(0, x1 -2)
 [1,5] = BF5 = max(0, 2 -x1)
 [1,6] = BF6 = BF4 * max(0, x2 -0.499770102643102)
 [1,7] = BF7 = BF4 * max(0, 0.499770102643102 -x2)
 [1,8] = BF8 = max(0, 0.865759839492344 -x2)
 [1,9] = BF9 = BF8 * max(0, 2 -x1)
 [1,10] = y = 19.3941877273305 +15.0399995903575*BF1 -22.5664934534249*BF2 -4.50069762381828*BF3 +9.85686151491185*BF4 -14.6458277948187*BF5 +19.1931416709916*BF6 -19.418993497707*BF7 -15.074984018779*BF8 +16.4915503604416*BF9
}

where x1 is wind speed [m sec-1]
where x2 is sin angle [rad]
*/

double Relative_Humidity(double T,double hum_ratio) {
    double pws = 0;
    double pw = 0;
    double RH = 0;
    const double C8 = -5.8002206*pow(10,3);
    const double C9 = 1.3914993;
    const double C10 = -4.8640239*pow(10,-2);
    const double C11 = 4.1764768*pow(10,-5);
    const double C12 = -1.4452093*pow(10,-8);
    const double C13 = 6.5459673;
    double W = 0;
    int i = 0;
    pws = C8/T + C9 + C10*T + C11*pow(T,2)+C12*pow(T,3) +C13*log(T);
    pws = exp(pws);
    pw = (101325*hum_ratio)/(0.629+hum_ratio);
    RH = pw/pws;
    return RH;


}


void print_result_humidity(vector<double> Temp_solid,vector<double> Temp_fluid,vector<double> Pressure, vector<double> velocity, vector<double> RH,vector<double> condensation, int size)

{
int place;
place = size;
/*int iter = 1;
string s;
stringstream out;
out << iter;
s = out.str();*/

ofstream ofs;
ofstream results;
ofstream sim;
sim.open("sim.log", ios::out | ios::binary);
if (ofs.fail()) { cout<<"error ofs.open"<<endl;
                  exit(-1);  }
//myfile.open ("example.bin", ios::out | ios::app | ios::binary); 	
//if ((size-1)==0) ofs.open("Solid_Temperature_distribution.txt");
ofs.open("results_ES.txt", ios::out | ios::binary);
if (ofs.fail()) { cout<<"error ofs.open"<<endl;
                  exit(-1);  }
results.open("results.txt", ios::out | ios::binary);
if (results.fail()) { cout<<"error ofs.open"<<endl;
                  exit(-1);  }
for ( place=0; place<(size-1); place++) {
//cout<<"Temp_solid[place]"<<Temp_fluid[60]<<endl;
if (place==0)
   {
	 ofs<<" Temperature cover,temperature fluid,Relative humidity,condensation,hum_ratio,minute time "<<endl;
    }
else {
	  ofs<<Temp_solid[place]<<","<<Temp_fluid[place]<<","<<RH[place]<<","<<humidity_ratio(Temp_fluid[place],RH[place])<<","<<condensation[place]<<","<<place <<endl;

       if (place==(size-3))
                     {
    	              results<< setprecision (9) <<"Temperature cover="<<-Temp_solid[place]<<endl;
                      results<< setprecision (9) <<"Temperature inside="<<-Temp_fluid[place]<<endl;
                      results<< setprecision (9) <<"RH inside="<<-RH[place]<<endl;
                      results<< setprecision (9) <<"cond_rate="<<-condensation[place]<<endl;
                     }
      }
    }
ofs.close();
sim.close();
//echo "Dummy file, needed since GenOpt needs a simulation log file" > sim.log;

//myfile.open ("example.bin", ios::out | ios::app | ios::binary);
//if ((size-1)==0) ofs.open("Solid_Temperature_distribution.txt");

//cout<<"Temp_solid[place]"<<Temp_fluid[60]<<endl;



results.close();


}

