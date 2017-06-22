#!/usr/bin/env python
# Author: Kelcey Damage <kdamage@Palantir.com>
# Python: 2.66
# OS: CentOS
# Portable: True

# Summary
#--------------------------------------------------------------------------------------------------#
# a, <
# |\ 
# | \
# |  \ h
# |   \
# |____\
# b     c
#
# convert polar coordinates into planar coordinates.
# 
# This module is intended for filtering sensor data by angular position and computing the planar
# coordinates. 

# Imports
#--------------------------------------------------------------------------------------------------#
from __future__ import print_function
import math

# Globals
#--------------------------------------------------------------------------------------------------#

# Classes
#--------------------------------------------------------------------------------------------------#

# Functions
#--------------------------------------------------------------------------------------------------#
def convert_to_planar(angle, hypotenuse):
	radians = math.radians(angle)
	opposite = hypotenuse * math.sin(radians)
	adjacent = hypotenuse * math.cos(radians)
	return opposite, adjacent

def zone_filter(zone_count, values):
	# Zones should be read in a clockwise manner
	stepping = 360 / zone_count
	print(stepping)
	zones = {}
	for i in range(zone_count):
		zones[i] = {
				'distance': [],
				'angle': [],
				'planar_coords': []
			}
	for value in values:
		index = math.floor(value[0] / stepping)
		zones[index]['distance'].append(value[1])
		zones[index]['angle'].append(value[0])
		zones[index]['planar_coords'].append(convert_to_planar(value[0], value[1]))
	return zones

# Main
#--------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
	reads = [
		[35, 47]
		]
	zone_count = 1
	print(zone_filter(zone_count, reads))


