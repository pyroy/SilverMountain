import pygame, random
import essentials.classes as classes
from modules.MODULE import module_master

def get_cells_around(cell, map_limit_x, map_limit_y):
    counter = cell[1]
    cell = cell[0]
    
    ret = []
    
    if cell[0] - 1 >= 0:
        ret.append( ((cell[0] - 1, cell[1]), counter + 1) )
        
    if cell[0] + 1 <= map_limit_x:
        ret.append( ((cell[0] + 1, cell[1]), counter + 1) )
        
    if cell[1] - 1 >= 0:
        ret.append( ((cell[0], cell[1] - 1), counter + 1) )
        
    if cell[1] + 1 <= map_limit_y:
        ret.append( ((cell[0], cell[1] + 1), counter + 1) )
        
    return ret
    
def get_all_counter(paths, origin, counter):
    return [p for p in paths if p[1] == counter and (origin == None or origin in get_cells_around(p, 10000, 10000))]
    
def remove_higher_counter(paths, counter):
    return [p for p in paths if p[1] < counter]

def path_algorithm(start, stop, walls, map_limit_x, map_limit_y, iteration_max=100):

    #PLEASE do not cry when reading this.
    #this is the wikipedia "sample algorithm" found on the pathfinding page

    paths = [(start,0)]
    iterations = 0

    while iterations < iteration_max:
        
        try: current_cell = paths[iterations]
        except: return None
        new_cells = get_cells_around( current_cell, map_limit_x, map_limit_y )
        for new_cell in new_cells:
              
            if walls.boundmap[new_cell[0][1]][new_cell[0][0]] == 0:
            
                already_in_list = False
                for cell in paths:
                    if cell[0][0] == new_cell[0][0] and cell[0][1] == new_cell[0][1] and cell[1] <= new_cell[1]:
                        already_in_list = True
                        break
                        
                if not already_in_list:
                    paths.append( new_cell )
                    
                    #when goal reached
                    if new_cell[0][0] == stop[0] and new_cell[0][1] == stop[1]:
                        final_path = []
                        cur = new_cell[1]
                        origin = None
                        g = [ new_cell ]
                        while g != []:
                            origin = random.choice(g)
                            final_path.append( origin )
                            paths = remove_higher_counter(paths, cur)
                            cur -= 1
                            g = get_all_counter(paths, origin, cur)

                        return final_path[::-1]
                        
        iterations += 1
        
class Pathfinder:
    def __init__(self, player):
        self.map = None
        self.destination = None
        self.pc = player
        self.move_performed = True
        self.precision = 0
        self.target_x = 0
        self.target_y = 0
        self.is_hijacking = False
        self.is_done = False
        self.set_path = None
        self.path_index = 0
        
    def set_goal(self, map, destination):
        self.map = map
        self.destination = destination
        
    def get_path(self, current_pos):
        self.path_index = 0
        self.set_path = path_algorithm( current_pos, self.destination, self.map, self.map.map_size[0], self.map.map_size[1] )
        
    def get_directions_from(self, current_pos):
        if self.set_path == None: 
            return None
        
        elif self.path_index >= len(self.set_path):
            return None
            
        else: 
            return (self.set_path[self.path_index][0][0] - current_pos[0], self.set_path[self.path_index][0][1] - current_pos[1])
            #return (path_get[1][0][0] - current_pos[0], path_get[1][0][1] - current_pos[1] )
        
    def perform_next_move(self, move, precision=1):
        self.pc.pathfinder.move_performed = False
        self.path_index += 1
        self.target_x = int((self.pc.x_position+8)//16)*16 + move[0]*16
        self.target_y = int((self.pc.y_position+8)//16)*16 + move[1]*16
        self.precision = precision
    
    def run_move_frame(self, dt):
    
        if self.target_x - self.pc.x_position > 1:
            self.pc.move(dt, [0, 0, 0, 1])
        elif self.target_x - self.pc.x_position < -1:
            self.pc.move(dt, [1, 0, 0, 0])
        if self.target_y - self.pc.y_position < -1:
            self.pc.move(dt, [0, 0, 1, 0])
        elif self.target_y - self.pc.y_position > 1:
            self.pc.move(dt, [0, 1, 0, 0])
            
        if abs(self.pc.x_position - self.target_x) < self.precision and abs(self.pc.y_position - self.target_y) < self.precision:
            self.move_performed = True

class module_head(module_master):
    def __init__(self):
        self.module_name = "Basegame::Pathfinding"
        self.next_move = None
        
    def setup(self, game_main, MODULES):
        self.pc = MODULES.get_module("Essential::Player").player_character
        self.pc.pathfinder = Pathfinder(self.pc) #this is disgusting
        
    def handle_keydown(self, event):
        if event.key == pygame.K_p:
            self.goto_goal()
        
    def set_goal(self, goal):
        self.pc.pathfinder.set_goal( self.pc.map, goal )
        self.pc.pathfinder.get_path( (int((self.pc.x_position+8)//16), int((self.pc.y_position+8)//16)) )
        self.next_move = self.pc.pathfinder.get_directions_from( (int((self.pc.x_position+8)//16), int((self.pc.y_position+8)//16)) )
        
    def goto_goal(self, precision=1):
        self.pc.pathfinder.is_done = False
        self.pc.pathfinder.is_hijacking = True
        self.precision = precision
        
    def stop(self):
        self.pc.pathfinder.is_hijacking = False
        self.pc.pathfinder.is_done = True
        
    def run_frame(self, game_main, MODULES):
    
        if self.pc.pathfinder.is_hijacking:
        
            if self.pc.pathfinder.move_performed:
            
                if self.next_move == None:
                    self.stop()
                    
                else:
                    self.next_move = self.pc.pathfinder.get_directions_from( (int((self.pc.x_position+8)//16), int((self.pc.y_position+8)//16)) )
            
            if self.next_move != None and self.pc.pathfinder.move_performed:
                self.pc.pathfinder.perform_next_move( self.next_move, self.precision )
                
            else: 
                self.pc.pathfinder.move_performed = False
                self.pc.pathfinder.run_move_frame(game_main.dt)