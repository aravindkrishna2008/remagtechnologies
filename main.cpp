#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

const double µ_0 =
    4 * M_PI * 1e-7; // Magnetic permeability of free space (SI units)

// Function to calculate the magnetic reconnection rate
pair<double, bool> rate(double B_z) {
  // Define physical constants
  double L = 1.0;            // Typical length scale (adjust as needed)
  double ion_density = 2e19; // Ion density (SI units)

  // Ensure B_z is positive for calculations
  double abs_B_z = abs(B_z);

  // Calculate Sweet-Parker reconnection rate
  double v_a = abs_B_z / sqrt(µ_0 * ion_density); // Alfven velocity
  double S = L * v_a / µ_0;

  double reconnection_rate = 1e-6 * sqrt(S); // Adjust scaling as needed

  // Determine if there's a magnetic flip
  bool magnetic_flip = (B_z < 0);

  return make_pair(reconnection_rate, magnetic_flip);
}

int main() {
  // Read data from the input file
  ifstream file("output.txt");
  if (!file.is_open()) {
    cerr << "Error: Could not open input file 'output.txt'" << endl;
    return 1;
  }

  int amt;
  file >> amt;
  vector<pair<float, float>> data;

  for (int i = 0; i < amt; i++) {
    float day, B_z;
    file >> day >> B_z;
    data.push_back(make_pair(day, B_z));
  }

  file.close();

  // Calculate reconnection rates and check for flips
  int consecutive_flips = 0;

  for (const auto &entry : data) {
    pair<double, bool> result = rate(entry.second);

    cout << "Day " << entry.first << " - Reconnection Rate: " << result.first
         << " m^2/s";

    if (result.second) {
      cout << " - Magnetic Flip: Yes";
      consecutive_flips++;
      if (consecutive_flips >= 3) {
        cout << " *** POTENTIAL SEVERE SOLAR EVENT ***";
      }
    } else {
      cout << " - Magnetic Flip: No";
      consecutive_flips = 0; // Reset consecutive flip counter
    }

    cout << endl;
  }

  return 0;
}
