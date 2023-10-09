#include <bits/stdc++.h>
using namespace std;


vector<tuple<int, float, float>> outside_input() {
  // data import (format: {day number, min(Bz), max(Bz)})
  ifstream file;
  file.open("output.txt");
  int amt;
  file >> amt;
  vector<tuple<int, float, float>> raw_data_nT;
  for (int i = 0; i < amt; i++) {
    int n1;
    float n2;
    float n3;
    file >> n1 >> n2 >> n3;
    raw_data_nT.push_back(make_tuple(n1+1, n2, n3));
  }
  return raw_data_nT;
}

// Reconnection Rate
pair<float, bool> rate(float B) {
  // physical variables
  bool magnetic_flip = false;
  if (B < 0) {
    magnetic_flip = true;
    B = -B;
  }
  float L_times_10e16 = 1.3981973;
  double µ_0 = 4 * M_PI / 10000000;
  float dif = 610;
  float ion_density = 20000; // steve is asking why this is the value
  double v_a = B / sqrt(µ_0 * ion_density);
  float S = v_a * L_times_10e16 / dif;
  return make_pair(1 / pow(S, 0.5), magnetic_flip);
}

int main() {
  // Reconnection Rate computation using the Sweet-Parker model
  vector<tuple<int, float, float>> data = outside_input();
  int counter = 0;
  pair<int,float> pre_flip;

  /*output data:
  1. day
  2.reconnection rate of IMF flip (min(Bz))
  3.IMF peak?
  4.IMF flip?
  5.Solar event?
  6.Severity rating (G scale)
  */
	
  vector<tuple<int,float,bool,bool,bool,int>> results;
  for (auto i : data) {
	tuple<int,float,bool,bool,bool,int> output_tuple = {0,0,false,false,false,0};
	  
    pair<float, bool> R_min = rate(1000 * get<1>(i));
    pair<float, bool> R_max = rate(1000 * get<2>(i));
    get<1>(i) = R_min.first;
    get<2>(i) = R_max.first;
	  
    // day -- reconnection rate (min then max) -- IMF flip (yes/no)
	get<0>(output_tuple) = get<0>(i);
	get<1>(output_tuple) = get<1>(i);

	  
    // tracking how long conspicuous activity has occurred
	  
	// detecting negative flip < ~-35nT
    if (R_min.second && get<1>(i) < 0.045) {
      get<3>(output_tuple) = true;
      counter++;
    }
    // detecting positive peak > ~30nT
    if (!R_max.second && get<2>(i) < 0.055) {
      get<2>(output_tuple) = true;
      pre_flip = {get<0>(i),pow(get<2>(i),-0.5)};
    }
    // testing validity of possible solar storm
    if (counter && (get<0>(i) - pre_flip.first) < 8) {
      get<4>(output_tuple) = true;
	  //estimating severity of the solar storm
	  float flip_gap = pre_flip.second + pow(get<1>(i),-0.5);
	  if (flip_gap>7) {
		  get<5>(output_tuple) = 5;
	  } else if (flip_gap>6.22) {
		  get<5>(output_tuple) = 4;
	  } else if (flip_gap>5.44) {
		  get<5>(output_tuple) = 3;
	  } else if (flip_gap>4.66) {
		  get<5>(output_tuple) = 2;
	  } else if (flip_gap>3.89) {
		  get<5>(output_tuple) = 1;
	  } else {
		  get<5>(output_tuple) = 0;
	  }
	}
    results.push_back(output_tuple);
  }
  for (auto i : results) {
		cout << get<0>(i) << " " << get<1>(i) << " " << get<2>(i) << " " << get<3>(i) << " " << get<4>(i) << " " << get<5>(i) << "\n";
  }
}