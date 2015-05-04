class MDPSolver:
    def __init__(self, mproblem, gamma = 1.0, delta = 1):
        self.problem = mproblem
        self.gamma = gamma
        self.delta = 0.5
        self.policy = {}
    #Calculates values and determines policies with an iterative process.
    #Also decorates mproblem with a policy dictionary
    def calculateValues(self):
        changes = 1
        #Use a shortcut
        p = self.problem
        #While there are changes in value calculations
        while changes > 0:
            changes = 0
            print("----------")
            #Iterate every possible state
            for state in p.states():
                #Apply all possible actions (keep track of the max)
                maxval = float('-inf')
                maxac = None
                for action in p.actions():
                    #Formula
                    poss = p.applyAction(state, action)
                    results = self.gamma * sum(poss[r]['prob']*p.value(poss[r]['state']) for r in poss) + p.reward(state)
                    if results > maxval:
                        maxval = results
                        maxac = action
                #If it's different
                if abs(p.value(state) - maxval) > self.delta:
                    p.value(state, maxval)
                    self.policy[state] = maxac
                    changes += 1
        p.policy = self.policy
    
        

if __name__ == '__main__':
    from maze import MazeCSV
    
    m = MazeCSV('maps/sample0.csv')
    m.printMap()
    solver = MDPSolver(m)
    solver.calculateValues()
    m.printMap()
    m.toDict()