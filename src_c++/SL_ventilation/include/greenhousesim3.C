#include <greenhouse.H>
#include <Read.H>
#include <viewFactor.H>
#include <viewFactor.C>
#include <vector>
#include <vector_ddp.H>
using namespace std;

greenhouse::greenhouse(string file_name):
		geo(file_name),
		size(13),
		kbol(5.67*pow(10,-8)), 
		Vol(geo.span_number*(geo.span_width*geo.span_height+geo.cover_height*geo.span_width/2)),
		F(vector<vector <double> >(size, vector<double> (size,0))),
		j(vector<double> (size,0)),
		g(vector<double> (size,100)),
		T(vector<double> (size,280)),
		e(vector<double> (size,0)),
		A(vector<double> (size,0)),
		t(vector<double> (size,0)),
		deltaT(60),
                Transpiration(0.000247),  //Kg/sec
                RH_initial(0.50)

{   
    
	alpha = vector<double>(size,5);
	qrad = vector<double> (size,0);
	qcond = vector<double> (size,0);
	qconv = vector<double> (size,0);
	T0 = vector<double> (size,280);
	viewFactor prova;
	F = prova.Factor(geo.ext_land,geo.span_number,geo.span_width,geo.span_height,geo.cover_height,geo.domain_height);
	A = prova.Area_calculation();
	e[1] = 1; //sky black body
	e[7] = 1;  //low inlet 
	e[2] = 1; //ext soil
	e[0]=geo.emi_cover_out;
	e[4]=geo.emi_cover_in;
	e[3]=e[5]= geo.emi_sidewall_out;
	e[6]=geo.emi_ext_soil; //top inlet
	//Initial conditions
	T[1] = geo.sky_temp; //kelvin t_sky
	T[7] = geo.sky_temp;
	T[2] = 283; //external soil temperature
	T[4]=T[0]=278;
	T[3]=T[6]=283;
	T[4]=285;
	t[0]=geo.tra_cover_out;
	t[4]=geo.tra_cover_in;
	t[3]=t[5]=geo.tra_sidewall_out;
	qcond[6]= geo.heat_flux;
	prova_coef=convective_coef_forced(geo.ext_land,2); 
	alpha[0]= 0.95 + 6.76*pow(geo.wind_speed,0.49);   //convective_coef_forced(7,geo.wind_speed);
	alpha[2] =  convective_coef_forced(geo.ext_land,geo.wind_speed);
        alpha[3] = convective_coef_forced(8,geo.wind_speed);
	//alpha[0]=alpha[3]=alpha[2]=2.7;
	//alpha[3]=alpha[2]=alpha[0]= 2.8+3.0*geo.wind_speed;
	//alpha[3]= 2.8+3.0*(geo.wind_speed/4);
	T_air_inside = T_inside0 = geo.T_air_inside;//T_air_inside-1;
	T_iter_0 = 0;
	relax = 0.25;
};

