#include <viewFactor.H>

using namespace std;

//vector<double> viewFactor::Factor(double ext_land,int span_number, double span_lenght,double span_height,double cover_height,double domain_height)
double2D viewFactor::Factor(double ext_land,int span_number, double span_lenght,double span_height,double cover_height,double domain_height)
{
//external and internal calculation
double AB,BC,CD,SA,RS,QR,Dd,Bb;
Dd = cover_height;
AB = ext_land;
QR = (AB*2)+ (span_number*span_lenght);
BC = span_height;
RS = (domain_height - BC - Dd);
Bb = span_lenght; 
CD = pow(Dd,2)+ pow(Bb/2,2);
CD = pow(CD,0.5);
cout<<"AB "<<AB<<" QR "<<QR<<"BC "<<BC<<"RS "<<RS<<"Dd "<<Dd<<"Bb "<<Bb<<endl;
cout<<"CD "<<CD<<endl;

//internal calculation

double BN = span_number*span_lenght;
cout<<"BN "<<BN<<endl;
double CN = pow(BN,2)+pow(BC,2);
CN = pow(CN,0.5);
cout<<"CN "<<CN<<endl;
double F_soil_sidewall= 1-((CN*2) -(BC*2))/(2*BN);
cout<<"F_soil_sidewall "<<F_soil_sidewall<<endl;
double F_soil_cover= 1 - F_soil_sidewall;
cout<<"F_soil_cover "<<F_soil_cover<<endl;
Area[6] = BN;
Area[5] = BC*2;
Area[4] = CD*2*span_number;
cout<<"A[4] "<<Area[4]<<"A[5] "<<Area[5]<<"A[6] "<<Area[6]<<endl;
double F_side_side;
//cout<<"F_Side_side "<<F_side_side<<endl;
double F_sidewall_soil = F_soil_sidewall*Area[6]/Area[5];
cout<<"F_soil_sidewall "<<F_sidewall_soil<<endl;
double F_sidewall_cover = F_sidewall_soil;
F_side_side = 1 - (F_sidewall_soil*2);
cout<<"F_side_side "<<F_side_side<<endl;
double F_cover_soil = F_soil_cover * Area[6]/Area[4];
cout<<"F_cover_soil "<<F_cover_soil<<endl;
double F_cover_sidewall = F_sidewall_cover * Area[5]/Area[4];
cout<<"F_cover_sidewall "<<F_cover_sidewall<<endl;
double F_cover_cover = 1 - F_cover_sidewall -F_cover_soil;
cout<<"F_cover_cover "<<F_cover_cover<<endl;
F[4][4] = F_cover_cover;
F[4][5] = F_cover_sidewall;
F[4][6] = F_cover_soil;
F[5][4] = F_sidewall_cover;
F[5][5] = F_side_side;
F[5][6] = F_sidewall_soil;
F[6][4] = F_soil_cover;
F[6][5] = F_soil_sidewall;
F[6][6] = 0;

//external 
Area[2] = AB*2;
Area[3] = BC*2;
double AS = BC+Dd;
cout<<"AS "<<AS<<endl;
Area[7] = AS*2;
Area[1] = QR +(domain_height*2 -Area[7]);
cout<<"Area1 "<<Area[1]<<endl;
Area[0]=Area[4];
double AC = pow(AB,2) +pow(BC,2);
AC = pow(AC,0.5);
cout<<"AC "<<AC<<endl;
F[2][3] = ((AB+BC)-AC)/(2*AB);
cout<<"F[2][3] "<<F[2][3]<<endl;
F[3][2] = F[2][3]*Area[2]/Area[3];
cout<<"F[3][2] "<<F[3][2]<<endl;
//F[3][7] = 1 - F[3][2]*2;
//cout<<"F[3][7] "<<F[3][7]<<endl;
double BS = pow(AB,2)+pow(AS,2);
BS = pow(BS,0.5);
cout<<"BS "<<BS<<endl;
double CS = pow(AB,2) + pow(Dd,2);
CS = pow(CS,0.5);
cout<<"CS "<<CS<<endl;
F[3][7]= ((BS+AC-CS-AB)/(2*BC));
cout<<"F37 "<<F[3][7]<<endl;
F[3][1] = 1 -F[3][2] -F[3][7];
cout<<"F[3][1] "<<F[3][1]<<endl;
F[3][0]=F[3][3]=0;
F[2][2] = 0;
//soil_cover I have already AC
double BD = pow(Bb/2,2)+pow(BC+Dd,2);
BD = pow(BD,0.5);
cout<<"BD "<<BD<<endl;
double AD = pow(AB+Bb/2,2)+pow(BC+Dd,2);
AD = pow(AD,0.5);
cout<<"AD "<<AD<<endl;
F[2][0]= (AC+BD-AD-BC)/(AB*2);

cout<<"F[2][0] "<<F[2][0]<<endl;
if (F[2][0] <= 0) {F[2][0] = 0;   cout<<"azzerato"<<endl;};
F[2][7] = (AS+AB-BS)/(2*AB);
cout<<"F[2][7] "<<F[2][7]<<endl;
F[2][1] = 1 -F[2][3] -F[2][7];
cout<<"F[2][1] "<<F[2][1]<<endl;
F[7][2] = F[2][7]*Area[2]/Area[7];
cout<<"F[7][2] "<<F[7][2]<<endl;
F[7][3] = F[3][7]*Area[3]/Area[7];
cout<<"F[7][3] "<<F[7][3]<<endl;
//DS

double DS = AB+ Bb/2;
cout<<"DS "<<DS<<endl;
F[7][0] = (AD+CS-DS-AC)/(2*AS);
if (F[7][0]<=0 ){F[7][0] = 0;};
cout<<"F[7][0] "<<F[7][0]<<endl;
F[7][1]= 1 - F[7][0] - F[7][2] - F[7][3];
cout<<"F[7][1] "<<F[7][1]<<endl;
F[0][7] = F[7][0] * Area[7]/Area[0];
cout<<"F[0][7] "<<F[0][7]<<endl;
F[0][3] = 0;
F[0][2] = F[2][0] * Area[2]/Area[0];
cout<<"F[0][2] "<<F[0][2]<<endl;
double F_SP_sky = 1;
F[1][1] = 1- (F_SP_sky * QR / (2*RS + QR));
cout<<"F[1][1] "<<F[1][1]<<endl;
F[1][2] = F[2][1] * Area[2]/Area[1];
cout<<"F[1][2] "<<F[1][2]<<endl;
F[1][3] = F[3][1] * Area[3]/Area[1];
cout<<"F[1][3] "<<F[1][3]<<endl;
F[1][7] = F[7][1] * Area[7]/Area[1];
cout<<"F[1][7] "<<F[1][7]<<endl;
F[1][0] = 1 - F[1][1] - F[1][2] - F[1][3] - F[1][7];
cout<<"F[1][0] "<<F[1][0]<<endl;
cout<<"area[1] "<<Area[1]<<"area0 "<<Area[0]<<"area2 "<<Area[2]<<"area1 "<<Area[1]<<endl;
F[0][1] = F[1][0] * Area[1]/Area[0];
cout<<"F[0][1] "<<F[0][1]<<endl;
F[0][0] = 1 - F[0][1] - F[0][2] - F[0][3] - F[0][7];
cout<<"F[0][0] "<<F[0][0]<<endl;    
/*double BC,CD,Dd,Bb,AB,AQ,AO;
Area[1]=(AO+AQ)*2;
Area[2]=2*AB;
Area[3]=Area[0];
Area[4]=span_number*span_lenght; */
return F;

};

vector<double> viewFactor::Area_calculation(){
cout<<"Area calculation "<<endl;
return Area;
};
