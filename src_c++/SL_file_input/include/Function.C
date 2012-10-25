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

