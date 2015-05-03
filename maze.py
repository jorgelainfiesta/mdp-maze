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

'''
A Maze loaded from CSV that holds info for a MDP problem
The state is the position (x, y) of the cursor.
'''
class MazeCSV (MProblem):
    def __init__(self, url):
        #Load CSV
        f = open(url, 'r')
        rawline = f.readline().split(",")
        f.close()
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
                    row.append({'val' : 0, 'cost' : int(item)})
                else:
                    row.append({'val' : None})
            maze.append(row)
#        print(maze)
        self.maze = maze
        self.actions = {
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
    
    #Returns the possible states after applying an action
    def applyAction(self, s1, a):
        if a in self.actions:
            res = {}
            #For each possible action ac from action a
            for i in range(len(self.actions[a])):
                ac = self.actions[a][i]
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
    
    def printMap(self):
        for row in self.maze:
            line = ""
            for item in row:
                line += str(item['val']) + "\t"
            print(line)

if __name__ == '__main__':
    m = MazeCSV('maps/sample1.csv')
    m.applyAction((0, 0), 'up')
    m.transitionProb((0,0), 'up', (5,5))
    m.printMap()
#    print(m.move((4, 1), 'up'))
#    print(m.move((4, 1), 'down'))
#    print(m.move((4, 1), 'left'))
#    print(m.move((4, 1), 'right'))