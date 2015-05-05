'''
A generic structure of a markov Problem.
'''
class MProblem:
    #Returns the possible actions
    def actions(self):
        pass
    #Returns the possible states after applying an action
    def applyAction(self, s1, a):
        pass
    #Returns the probability of getting to s2 after applying a to s1
    def transitionProb(self, s1, a, s2):
        pass
    #Returns the reward of a given state
    def reward(self, s):
        pass
    def value(self, s, new=None):
        pass
    #Returns the non-absorbing states
    def states():
        pass

'''
A Maze loaded from CSV that holds info for a MDP problem
The state is the position (x, y) of the cursor.
'''
class MazeCSV (MProblem):
    def __init__(self, url, strline = False, absorbent = 100):
        #Set absorbent
        self.absorbent = absorbent
        #Load CSV
        if not strline:
            f = open(url, 'r')
            rawline = f.readline().split(",")
            f.close()
        else:
            rawline = url.split(",")
        #Read rows and cols count
        rows = int(rawline[0].strip())
        cols = int(rawline[1].strip())
        #Read probabilities for actions
        self.distribution = float(rawline[2].strip()), float(rawline[3].strip()), float(rawline[4].strip())
        #Error
        if sum(self.distribution) != 1.0:
            print("Probabilities must sum 1.0")
            return
        #Build the map
        maze = []
        #For each item, form map
        for i in range(rows):
            row = []
            for j in range(cols):
                item = rawline[5 + i * cols + j].strip()
                if item != 'x':
                    cost = int(item)
                    if abs(cost) == self.absorbent:
                        row.append({'val' :  cost, 'reward' : cost})
                    else:
                        row.append({'val' :  0, 'reward' : -1*cost})
                        
                else:
                    row.append({'val' : None})
            maze.append(row)
#        print(maze)
        self.maze = maze
        self.actionsDesc = {
            "up" : ["up", "right", "left"],
            "down" : ["down", "right", "left"],
            "left" : ["left", "up", "bottom"],
            "right" : ["right", "bottom", "up"]
        }
    
    #Returns the state after moving with an action a
    def move(self, s1, a):
        y, x = s1
        res = s1
        if a == 'up':
            if y > 0 and self.maze[y-1][x]['val'] != None:
                res = (y-1, x)
        elif a == 'down':
            if y < len(self.maze)-1 and self.maze[y+1][x]['val'] != None:
                res = (y+1, x)
        elif a == 'left':
            if x > 0 and self.maze[y][x-1]['val'] != None:
                res = (y, x-1)
        elif a == 'right':
            if x < len(self.maze[0])-1 and self.maze[y][x+1]['val'] != None:
                res = (y, x+1)
        return res
    
    #Return the possible actions
    def actions(self):
        return self.actionsDesc.keys()
    
    #Returns the possible states after applying an action
    def applyAction(self, s1, a):
        if a in self.actionsDesc:
            res = {}
            #For each possible action ac from action a
            for i in range(len(self.actionsDesc[a])):
                ac = self.actionsDesc[a][i]
                res[ac] = {'state' : self.move(s1, ac), 'prob' : self.distribution[i]}
            return res

    #Returns the probability of getting to s2 after applying a to s1
    def transitionProb(self, s1, a, s2):
        possibles = self.applyAction(s1, a)
        res = 0.0
        for p in possibles:
            poss = possibles[p]
            if poss['state'] == s2:
                res += poss['prob']
        return res
    
    def reward(self, s1):
        y, x = s1
        return self.maze[y][x]['reward']
    
    def value(self, s1, val=None):
        y, x = s1
        if not val:
            return self.maze[y][x]['val']
        else:
            self.maze[y][x]['val'] = val
    
    def printMap(self):
        for row in self.maze:
            line = ""
            for item in row:
                line += str(item['val']) + "\t"
            print(line)
            
    #Returns the non-absorbing states
    def states(self):
        res = []
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.maze[y][x]['val'] != None and abs(self.maze[y][x]['val']) != self.absorbent:
                    res.append((y, x))
        return res
    #Prints the policies to a CSV
    def toCSV(self, url):
        if not self.policy:
            raise Exception("No policy defined for this problem")
        else:
            res = "%s, %s, %s, %s, %s" % (len(self.maze), len(self.maze[0]), self.distribution[0], self.distribution[1], self.distribution[2])
            print(self.policy)
            for y in range(len(self.maze)):
                for x in range(len(self.maze[0])):
                    if self.maze[y][x]['val'] == None:
                        res += ", x"
                    elif abs(self.maze[y][x]['val']) == self.absorbent:
                        res += ", %s" % self.maze[y][x]['val']
                    else:
                        res += ", %s" % self.policy[(y, x)]
            with open(url, 'w') as f:
                f.write(res)
    #Maps everything to a dictionary for external usage
    def toDict(self):
        import copy
        data = copy.deepcopy(self.maze)
        for y in range(len(data)):
            for x in range(len(data[0])):
                if 'reward' in data[y][x]:
                    del data[y][x]['reward']
                if (y, x) in self.policy:
                    data[y][x]['policy'] = self.policy[(y, x)]
        return data
            
                                          
if __name__ == '__main__':
    m = MazeCSV('maps/sample1.csv')
    m.applyAction((0, 0), 'up')
    trm.transitionProb((0,0), 'up', (5,5))
    m.printMap()
#    print(m.move((4, 1), 'up'))
#    print(m.move((4, 1), 'down'))
#    print(m.move((4, 1), 'left'))
#    print(m.move((4, 1), 'right'))