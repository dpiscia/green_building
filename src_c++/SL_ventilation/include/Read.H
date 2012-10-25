#ifndef Read_H
#define Read_H

using namespace std;

class Read{

public: 

double span_height,span_width,cover_height,domain_height,ext_land,T_air_inside,T_air,wind_speed,out_hum_ratio;
double sky_temp,heat_flux,emi_sky,emi_ext_soil,emi_cover_out,tra_cover_out,emi_cover_in,tra_cover_in,emi_sidewall_out,tra_sidewall_out,emi_sidewall_in,tra_sidewall_in,degree_window;
double rho;  
double cp;
int span_number;

Read(string file_name){

ifstream myfile;

string line;
string name;
string value_s;
float value;
char item[20];

myfile.open (file_name.c_str());
  if (myfile.is_open())
  {
    if( myfile.is_open() )
    { int i = 0;
      /*while(! myfile.eof()) 
      {
       getline(myfile, name, '=');
       myfile >>  value;
       myfile.ignore(2);
       cout << "name is   "<<name<<endl; 
       cout << "value is   "<<value<<endl;
       continue;
       }*/
       while(!getline(myfile,name,'=').eof())
       {
         i = i +1;
         //cout<<"name is "<<name<<endl;
         getline(myfile,value_s);
         //cout<<"vlaueis ";
         
         if (i==1) { span_height=atof(value_s.c_str());}
         else if (i==2) { span_width=atof(value_s.c_str());}
         else if (i==3) { span_number=atof(value_s.c_str());}
         else if (i==4) { cover_height=atof(value_s.c_str());}
         else if (i==5) { domain_height=atof(value_s.c_str());}
         else if (i==6) { ext_land=atof(value_s.c_str());}
         else if (i==7) { rho=atof(value_s.c_str());}
         else if (i==8) { cp=atof(value_s.c_str());}
         else if (i==9) { T_air_inside=atof(value_s.c_str());}
         else if (i==10) { T_air=atof(value_s.c_str());}
         else if (i==11) { sky_temp=atof(value_s.c_str());}
         else if (i==12) { heat_flux=atof(value_s.c_str());}
         else if (i==13) { emi_sky=atof(value_s.c_str());}
         else if (i==14) { emi_ext_soil=atof(value_s.c_str());}
         else if (i==15) { emi_cover_out=atof(value_s.c_str());}
         else if (i==16) { tra_cover_out=atof(value_s.c_str());}
         else if (i==17) { emi_cover_in=atof(value_s.c_str());}
         else if (i==18) { tra_cover_in=atof(value_s.c_str());}
         else if (i==19) { emi_sidewall_out=atof(value_s.c_str());}
         else if (i==20) { tra_sidewall_out=atof(value_s.c_str());}
         else if (i==21) { emi_sidewall_in=atof(value_s.c_str());}
         else if (i==22) { tra_sidewall_in=atof(value_s.c_str());}
         else if (i==23) { wind_speed=atof(value_s.c_str());}
         else if (i==24) { degree_window=atof(value_s.c_str());}
         else if (i==25) { out_hum_ratio=atof(value_s.c_str());}
              
             
           
        }
     }
    myfile.close();
  }

  else {cout << "Unable to open file";
  //exit (EXIT_FAILURE);
  }
  




 }

};   
#endif
