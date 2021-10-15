from library import map
import itertools
import pickle

map=map()

#training specifications
timesoftraining = 50
gamma = 0.9


l = [False, True]
gold=list(itertools.product(l, repeat=len(map.Goldlist)))

#iterate through each possible list of gold availability
for j in range (0, len(map.Qtable)):

    for i in range(timesoftraining):

        #fetch Q-table according to gold state
        k=tuple(map.whichq(j))
        Goldlist,accumulate,Done,location,state=map.reset(j)

        while Done==False:

            #add logic between random and choose max later.
            direction=map.randomdirection()

            #the movement
            Done,R_P,nextstate,accumulate,state=map.move(direction,accumulate)

            #check the list of gold availibility
            Goldstate=tuple(map.Goldlist.values())

            #Bellman equations
            k[int(state)][direction] = R_P + gamma * max(k[nextstate])

            state=nextstate

q = map.Qtable
filename = "Dict"+str(timesoftraining)+".pk"
with open(filename, 'wb')as fi:
    pickle.dump(q, fi)
fi.close()
