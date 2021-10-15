import pickle
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import copy

#read through open-cv
img = cv2.imread("mining_map.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#read through PIL
im = Image.open("mining_map.png")
pix = im.load()
Goldlist = {}
for x in range (0,im.width):
    for y in range (0,im.height):
        if pix[x,y]==(255,102,0,255) or pix[x,y]==(255,255,0,255):
            now=(x,y)
            Goldlist[now]=True

#open trained Q-table
filename = "Dict50.pk" #the filename is in the format of Dict(timesoftraining).pk
with open(filename, 'rb') as fi:
    d = pickle.load(fi)

#instantiate final path of the agent
path = {}

#instantiate results
x, y = 0, 0
reward = 0
result = []
prev_ind = 8

for i in range (100): #no more than 100 steps
    temp = copy.copy(img[y,x])
    img[y,x]=[255, 255, 255]

    #small animation for visualization
    plt.imshow(img)
    plt.show(block=False)
    plt.pause(0.6) #0.7 seconds between frames
    plt.close()

    img[y,x] = copy.copy(temp)

    #update agent's path
    coordinate = (y,x)
    path[coordinate]=[255, 255, 255]

    #add value in coordinate form
    result.append("("+str(x)+", "+str(y)+')')

    #prevents infinite looping
    if ((x,y) in Goldlist):
        Goldlist[(x,y)] = False
    booleans = tuple(Goldlist.values())
    ind = 10*y+x
    move_ind = d[booleans][ind].index(max(d[booleans][ind]))
    if (abs(move_ind-prev_ind)==2):
        maximum = d[booleans][ind][move_ind]
        min_diff = maximum
        second_index = -1
        for j in range (4):
            if (j==move_ind):
                continue
            diff = maximum - d[booleans][ind][j]
            if (diff<min_diff):
                min_diff = diff
                second_index = j
        move_ind = second_index

    #traceback action
    if (move_ind == 0):
        y = y - 1 #move up
    if (move_ind == 1):
        x = x + 1 #move right
    if (move_ind == 2):
        y = y + 1 #move down
    if (move_ind == 3):
        x = x - 1 #move left
    prev_ind = move_ind

    #update reward
    if (pix[x,y] == (153,0,0,255)):
        reward = reward - 1 * 0.1
    elif (pix[x,y] == (0,0,0,255)):
        reward = reward - 1 * 0.01
    elif (pix[x,y] == (255,102,0,255)):
        reward = reward + 10 * 0.95
    else:
        reward = reward + 100 * 0.90

    #terminate when all gold mines have been collected
    if (booleans == (False,False,False,False,False,False)):
        break

print(result)
print(path)
print("Final Reward: " + str(reward))

#shows the entire path of the agent
for i in path:
    img[i[0],i[1]]=path[i]
plt.imshow(img)
plt.show()