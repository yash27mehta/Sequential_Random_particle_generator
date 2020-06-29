#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:01:57 2019
@author: yashmehta

# This script generates a particle.inp file for the AWESUMM Code
# User can specify if simulation is 2-D or 3-D
# Particles will be randomly distributed based on volume fraction and other 
# constraints provided by the user
# Particles can have random initial velocities if required
# Particle distribution is periodic in y and z direction 
"""

import numpy as np
import random as rand
import math as ma
import subprocess as sp
tmp = sp.call('clear', shell=True)
import sys
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

from Distance import distance

# main code
dim = 2  # 2-D or 3-D
Dp = 1 # Diameter of the particles 
particle_random_vel = False
partilce_random_vel_bound_min = 0.4
partilce_random_vel_bound_max = 0.8
particle_density = 35

x_part_domain = [0,8] # x_min and x_max
y_part_domain = [-4,4] # y_min and y_max
z_part_domain = [-4,4] # z_min and z_max

x_part_domain_len = x_part_domain[1]-x_part_domain[0]
y_part_domain_len = y_part_domain[1]-y_part_domain[0]
z_part_domain_len = z_part_domain[1]-z_part_domain[0]

part_vol_frac = 32/100 # particle volume fraction
pi = ma.pi
dist_tol = Dp+ (Dp/10) # min inter-particle distance

# compute the number of particles based on the volume fraction and initalize an
# empty array

if dim == 2:
    
    vol_1_part = pi*(Dp/2)**2  
    vol_domain = abs(x_part_domain[1]-x_part_domain[0])*abs(y_part_domain[1]-y_part_domain[0])
    Np = int((vol_domain*part_vol_frac)/vol_1_part)
    particles = np.zeros([Np,10])
                  
elif dim == 3:
    
    vol_1_part = pi*(4/3)*(Dp/2)**3
    vol_domain = abs(x_part_domain[1]-x_part_domain[0])*abs(y_part_domain[1]-y_part_domain[0]) \
                 * abs(z_part_domain[1]-z_part_domain[0])
    Np = int((vol_domain*part_vol_frac)/vol_1_part)
    particles = np.zeros([Np,14])
   

else :
    
    sys.exit(quit)

# set same particle radius and density for all particles    
particles[:,0] = (Dp/2)
particles[:,1] = particle_density



# loop over particle number
count = 0
while count<Np :
    print(count)
        
    if particle_random_vel == True :
        
       
        particles[count,dim+2] = rand.choice((-1,1))*rand.uniform(partilce_random_vel_bound_min,partilce_random_vel_bound_max)
        particles[count,dim+3] = rand.choice((-1,1))*rand.uniform(partilce_random_vel_bound_min,partilce_random_vel_bound_max)
        
        if dim == 3 :
            particles[count,dim+4] = rand.choice((-1,1))*rand.uniform(partilce_random_vel_bound_min,partilce_random_vel_bound_max)
    
     
    tmp_x_pos = rand.uniform(x_part_domain[0],x_part_domain[1])
    tmp_y_pos = rand.uniform(y_part_domain[0],y_part_domain[1])
    # z only if dim = 3
    tmp_z_pos = (dim-2)*rand.uniform(z_part_domain[0],z_part_domain[1])
     
    if count == 0 :
        particles[count,2] = tmp_x_pos
        particles[count,3] = tmp_y_pos
    
        
         
        if dim == 3:
            particles[count,4] = tmp_z_pos
            
                        
        count = count + 1
             
    else :
        
       
        dist_bol = distance(dim,count,particles,tmp_x_pos,tmp_y_pos,tmp_z_pos,dist_tol, \
                            x_part_domain_len,y_part_domain_len,z_part_domain_len)
        
            
        #print(dist_bol)
        if dist_bol == True:
            particles[count,2] = tmp_x_pos
            particles[count,3] = tmp_y_pos
                 
            if dim == 3 :
                particles[count,4] = tmp_z_pos
                
            count = count + 1


fig, ax = plt.subplots()
plt.plot(particles[:,2], particles[:,3], marker = '.', color = 'k', linestyle = 'None')
plt.plot(particles[:,2], particles[:,3]-y_part_domain_len, marker = '.', color = 'k', linestyle = 'None')
plt.plot(particles[:,2], particles[:,3]+y_part_domain_len, marker = '.', color = 'k', linestyle = 'None')
for i in range(Np):
    circle1 = plt.Circle((particles[i,2], particles[i,3]), Dp/2, color = 'r')
    circle2 = plt.Circle((particles[i,2], particles[i,3]-y_part_domain_len), Dp/2, color = 'k')
    circle3 = plt.Circle((particles[i,2], particles[i,3]+y_part_domain_len), Dp/2, color = 'k')
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)

plt.show()

np.savetxt('Mul_Cyl_Demo.inp', particles, fmt='%5.23e', delimiter=' ') 
   
