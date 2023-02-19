import matplotlib.animation as anim
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

on = 255
off = 0
#I'm setting ON = the pixel brightness value which will indicate ON as a shorthand
#so later it is easier to set pixels to the ON colour without confusion

possible_values = [on, off]
N = 150#side lengths of the grid
#initiate a grid
grid = np.random.choice(possible_values, N*N, p=[.05,.95]).reshape(N, N)
cgrid = np.zeros((N,N), dtype=int)
#^ makes a colour grid with values set to zero initially. (N,N) specifies it should be in the shape of a NxN grid
#dtype tells it that the grid will be storing integer values (as colour values range 0-255)
#makes a N x N long list of pixel values either set to On or Off in the proportion of 30% on to 70% off randomly
#it then reshapes this NxN long list of pixels into an array of NxN size which is essentially a square grid of dimensions NxN

#now to make a function to update the grid. this will be the rules governing the cells behaviour
rgrid = np.random.choice([1,2,3], N*N, p = [.9,.05,.05]).reshape(N, N)
ruleset = 1
def update(data):
    global grid
    global ruleset
    global cgrid
    newgrid = grid.copy()
    #copy a grid over to edit and check values from before updating to the current grid

    #go over every pixel and apply the rules on them to see what should happen
    #you will see usage of %N. this means if the program tries to check pixel x value 251 which we dont have, it will loop back
    #from the start and go back to pixel 0 instead of trying to check nonexistent pixel 251
    for x in range(N):
        for y in range(N):
            #setting the ruleset to be the current pixels ruleset referenced from the ruleset grid of the pixel's position
            #ruleset = rgrid[x,y]

            #colour mapping
            #colour = ON if the pixel is currently alive
            #colour = colour - 1 if the pixel is dead
            if grid[x,y] == on:
                cgrid[x,y]=255
            elif grid[x,y]== off and cgrid[x,y] > 0:
                cgrid[x,y]-=17

            #pixels surrounding the point x,y
            # [x-1,y+1] [x,y+1] [x+1,y+1]
            # [x-1, y ] [x , y] [x+1, y ]
            # [x-1,y-1] [x,y-1] [x+1,y-1]
            #we need to check all of these and add up how many were on etc.
            #keep in mind we dont take into account x,y
            total = (grid[(x-1)%N,(y+1)%N] + grid[x,(y+1)%N] + grid[(x+1)%N,(y+1)%N] + grid[(x-1)%N, y] + grid[(x+1)%N,y] + grid[(x-1)%N,(y-1)%N] + grid[x,(y-1)%N] + grid[(x+1)%N,(y-1)%N])/255
            #to see how many pixels had the value 255 = ON, we divide by 255 as each ON pixel adds on 255
            #now to apply Conrad's rules
            if ruleset == 1:
                if grid[x,y]==on:
                    if (total<2) or (total>3):
                        newgrid[x,y] = off
                        #rgrid[x,y]=2
                else:
                    if total == 3:
                        newgrid[x,y] = on
                        #rgrid[x,y]=3
            elif ruleset == 2:
                if grid[x,y]==on:
                    if (total<2) or (total>6):
                        newgrid[x,y] = off
                        #rgrid[x,y]=1
                else:
                    if total == 3 or total == 4:
                        newgrid[x,y] = on
                        #rgrid[x,y]=1
            elif ruleset == 3:
                if grid[x,y]==on:
                    if (total<2) or (total>4):
                        newgrid[x,y] = off
                        #rgrid[x,y]=1
                else:
                    if total == 3 or total == 4:
                        newgrid[x,y] = on
                        #rgrid[x,y]=1
    
    #now with the new updated grid copy, we need to transfer the data to the current grid and then repeat updates again
    mat.set_data(cgrid)
    grid = newgrid
    ruleset +=1
    if ruleset > 3:
        ruleset=1
    return [mat]

#setting up the animations
fig, ax = plt.subplots()
mat = ax.matshow(grid, cmap=matplotlib.cm.BuGn_r)
ani = anim.FuncAnimation(fig, update, interval = 5, frames=390, blit=True)
plt.axis('off')

#code to save the animation below:
fig.set_size_inches(11.25,11.25)
plt.rcParams['animation.ffmpeg_path'] = 'C:/FFmpeg/bin/ffmpeg'
writervideo = anim.FFMpegWriter(fps=13, bitrate=6000)

ani.save("wave17.mp4", writer=writervideo, dpi=300)
plt.close()
#plt.show()#