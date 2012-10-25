#ifndef viewFactor_H
#define viewFactor_H


using namespace std;

class viewFactor{
public:
//vector<vector<int> >ap;
double1D Area;
	

vector<double> view_array; 
double2D F;
viewFactor(){
 int size = 13;
view_array = vector<double> (3,1);
Area = vector<double> (size,1);
F = vector<vector <double> >(size, vector<double> (size,0)); 


}
~viewFactor(){};


vector<double> Area_calculation();
double2D Factor(double ext_land,int span_number, double span_lenght,double span_height,double cover_height,double domain_height);
};

#endif 
//double AB,int span_number, double span_lenght,double BC,double Dd,double domain_height

/**           R-----------------------------------------------------------Q       ***/
/**           !                                                           !        ***/
/**           !                                                           !        ***/
/**           !                                                           !        ***/
/**           !                                                           !        ***/
/**           !             D        F       H      L                     !        ***/
/**           !            /!\      / \     / \    / \                    !        ***/
/**           !           / ! \    /   \   /   \  /   \                   !        ***/
/**           S          C -d-- E--------G-------I-----M                  P        ***/
/**           !          !      !        !       !     !                  !        ***/
/**           !          !      !        !       !     !                  !        ***/
/**           !          !      !        !       !     !                  !        ***/
/**           A----------B------b----------------------N------------------O        ***/

/**  0- greenhouse_outside
/**  1- sky
/**  2_land
/**  3_ext_sidewall
/**  4_greenhouse_cover_inside
// 5 ins_sidewall
// 6 soil **/
// 7 SA+PO
