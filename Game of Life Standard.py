import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np

on = 255
off = 0
#I'm setting ON = the pixel brightness value which will indicate ON as a shorthand
#so later it is easier to set pixels to the ON colour without confusion

possible_values = [on, off]
N = 200#side lengths of the grid

#initiate a grid
grid = np.random.choice(possible_values, N*N, p=[.2,.8]).reshape(N, N)
#makes a N x N long list of pixel values either set to On or Off in the proportion of 30% on to 70% off randomly
#it then reshapes this NxN long list of pixels into an array of NxN size which is essentially a square grid of dimensions NxN

#now to make a function to update the grid. this will be the rules governing the cells behaviour

def update(data):
    global grid
    newgrid = grid.copy()
    #copy a grid over to edit and check values from before updating to the current grid

    #go over every pixel and apply the rules on them to see what should happen
    #you will see usage of %N. this means if the program tries to check pixel x value 251 which we dont have, it will loop back
    #from the start and go back to pixel 0 instead of trying to check nonexistent pixel 251
    for x in range(N):
        for y in range(N):
            #pixels surrounding the point x,y
            # [x-1,y+1] [x,y+1] [x+1,y+1]
            # [x-1, y ] [x , y] [x+1, y ]
            # [x-1,y-1] [x,y-1] [x+1,y-1]
            #we need to check all of these and add up how many were on etc.
            #keep in mind we dont take into account x,y
            total = (grid[(x-1)%N,(y+1)%N] + grid[x,(y+1)%N] + grid[(x+1)%N,(y+1)%N] + grid[(x-1)%N, y] + grid[(x+1)%N,y] + grid[(x-1)%N,(y-1)%N] + grid[x,(y-1)%N] + grid[(x+1)%N,(y-1)%N])/255
            #to see how many pixels had the value 255 = ON, we divide by 255 as each ON pixel adds on 255
            #now to apply Conrad's rules
            if grid[x,y]==on:
                if (total<2) or (total>3):
                    newgrid[x,y] = off
            else:
                if total == 3:
                    newgrid[x,y] = on
    
    #now with the new updated grid copy, we need to transfer the data to the current grid and then repeat updates again
    mat.set_data(newgrid)
    grid = newgrid
    return [mat]

#setting up the animations
fig, ax = plt.subplots()
mat = ax.matshow(grid)
ani = anim.FuncAnimation(fig, update, interval = 50, frames=500, blit=True)

#code to save the animation below:

# writervideo = anim.PillowWriter(fps=60)
# ani.save("niceSMALL.gif", writer=writervideo)
# plt.close()
plt.show()#