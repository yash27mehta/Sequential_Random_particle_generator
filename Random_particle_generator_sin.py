#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed July 1 10:31:57 2020
@author: yashmehta

# This script generates a particle.inp file for the AWESUMM Code
# Right now it works for only 2-D
# Particles volume fractions are specified by the user (each bin as phi) 
# Bin are horizontal
# Bins sizes are assumed to be fixed as of now (specified by the user)
# Particles are distributed randomly in each bin
# Particle distribution is periodic in y and z direction 
"""

import numpy as np
import random as rand
import subprocess as sp
tmp = sp.call('clear', shell=True)
import sys
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

from Distance import distance
from Area_fraction import area_fraction

# main code
dim = 2  # 2-D or 3-D
Dp = 1 # Diameter of the particles 
particle_density = 35

x_part_domain = [0,20] # x_min and x_max
y_part_domain = [(0,3),(3,6),(6,9),(9,12),(12,15),(15,18),(18,21),(21,24)] # y_min and y_max for each bin, this hardcoded for now
y_part_domain_for_area = [y_part_domain[0][0],y_part_domain[-1][1]]
z_part_domain = [-4,4] # z_min and z_max

x_part_domain_len = x_part_domain[1]-x_part_domain[0]
y_part_domain_len = y_part_domain[-1][1]-y_part_domain[0][0]
z_part_domain_len = z_part_domain[1]-z_part_domain[0]

# User specified volume fraction in each bin to repesent a sinusoidal dist in y
part_vol_frac = [0.2,0.25,0.3,0.25,0.2,0.15,0.1,0.15]
Np = np.zeros(len(part_vol_frac)) # empty array for number of particles in each bin

pi = np.pi
dist_tol = Dp+ (Dp/10) # min inter-particle distance

# compute the number of particles based on the volume fraction and initalize an

if dim == 2:
    
    vol_1_part = pi*(Dp/2)**2  
    
    for i in range(len(part_vol_frac)) :
        vol_domain = abs(x_part_domain[1]-x_part_domain[0])*abs(y_part_domain[i][1]-y_part_domain[i][0])
        # print(int((vol_domain*part_vol_frac[i])/vol_1_part))
        Np[i] = int((vol_domain*part_vol_frac[i])/vol_1_part) # compute number of particles in each bin
    
else :
    
    sys.exit(quit)


# Global particle array 
Np = Np.astype(np.int)    
particles_global = np.zeros((sum(Np),10))
particles_global[:,0] = (Dp/2)
particles_global[:,1] = particle_density

mean_vol_frac = (sum(Np)*vol_1_part)/(abs(x_part_domain[1]-x_part_domain[0])*abs(y_part_domain[-1][1]-y_part_domain[0][0]))

# loop over particle number
global_count = 0
for i in range(len(Np)):
    
    # counter for each bin   
    count = 0
    
    while count<Np[i] :
        # print(count)
        
        # generate random x, y positions            
        tmp_x_pos = rand.uniform(x_part_domain[0],x_part_domain[1])
        tmp_y_pos = rand.uniform(y_part_domain[i][0],y_part_domain[i][1])
        
        # this is redundant since current version is 2-D but required since distance and area functions are generic 3-D
        tmp_z_pos = (dim-2)*rand.uniform(z_part_domain[0],z_part_domain[1])
        
        # first particle
        if global_count == 0 :
            particles_global[global_count,2] = tmp_x_pos
            particles_global[global_count,3] = tmp_y_pos
            
            global_count = global_count + 1                                       
            count = count + 1
                 
        else :
            
            # check for overlap with all previous particles
            dist_bol = distance(dim,global_count,particles_global,tmp_x_pos,tmp_y_pos,tmp_z_pos,dist_tol, \
                            x_part_domain_len,y_part_domain_len,z_part_domain_len)
            
                
            #print(dist_bol)
            if dist_bol == True:
                particles_global[global_count,2] = tmp_x_pos
                particles_global[global_count,3] = tmp_y_pos
                     
                if dim == 3 :
                    particles_global[global_count,4] = tmp_z_pos
                
                global_count = global_count + 1    
                count = count + 1



direction = 1

area_fraction(direction,dim,Dp,particles_global,x_part_domain,y_part_domain_for_area,z_part_domain)

direction = 2

area_fraction(direction,dim,Dp,particles_global,x_part_domain,y_part_domain_for_area,z_part_domain)

fig, ax = plt.subplots()
plt.plot(particles_global[:,2], particles_global[:,3], marker = '.', color = 'k', linestyle = 'None')
# plt.plot(particles_global[:,2], particles_global[:,3]-y_part_domain_len, marker = '.', color = 'k', linestyle = 'None')
# plt.plot(particles_global[:,2], particles_global[:,3]+y_part_domain_len, marker = '.', color = 'k', linestyle = 'None')
for i in range(global_count):
    circle1 = plt.Circle((particles_global[i,2], particles_global[i,3]), Dp/2, color = 'r')
    # circle2 = plt.Circle((particles[i,2], particles[i,3]-y_part_domain_len), Dp/2, color = 'k')
    # circle3 = plt.Circle((particles[i,2], particles[i,3]+y_part_domain_len), Dp/2, color = 'k')
    ax.add_artist(circle1)
    # ax.add_artist(circle2)
    # ax.add_artist(circle3)

plt.show()

# # # # np.savetxt('Mul_Cyl_Demo.inp', particles, fmt='%5.23e', delimiter=' ') 
   
