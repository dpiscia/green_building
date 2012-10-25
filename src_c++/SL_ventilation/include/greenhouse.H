#ifndef greenhouse_H
#define greenhouse_H

using namespace std;

class greenhouse{
public:
    Read geo;
	greenhouse(string file_name);
	void solver(int timelenght, int iteration_for_timestep);
        
private : 
	int size;
	const double kbol;
	const int deltaT;
	double Vol,prova_coef_nat,prova_coef, T_inside0 , T_iter_0,relax,T_air_inside,Transpiration,RH_initial;
	double2D F;
	double1D j,g,T,e,A,qrad,qcond,qconv,alpha,T0,t,T_ins_evo, T_cover,RH,cond_rate;

	
};

#endif