void greenhouse::solver(int timelenght, int iteration_for_timestep){
	T_ins_evo = vector<double> (timelenght,0);
	T_cover = vector<double> (timelenght,0);
        RH = vector<double> (timelenght,RH_initial);
        cond_rate = vector<double> (timelenght,0);
        double humidity_ratio_next;
        double RH0 = RH_initial;
	int i = iteration_for_timestep;
	int pause,time;
	for ( time=0; time<=timelenght; time++)
	{
		for (int i=0; i<=4000; i++) 
		{
			T0=T;
			T[0]=T[4];
			T[5]=T[3];
			Radiation radia(A,F,e,T,j,g,t);
			//alpha[4]= convective_coef_natural_2(4.5,T_air_inside,T[6]);
			alpha[6]=2.21*pow(fabs(T[6]-T_air_inside),0.33);
                        alpha[4]=2.21*pow(fabs(T[4]-T_air_inside),0.33);
			//alpha[6]=2.21*pow(fabs(T[6]-T_air_inside),0.33);
			alpha[5]=1.246*pow(fabs(T[5]-T_air_inside),0.33);
                        if (time == (timelenght -1)){
                                cout << "outer cover heat tr coeff"<< alpha[0]<<endl;
                                cout << "outer soil tr coeff"<< alpha[2]<<endl;       
                                cout << "outer sidewall heat tr coeff"<< alpha[3]<<endl;
                                cout << "inner cover heat tr coeff"<< alpha[4]<<endl;
                                cout << "inner sidewall heat tr coeff"<< alpha[5]<<endl;
                                cout << "inner soil heat tr coeff"<< alpha[6]<<endl;
                                 }
			//alpha[4]=1.246*pow(fabs(T[4]-T_air_inside),0.33);
			/*alpha[4] = 2.2;
			alpha[5] = 1.54;
			alpha[6] = 2.76;
			alpha[0] = 4.85;
			alpha[3] = 3.09;*/
                        //alpha[6]= alpha[5]=alpha[4];
			Convection conve(alpha,geo.T_air,T,T_air_inside);
			qrad = radia.qradiation();
			qconv = conve.qconvection();
			T[6]= ((qcond[6]+alpha[6]*T_air_inside+e[6]*g[6])/(e[6]*kbol*pow(T[6],3)+alpha[6])); //soil conditions
			T[4]= (e[0]*g[0]+alpha[0]*geo.T_air+e[4]*g[4]+alpha[4]*T_air_inside -t[0]*j[4]+t[0]*j[0] - t[4]*j[0] +t[4]*j[4])/(e[0]*kbol*pow(T[4],3)+alpha[0]+alpha[4]+e[4]*kbol*pow(T[4],3)); //cover condition
			T[3]= (e[5]*g[5]+alpha[5]*T_air_inside+e[3]*g[3]+alpha[3]*geo.T_air -t[5]*j[3]+t[5]*j[5] - t[3]*j[5] +t[3]*j[3])/(e[5]*kbol*pow(T[3],3)+alpha[5]+alpha[3]+e[3]*kbol*pow(T[3],3)); //sidewall condition
			T_air_inside = (alpha[5]*T[5]*A[5]+alpha[4]*T[4]*A[4]+alpha[6]*T[6]*A[6]+(geo.rho*geo.cp*Vol*T_inside0/deltaT))/(alpha[5]*A[5]+alpha[4]*A[4]+alpha[6]*A[6]+ (geo.rho*geo.cp*Vol/deltaT));
			T[6] = T0[6] + relax*(T[6]-T0[6]);
			T[4] = T0[4] + relax*(T[4]-T0[4]);
			T[3] = T0[3] + relax*(T[3]-T0[3]);

                            
                            double pause;
                            //cin >>pause;
			if (fabs(T_iter_0-T_air_inside)<=0.000001 && ((fabs((qconv[4]*A[4]+qconv[5]*A[5]+qconv[6]*A[6])-(T_air_inside-T_inside0)*(geo.cp*geo.rho*Vol)/(deltaT)))<=0.000001)) 
			{   
				T_cover[time] = T[0];
			    T_ins_evo[time]=T_inside0 = T_air_inside;
                            //cond_rate[time]= condensation(T_cover[time],T_air_inside,RH0,1.2,Vol);
                            //RH[time]= Relative_Humidity(T_air_inside,humidity_ratio_next);
                            humidity_ratio_next = ((humidity_ratio(T_air_inside,RH0)*1.2*Vol) + Transpiration*deltaT )/(1.2*Vol);
                            //condensation(T_cover[time],T_air_inside,RH0,1.2,Vol)
                            RH[time]= Relative_Humidity(T_air_inside,humidity_ratio_next);
                            cond_rate[time]= condensation(T_cover[time],T_air_inside,RH[time],1.2,Vol);
                            humidity_ratio_next = ((humidity_ratio(T_air_inside,RH0)*1.2*Vol) + Transpiration*deltaT - cond_rate[time])/(1.2*Vol)  ;
                            RH[time]= Relative_Humidity(T_air_inside,humidity_ratio_next);
                            cout << "RH cover" << Relative_Humidity(T_cover[time],humidity_ratio_next) <<endl;
                            cout << "transpriatio" << Transpiration*deltaT << endl;
                            cout << "humidity_ratio_next" << humidity_ratio_next <<endl;
                            cout << "RH " << RH[time] <<endl;
                            cout<<"condensation" << cond_rate[time] << endl;
                            RH0 = RH[time];
                            
                            double pause;
                            //cin >>pause;
			    break;
		     }

			T_iter_0 = T_air_inside;
			
	     }
		print_result_humidity(T_cover,T_ins_evo,T_ins_evo,T_ins_evo,RH,cond_rate,(timelenght+1));
                cout << "time is" << time << endl;
	}
};
