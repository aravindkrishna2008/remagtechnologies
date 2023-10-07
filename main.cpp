#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <utility>

using namespace std;

vector<pair<int,float>> outside_input() {
    ifstream file;
      file.open("output.txt");
    vector<pair<int,float>> raw_data_nT;
    int data_points;
    file >> data_points;
    for(int i = 0; i < data_points; i++) {
        int n1;
        float n2;
        file >> n1 >> n2;
        raw_data_nT.push_back(make_pair(n1,n2));
    }
    return raw_data_nT;
}

//Reconnection Rate
pair<float,bool> rate(float B) {
    //physical variables
    bool magnetic_flip = false;
    if (B<0) {
        magnetic_flip = true;
        B = -B;
    }
    float L_times_10e16 = 1.3981973;
    double µ_0 = 4*M_PI/10000000;
    float dif = 610;
    float ion_density = 20000;
    double v_a = B/sqrt(µ_0*ion_density);
    float S = v_a*L_times_10e16/dif;
    return make_pair(100*pow(S,-0.5),magnetic_flip);
}

int main() {
    //Reconnection Rate computation using the Sweet-Parker model
    vector<pair<int,float>> data = outside_input();
    int month,year;
    //tracks how long conspicuous activity has occurred
    int counter = 0;
    for (auto i : data) {
        pair<float,bool> R = rate(1000*i.second);
        i.second = R.first;
        //index -- reconnection rate (m^2/s) -- IMF flip (yes/no)
        cout << i.first << " -- " << i.second << " -- " << R.second << "\n";
        if (R.second && i.second<5000000) {
            cout << " ** Major IMF flip occurred" << "\n";
            counter++;
            if (counter>4) {
                cout << "\n\n --- POTENTIAL SEVERE SOLAR EVENT --- " << month << "/" << i.first << "/" << year << "\n\n";
            }
        }
    }
    //forward data to the exterior programs in the website/backend
}