from PIL import Image
import itertools  #For different gold state
import numpy as np
import random

im = Image.open("mining_map.png")


class map:
    def __init__(self):
        pix = im.load()
        #max width of the cave
        self.width=im.width-1
        self.height=im.height-1
        #current position
        self.x_c=0
        self.y_c=0
        #actions for each state
        self.direction = [0,1,2,3]
        self.Goldlist={}
        self.imlist=[[0 for k in range(im.width)] for k in range(im.height)]

        for x in range (0,im.width):
            for y in range (0,im.height):
                if pix[x,y]==(255,102,0,255) or pix[x,y]==(255,255,0,255):
                    now=(x,y)
                    self.Goldlist[now]=True

        l = [False, True]
        self.Qtable=dict.fromkeys(itertools.product(l, repeat=len(self.Goldlist)))

        self.imlist=[[0 for k in range(im.width)] for k in range(im.height)]

        for x in range(0,(im.width)): #look for the position
            for y in range(0,(im.height)):
                self.imlist[x][y]=pix[x,y]

        self.Qtable={x:(np.zeros((im.width*im.height,len(self.direction))).tolist()) for x in self.Qtable}




    def whichq(self,G_table):
        l = [False, True]
        D_table=list(itertools.product(l, repeat=len(self.Goldlist)))

        goldstate=D_table[G_table]

        Qtablen=self.Qtable.get(goldstate)
        return Qtablen




    def reset(self,whatstate):

        keys_list = list(self.Qtable)
        key = keys_list[whatstate]
        q=0
        for i in self.Goldlist:
            self.Goldlist[i]=key[q]
            q=q+1

        self.x_c=0
        self.y_c=0
        accumulate=0
        Done=False
        location=(self.x_c,self.y_c)
        self.state= self.width * self.y_c + self.x_c
        return self.Goldlist,accumulate,Done,location,self.state



    def randomdirection(self):
        Valid=False
        while Valid==False:
            newmove=random.randrange(0,4)

            if newmove==0 and self.y_c!=0:
                Valid=True
            if newmove==1 and self.x_c!=(im.width-1):
                Valid=True
            if newmove==2 and self.y_c!=(im.height-1):
                Valid=True
            if newmove==3 and self.x_c!=0:
                Valid=True

        return newmove

    def store(self,qtable):
        Goldstate=tuple(self.Goldlist.values())
        self.Qtable[tuple(Goldstate)]=qtable

    def move(self,direction,accumulate):


        state = ((self.width+1)*(self.y_c)+self.x_c)

        if direction == 0: # up
            self.y_c=self.y_c-1
        if direction == 1: # right
            self.x_c=self.x_c+1
        if direction == 2: # down
            self.y_c=self.y_c+1
        if direction == 3: # left
            self.x_c=self.x_c-1

        Done=(self.Goldlist=={x:False for x in self.Goldlist})

        #Red Cave
        if self.imlist[self.x_c][self.y_c]==(153, 0, 0, 255):
            reward=-1
            prob=0.10

        #Black Roads
        if self.imlist[self.x_c][self.y_c]==(0, 0, 0, 255):
            reward=-1
            prob=0.01

        #Yellow Gold Mine
        if self.imlist[self.x_c][self.y_c]==(255, 255, 0, 255)and self.Goldlist[tuple((self.x_c,self.y_c))]==True:
            reward=100
            prob=0.90
            location=tuple((self.x_c,self.y_c))
            self.Goldlist[location]=False

        elif self.imlist[self.x_c][self.y_c]==(255, 255, 0, 255)and self.Goldlist[tuple((self.x_c,self.y_c))]==False:
            reward=0
            prob=0.90
            location=tuple((self.x_c,self.y_c))
            self.Goldlist[location]=False

        #Orange Gold Mine
        if self.imlist[self.x_c][self.y_c]==(255, 102, 0, 255) and self.Goldlist[tuple((self.x_c,self.y_c))]==True :
            reward=10
            prob=0.95
            location=tuple((self.x_c,self.y_c))
            self.Goldlist[location]=False

        elif self.imlist[self.x_c][self.y_c]==(255, 102, 0, 255)and self.Goldlist[tuple((self.x_c,self.y_c))]==False:
            reward=0
            prob=0.90
            location=tuple((self.x_c,self.y_c))
            self.Goldlist[location]=False



        nextstate = ((self.width+1)*(self.y_c)+self.x_c)
        accumulate=accumulate+reward


        return Done,(reward*prob),nextstate,accumulate,state

