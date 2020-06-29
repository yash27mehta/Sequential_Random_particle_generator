# -*- coding: utf-8 -*-
# This is a distance function which takes in particle centers and finds the 
# distance between them (takes into account periodic boundary conditions in y and z)
# Author : Yash Mehta
import numpy as np

def distance(dim,count,particles,tmp_x_pos,tmp_y_pos,tmp_z_pos,dist_tol, \
             x_part_domain_len,y_part_domain_len,z_part_domain_len):
    
    dist = np.empty([count])
    
    for i in range(count) :
        
        if dim == 2 :
            dist[i] = min(((particles[i,2]-tmp_x_pos)**2 \
                      + (particles[i,3]-tmp_y_pos)**2)**0.5,
                      ((particles[i,2]-tmp_x_pos)**2 \
                      + ((particles[i,3]-y_part_domain_len)-tmp_y_pos)**2)**0.5,
                       ((particles[i,2]-tmp_x_pos)**2 \
                      + ((particles[i,3]+y_part_domain_len)-tmp_y_pos)**2)**0.5)

        else : 
            dist[i] = min(((particles[i,2]-tmp_x_pos)**2 \
                      + (particles[i,3]-tmp_y_pos)**2 \
                      + (particles[i,4]-tmp_z_pos)**2)**0.5,
                      ((particles[i,2]-tmp_x_pos)**2 \
                      + ((particles[i,3]-y_part_domain_len)-tmp_y_pos)**2 \
                      + (particles[i,4]-tmp_z_pos)**2)**0.5,
                      ((particles[i,2]-tmp_x_pos)**2 \
                      + ((particles[i,3]+y_part_domain_len)-tmp_y_pos)**2 \
                      + (particles[i,4]-tmp_z_pos)**2)**0.5,
                      ((particles[i,2]-tmp_x_pos)**2 \
                      + (particles[i,3]-tmp_y_pos)**2 \
                      + ((particles[i,4]-z_part_domain_len)-tmp_z_pos)**2)**0.5,
                      ((particles[i,2]-tmp_x_pos)**2 \
                      + (particles[i,3]-tmp_y_pos)**2 \
                      + ((particles[i,4]+z_part_domain_len)-tmp_z_pos)**2)**0.5)
                      

    if np.amin(dist)<= dist_tol :
        
        return False
    
    else :
        
        return True
    
