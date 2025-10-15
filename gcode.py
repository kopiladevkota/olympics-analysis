# winggcode – basic usage example

import wing  # from the swarfer/winggcode project
import os

def generate_wing_gcode(airfoil_name, span, root_chord, tip_chord, washout_deg=0.0, steps=20):
    """
    Generate G-code for a tapered wing using the specified airfoil.
    - airfoil_name: name of the .dat file (e.g., 'mh45')
    - span: total wingspan (mm)
    - root_chord / tip_chord: chord lengths at root and tip (mm)
    - washout_deg: twist at tip in degrees
    - steps: number of cross-sections along the span
    """
    wg = wing.Wing()
    wg.airfoil = airfoil_name
    wg.span = span / 2           # winggcode cuts one half-wing
    wg.root_chord = root_chord
    wg.tip_chord = tip_chord
    wg.washout = washout_deg
    wg.steps = steps
    wg.output = f"{airfoil_name}_wing"

    # Optional: feedrate, wire settings
    wg.feed_rate = 2000  # mm/min
    wg.max_temp = 20     # V-value for wire power control

    wg.generate_gcode()
    print("G-code generated to:", wg.nc_left, wg.nc_right)
    # Files: <output>-left.nc, <output>-right.nc

if __name__ == "__main__":
    # Example: MH45 airfoil, 900mm span, chord taper 150→100mm:
    generate_wing_gcode('mh45', span=900, root_chord=150, tip_chord=100, washout_deg=2.0, steps=30)
