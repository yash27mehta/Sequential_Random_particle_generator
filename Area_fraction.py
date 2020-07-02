# -*- coding: utf-8 -*-
# This area fraction function computes the area fraction of particles in the 
# direction specified by the user
# !! Assumption that y and z are periodic 
# Author : Yash Mehta
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

def area_fraction(direction,dim,Dp,particles,x_part_domain,y_part_domain,z_part_domain):
    
    # Get domain info
    x_min = x_part_domain[0]-Dp
    x_max = x_part_domain[1]+Dp
    y_min = y_part_domain[0]
    y_max = y_part_domain[1]
    z_min = z_part_domain[0]
    z_max = z_part_domain[1]
    
    
    
    # Domain lengths
    x_part_domain_len = x_part_domain[1]-x_part_domain[0]
    y_part_domain_len = y_part_domain[1]-y_part_domain[0]
    z_part_domain_len = z_part_domain[1]-z_part_domain[0]
    
    # computing area fraction at delta interval
    delta = Dp/20
    
    # create the array at which area fraction will be computed
    x_array = np.arange(x_min,x_max+delta,delta)
    y_array = np.arange(y_min,y_max+delta,delta)
    z_array = np.arange(z_min,z_max+delta,delta)
    
    
    # Get the number of particles
    Np = len(particles)

    # Create an empty array to store area
    if direction == 1:
        area = np.zeros(len(x_array)) 
    elif direction == 2:
        area = np.zeros(len(y_array))
    elif direction == 3:
        area = np.zeros(len(z_array))
    
    # Choose the direction in which user wants to find the area
    if direction == 1 :
        
        for i in range(len(area)): # loop over the area array 
            
            for j in range(Np): # Loop over every particle
 
                if (abs(particles[j,2]-x_array[i]) <= Dp/2): # Particle intersecting the x-plane found
                    area[i] = area[i] + ((np.pi)**(dim-2))*((Dp/2)**2-(particles[j,2]-x_array[i])**2)**(0.5*(dim-1))
                    
    elif direction == 2:
        
        for i in range(len(area)): # loop over the area array 
            
            for j in range(Np): # Loop over every particle
 
                if (abs(particles[j,3]-y_array[i]) <= Dp/2 ): # Particle intersecting the y-plane found
                    
                    area[i] = area[i] + ((np.pi)**(dim-2))*((Dp/2)**2-(particles[j,3]-y_array[i])**2)**(0.5*(dim-1)) 
                    
                # elif (abs(abs(particles[j,3]-abs(y_part_domain_len))-y_array[i]) <= Dp/2): # Periodic
                    
                    
                #     area[i] = area[i] + ((np.pi)**(dim-2))*((Dp/2)**2-((particles[j,3]-abs(y_part_domain_len))-y_array[i])**2)**(0.5*(dim-1))
                    
                # elif (abs(abs(particles[j,3]+abs(y_part_domain_len))-y_array[i]) <= Dp/2): # Periodic
                    
                #     area[i] = area[i] + ((np.pi)**(dim-2))*((Dp/2)**2-((particles[j,3]+abs(y_part_domain_len))-y_array[i])**2)**(0.5*(dim-1))
   
    elif direction == 3:
        
        for i in range(len(area)): # loop over the area array 
            
            for j in range(Np): # Loop over every particle
 
                if (abs(particles[j,4]-z_array[i]) <= Dp/2 ): # Particle intersecting the z-plane found
                    
                    area[i] = area[i] + ((np.pi)**(dim-2))*((Dp/2)**2-(particles[j,4]-z_array[i])**2)**(0.5*(dim-1)) 
                    
                # elif (abs(abs(particles[j,4]-abs(z_part_domain_len))-z_array[i]) <= Dp/2): # Periodic
                    
                #     area[i] = area[i] + ((np.pi)**(dim-2))*((Dp/2)**2-((particles[j,4]-abs(z_part_domain_len))-z_array[i])**2)**(0.5*(dim-1))
                    
                # elif (abs(abs(particles[j,4]+abs(z_part_domain_len))-z_array[i]) <= Dp/2): # Periodic
                    
                #     area[i] = area[i] + ((np.pi)**(dim-2))*((Dp/2)**2-((particles[j,4]+abs(z_part_domain_len))-z_array[i])**2)**(0.5*(dim-1))                
    

    # Computing the area fraction
    area_frac = np.zeros(len(area))
    for i in range(len(area)):
        if direction == 1:
            area_frac[i] = (area[i]/(abs(y_part_domain_len)*abs(z_part_domain_len**(dim-2))))*100 
        elif direction == 2:
            area_frac[i] = (area[i]/(abs(x_part_domain_len)*abs(z_part_domain_len**(dim-2))))*100 
        elif direction == 3:
            area_frac[i] = (area[i]/(abs(x_part_domain_len)*abs(y_part_domain_len**(dim-2))))*100 
    


    mean_area_frac = area_frac.mean() 
    mean_plot = np.zeros((2,2))
    if direction == 1:
        mean_plot[0,0] = x_min
        mean_plot[1,0] = x_max
    elif direction ==2:
        mean_plot[0,0] = y_min
        mean_plot[1,0] = y_max
    elif direction ==3:
        mean_plot[0,0] = z_min
        mean_plot[1,0] = z_max
    
    mean_plot[:,1] = mean_area_frac

    print(mean_area_frac)
    fig = plt.figure()
    ax = plt.axes()
    
    if direction == 1:
        ax.set_xlabel('x')
    elif direction == 2:
        ax.set_xlabel('y')
    elif direction == 3:
        ax.set_xlabel('z')
        
    ax.set_ylabel('Particle area fraction')
    
    plt.rcParams.update({'font.size': 20})
    
    plt.plot(mean_plot[:,0], mean_plot[:,1],'k-', lw=3,label="Mean area fraction")
    if direction == 1:
        plt.plot(x_array[:], area_frac[:],'r-', lw=2, label='Particle area fraction (x)') 
    elif direction ==2:
        plt.plot(y_array[:], area_frac[:],'r-', lw=2, label='Particle area fraction (y)') 
    elif direction ==3:
        plt.plot(z_array[:], area_frac[:],'r-', lw=2, label='Particle area fraction (z)') 
    
    legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
    #fig.set_size_inches(19.2,14.4)
    plt.show()
    #result = np.where(max_array == np.amax(max_array))