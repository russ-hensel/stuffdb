#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pacitance (in farads)
$ \epsilon_0 $: Permittivity of free space ($ 8.854 \times 10^{-12} \, \text{F/m} $)
$ \epsilon_r $: Relative permittivity (dielectric constant) of the insulating material (e.g., ~4–7 for glass)
$ l $: Effective length of the overlapping conductive surfaces (in meters)
$ a $: Radius of the inner conductor (in meters)
$ b $: Radius of the outer conductor (in meters)
$ \ln(b/a) $: Natural logarithm of the ratio of the outer radius to the inner radius
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof

import math

# Constants
EPSILON_0   = 8.854e-12  # Permittivity of free space (F/m)
EPSILON_R   = 5.5        # Relative permittivity for glass (average value)
PI          = math.pi
R_MOON      = float( 384_400_000  ) # radius of moons orbit more or less in meters

def leyden_jar_capacitance( inner_radius, outer_radius, length):
    """
    Calculate the capacitance of a Leyden jar.

    Args:
        inner_radius (float): Radius of inner conductor (m)
        outer_radius (float): Radius of outer conductor (m)
        length (float): Effective length of overlapping surfaces (m)

    Returns:
        float: Capacitance in farads
    """
    capacitance = (2 * PI * EPSILON_0 * EPSILON_R * length) / math.log(outer_radius / inner_radius)
    print( f"Inner radius {a = } outer radius {b = }  length {l = } all in meters")
    print(f"Capacitance of the Leyden jar: {capacitance:.2e} F")
    return capacitance

# Example usage
if __name__ == "__main__":
    a = 0.05  # Inner radius in meters = (5 cm)
    b = 0.06  # Outer radius n meters = (6 cm)
    l = 0.2   # Length (20 cm)
    capacitance = leyden_jar_capacitance(a, b, l)

    print( "\nradius = 1/10 moon units, height = one moon unit, thickness = .001 cm ")
    a   = R_MOON/10
    b   = a + .001
    l   = R_MOON
    capacitance = leyden_jar_capacitance(a, b, l)



