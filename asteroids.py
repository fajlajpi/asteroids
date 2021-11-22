import pyglet
from pyglet import gl
from pyglet.window import key
import random
import math

### CONSTANTS for tweaking game behavior
### Such as numbers of enemies, speeds, health, etc.
PLAYER_SPEED = 5
PLAYER_ROTATION_SPEED = 3  # in rads per second
PLAYER_ACCELERATION = 300 # in pixels per second per second
PLAYER_MAX_SPEED = 300
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

ASTEROID_LARGE_SPEED = 100
ASTEROID_MEDIUM_SPEED = 200
ASTEROID_SMALL_SPEED = 300
ASTEROID_FRAG_SPEED = 500

ASTEROID_LARGE_ROTATION_SPEED = 1
ASTEROID_MEDIUM_ROTATION_SPEED = 3
ASTEROID_SMALL_ROTATION_SPEED = 4
ASTEROID_FRAG_ROTATION_SPEED = 6

### Dictionary to store filenames of sprites used for objects
IMAGES_PLAYER={
    "player_ship": "gfx\ship_red.png",
    }
IMAGES_ASTEROIDS_LARGE=[
    "gfx\meteorGrey_big1.png",
    "gfx\meteorGrey_big2.png",
    "gfx\meteorGrey_big3.png",
    "gfx\meteorGrey_big4.png",
    ]

### Global variables to keep various necessary data
### Such as all game objects, sprites, or keypresses
objects = list()
keys = set()
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(width = WINDOW_WIDTH, height = WINDOW_HEIGHT)

class Spaceobject:
    def __init__(self, x, y, rot, spr):
        global batch
        global objects
        
        self.x = x
        self.y = y
        self.rotation = rot
        
        self.x_speed = 0
        self.y_speed = 0
        
        _spr_centered = pyglet.image.load(spr)
        _spr_centered.anchor_x = _spr_centered.width // 2
        _spr_centered.anchor_y = _spr_centered.height // 2
        self.sprite = pyglet.sprite.Sprite(_spr_centered, batch=batch)
        
        objects.append(self)  # adds self to our object list
        
        pyglet.clock.schedule(self.tick)  # schedules own tick function to pyglet
    
    def tick(self, dt):
        ### MAKE SURE TO PUT MOVEMENT LOGIC IN CHILD CLASSES ###
        
        ### MOVEMENT of the Specobject
        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed
                
        ### Push the new values (x, y, rotation) to our sprite
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = 90 - math.degrees(self.rotation)
        
        ### EDGE WRAPPING ###
        if self.x < 0:
            self.x = window.width
        if self.x > window.width:
            self.x = 0
        if self.y < 0:
            self.y = window.height
        if self.y > window.height:
            self.y = 0
            
        return None

class Spaceship(Spaceobject):
    def tick(self, dt):
        """ mechanika lodi """
        
        ### ROTATION OF THE SHIP ###
        _rotation_speed = PLAYER_ROTATION_SPEED
        _rotation_direction = 0
        _rotation_left = 0
        _rotation_right = 0
        
        # set axes based on key presses and releases
        if "left" in keys:
            _rotation_left = 1
        else:
            _rotation_left = 0
        if "right" in keys:
            _rotation_right = -1
        else:
            _rotation_right = 0
        
            
        _rotation_direction = _rotation_left + _rotation_right  # combine the axes
        _rotation_speed = _rotation_speed * _rotation_direction
        
        self.rotation = self.rotation + dt * _rotation_speed
        
        ### ACCELERATION OF THE SHIP ###
        _acceleration = 0
        # set acceleration axis based on key press
        if "up" in keys:
            _acceleration = PLAYER_ACCELERATION * 1
        else:
            _acceleration = PLAYER_ACCELERATION * 0
            
        self.x_speed += dt * _acceleration * math.cos(self.rotation)
        self.y_speed += dt * _acceleration * math.sin(self.rotation)
        
        ### TOP SPEED CLAMPING ###
        _total_speed = math.sqrt(self.x_speed**2 + self.y_speed**2)
        if _total_speed > PLAYER_MAX_SPEED:
            _ratio = PLAYER_MAX_SPEED / _total_speed
            self.x_speed = self.x_speed * _ratio
            self.y_speed = self.y_speed * _ratio
            
        
        super().tick(dt)
        
        return None
 
class Asteroid(Spaceobject):
    def __init__(self, spr):
        if random.randint(1, 2) == 1:
            _init_x = 0
            _init_y = random.randint(0, WINDOW_HEIGHT)
        else:
            _init_y = 0
            _init_x = random.randint(0, WINDOW_WIDTH)
        _init_rot = random.random() * 3
        
        
        super().__init__(_init_x, _init_y, _init_rot, spr)
        
        _random_direction_degrees = random.randint(0, 360)
        _random_direction_rads = math.radians(_random_direction_degrees)
        self.rotation = _random_direction_rads
        self.rotation_direction = random.choice([-1, 1])
        
        self.asteroid_movement_direction = math.radians(random.randint(0,360))
        self.asteroid_movement_speed = ASTEROID_LARGE_SPEED
        
    def tick(self, dt):
        ### ROTATION OF THE ASTEROID ###
        _rotation_speed = ASTEROID_LARGE_ROTATION_SPEED
        self.rotation = self.rotation + dt * _rotation_speed * self.rotation_direction
        
        ### MOVEMENT OF THE ASTEROID ###
        self.x_speed = self.asteroid_movement_speed * math.cos(self.asteroid_movement_direction)
        self.y_speed = self.asteroid_movement_speed * math.sin(self.asteroid_movement_direction)
        
        super().tick(dt)

def draw():
    """ Funkce na vykreslování """
    window.clear()

    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            # Remember the current state
            gl.glPushMatrix()
            # Move everything drawn from now on by (x_offset, y_offset, 0)
            gl.glTranslatef(x_offset, y_offset, 0)

            # Draw
            batch.draw()

            # Restore remembered state (this cancels the glTranslatef)
            gl.glPopMatrix()
    return None
    
def key_press_handler(symbol, modifiers):
    """ Funkce na stisknutí kláves """
    if symbol == key.LEFT:
        keys.add("left")
    if symbol == key.RIGHT:
        keys.add("right")
    if symbol == key.UP:
        keys.add("up")
    if symbol == key.DOWN:
        keys.add("down")
    return None

def key_release_handler(symbol, modifiers):
    """ Funkce na pouštění kláves """
    if symbol == key.LEFT:
        keys.discard("left")
    if symbol == key.RIGHT:
        keys.discard("right")
    if symbol == key.UP:
        keys.discard("up")
    if symbol == key.DOWN:
        keys.discard("down")
    return None
    
def clamp (hodnota, minimum, maximum):
    return max(minimum, min(hodnota, maximum))

def init_game():
    global window
    
    window.push_handlers(
    on_draw = draw,
    on_key_press = key_press_handler,
    on_key_release = key_release_handler
    )
    
    ### Create 1 spaceship object
    Spaceship(window.width // 2, window.height // 2, 0, IMAGES_PLAYER["player_ship"])
    
    for _ in range(3):
        Asteroid(random.choice(IMAGES_ASTEROIDS_LARGE))
        
    return None

### GAME INIT ###
init_game()

### MAIN LOOP ###
pyglet.app.run()
