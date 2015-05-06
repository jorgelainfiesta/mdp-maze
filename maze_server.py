import os
import cherrypy
import cherrypy_cors

from mdp import MDPSolver 
from maze import MazeCSV 

class MazeServer(object):
    @cherrypy.expose
    def index(self):
        return "Request /solve passing the maze problem in a string"
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def solve(self, maze = None):
        if maze:
            #Build and solve Maze from raw line
            try:
                print(maze)
                m = MazeCSV(maze, True)
                solver = MDPSolver(m)
                solver.calculateValues()
                #Quick fix
                self.maze = m
#                cherrypy.session['maze'] = m
                return self.maze.toDict()
            except Exception:
                return {'error' : 'An error occurred while procesing the maze'}
        else:
            return {'error' : 'No map was sent'}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def move(self, y, x):
        if y and y.isdigit() and x and x.isdigit():
            m = self.maze
            return m.advanceToGoal((int(y), int(x)))
        else:
            return {'error' : 'No position was sent'}

server_ip = 'localhost'
server_port = 8080
PATH = os.path.abspath(os.path.dirname(__file__))
cherrypy_cors.install()
config = {
	'/': {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': PATH,
		'tools.staticdir.index': 'index.html',
		'cors.expose.on': True,
        'tools.sessions.on': True
	}
}

cherrypy.server.socket_host = server_ip
cherrypy.server.socket_port = server_port
	
if __name__ == '__main__':
	cherrypy.quickstart(MazeServer(), '/', config)