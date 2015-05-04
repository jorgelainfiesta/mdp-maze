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
        if maze or True:
            #Build and solve Maze from raw line
            try:
#                m = MazeCSV(maze, True)
                m = MazeCSV('maps/sample0.csv')
                solver = MDPSolver(m)
                solver.calculateValues()
                return m.toDict()
            except Exception:
                return {'error' : 'An error occurred while procesing the maze'}
        else:
            return {'error' : 'No map was sent'}

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
	}
}

cherrypy.server.socket_host = server_ip
cherrypy.server.socket_port = server_port
	
if __name__ == '__main__':
	cherrypy.quickstart(MazeServer(), '/', config)