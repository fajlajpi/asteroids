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
PLAYER_FIRING_DELAY = 0.3  # in seconds
PLAYER_RADIUS = 30

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

LASER_SPEED = 450
LASER_RADIUS = 10
LASER_LIFESPAN = 2  # in seconds

ASTEROID_LARGE = 3
ASTEROID_MEDIUM = 2
ASTEROID_SMALL = 1
ASTEROID_FRAG = 0

ASTEROID_LARGE_SPEED = 100  # in pixels per second
ASTEROID_MEDIUM_SPEED = 200
ASTEROID_SMALL_SPEED = 300
ASTEROID_FRAG_SPEED = 500

ASTEROID_LARGE_ROTATION_SPEED = 1  # in rads per second
ASTEROID_MEDIUM_ROTATION_SPEED = 2
ASTEROID_SMALL_ROTATION_SPEED = 3
ASTEROID_FRAG_ROTATION_SPEED = 6

ASTEROID_LARGE_RADIUS = 45  # in pixels
ASTEROID_MEDIUM_RADIUS = 20
ASTEROID_SMALL_RADIUS = 10
ASTEROID_FRAG_RADIUS = 5

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
IMAGES_ASTEROIDS_MEDIUM=[
    "gfx\meteorGrey_med1.png",
    "gfx\meteorGrey_med2.png",
    ]
IMAGES_ASTEROIDS_SMALL=[
    "gfx\meteorGrey_small1.png",
    "gfx\meteorGrey_small2.png",
    ]
IMAGES_ASTEROIDS_FRAG=[
    "gfx\meteorGrey_tiny1.png",
    "gfx\meteorGrey_tiny2.png",
    ]
IMAGES_LASERS=[
    "gfx\laserRed01.png",
    ]
    
IMAGES_BACKGROUND=[
    "gfx/purple.png",
    "gfx/darkPurple.png",
    "gfx/blue.png",
    "gfx/black.png",
    ]

### Global variables to keep various necessary data
### Such as all game objects, sprites, or keypresses
objects = list()
keys = set()
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(width = WINDOW_WIDTH, height = WINDOW_HEIGHT)

### PREPARE Background Sprites and Batch
bg_batch = pyglet.graphics.Batch()
_bg_sprites_list = []
_bg_sprite_img = pyglet.image.load(random.choice(IMAGES_BACKGROUND))
_bg_sprite_width = _bg_sprite_img.width
_bg_sprite_height = _bg_sprite_img.height
_bg_x_tiles = (WINDOW_WIDTH // _bg_sprite_width) + 1
_bg_y_tiles = (WINDOW_HEIGHT // _bg_sprite_height) + 1

for x_tile in range(_bg_x_tiles):
    _bg_sprites_list.append(list())
    for y_tile in range(_bg_y_tiles):
        _bg_sprites_list[x_tile].append(pyglet.sprite.Sprite(_bg_sprite_img, batch=bg_batch))
        _bg_sprites_list[x_tile][y_tile].x = _bg_sprite_width * x_tile
        _bg_sprites_list[x_tile][y_tile].y = _bg_sprite_height * y_tile
        print(f"Added a tile at x: {x_tile}, y: {y_tile}")



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
        
    def draw_circle(self, x, y, radius):
        iterations = 20
        s = math.sin(2*math.pi / iterations)
        c = math.cos(2*math.pi / iterations)

        dx, dy = radius, 0

        gl.glBegin(gl.GL_LINE_STRIP)
        for i in range(iterations+1):
            gl.glVertex2f(x+dx, y+dy)
            dx, dy = (dx*c - dy*s), (dy*c + dx*s)
        gl.glEnd()
        
    def hit_by_spaceship(self, other):
        
        return None
        
    def hit_by_laser(self, other):
        
        return None
        
    def delete(self):
        _object_index = objects.index(self)
        objects.pop(_object_index)
        self.sprite.delete()
        pyglet.clock.unschedule(self.tick)
        print("Poof!")
        

class Spaceship(Spaceobject):
    def __init__(self, x, y, rot, spr):
        super().__init__(x, y, rot, spr)
        
        self.radius = PLAYER_RADIUS
        
        self.laser_timer = PLAYER_FIRING_DELAY
        
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
        
        ### COLLISION CHECKING ###
        
        for obj in objects:
            if obj != self:
                if overlaps(self, obj) == True:
                    obj.hit_by_spaceship(self)
                    
        ### SHOOTING ###
        
        if "space" in keys:
            if self.laser_timer < 0:
                self.laser_timer = PLAYER_FIRING_DELAY
                print("PEW!")
                Laser(self.x, self.y, self.rotation, IMAGES_LASERS[0])
        self.laser_timer -= 1 * dt
        
        return None
 
class Asteroid(Spaceobject):
    def __init__(self, size=ASTEROID_LARGE, x=-1, y=-1, direction=-1):
        if x == -1:
            if random.randint(1, 2) == 1:
                _init_x = 0
                _init_y = random.randint(0, WINDOW_HEIGHT)
            else:
                _init_y = 0
                _init_x = random.randint(0, WINDOW_WIDTH)
        else:
            _init_x = x
            _init_y = y
            
        _init_rot = random.random() * 3
        
        if size == ASTEROID_LARGE:
            _spr = random.choice(IMAGES_ASTEROIDS_LARGE)
            self.asteroid_movement_speed = ASTEROID_LARGE_SPEED
            self.radius = ASTEROID_LARGE_RADIUS
            self.asteroid_size = 3  # 3 is LARGE, 2 is MEDIUM, 1 is SMALL, 0 is FRAGS
        elif size == ASTEROID_MEDIUM:
            _spr = random.choice(IMAGES_ASTEROIDS_MEDIUM)
            self.asteroid_movement_speed = ASTEROID_MEDIUM_SPEED
            self.radius = ASTEROID_MEDIUM_RADIUS
            self.asteroid_size = 2
        elif size == ASTEROID_SMALL:
            _spr = random.choice(IMAGES_ASTEROIDS_SMALL)
            self.asteroid_movement_speed = ASTEROID_SMALL_SPEED
            self.radius = ASTEROID_SMALL_RADIUS
            self.asteroid_size = 1
        
        super().__init__(_init_x, _init_y, _init_rot, _spr)
        
        
        self.rotation_direction = random.choice([-1, 1])
        if direction == -1:
            _random_direction_degrees = random.randint(0, 360)
            _random_direction_rads = math.radians(_random_direction_degrees)
            self.rotation = _random_direction_rads
            
            self.asteroid_movement_direction = math.radians(random.randint(0,360))
        else:
            self.asteroid_movement_direction = direction

    def tick(self, dt):
        ### ROTATION OF THE ASTEROID ###
        _rotation_speed = ASTEROID_LARGE_ROTATION_SPEED
        self.rotation = self.rotation + dt * _rotation_speed * self.rotation_direction
        
        ### MOVEMENT OF THE ASTEROID ###
        self.x_speed = self.asteroid_movement_speed * math.cos(self.asteroid_movement_direction)
        self.y_speed = self.asteroid_movement_speed * math.sin(self.asteroid_movement_direction)
        
        super().tick(dt)
        
    def hit_by_spaceship(self, other):
        print("Boop!")
        other.delete()
        
    def hit_by_laser(self, other):
        print("Kaboom!")
        
        _hit_x = self.x
        _hit_y = self.y
        _laser_rotation = other.rotation
        
        if self.asteroid_size == ASTEROID_LARGE:
            for count in range(2):
                _new_asteroid_direction = _laser_rotation + random.randint(-90, 90)
                _new_asteroid = Asteroid(ASTEROID_MEDIUM, _hit_x, _hit_y, _new_asteroid_direction)
        if self.asteroid_size == ASTEROID_MEDIUM:
            for count in range(2):
                _new_asteroid_direction = _laser_rotation + random.randint(-90, 90)
                Asteroid(ASTEROID_SMALL, _hit_x, _hit_y, _new_asteroid_direction)
            
        self.delete()
        other.delete()

class Laser(Spaceobject):
    def __init__(self, x, y, rot, spr):
        super().__init__(x, y, rot, spr)
        
        self.speed = LASER_SPEED
        self.radius = LASER_RADIUS
        self.lifespan = LASER_LIFESPAN
    
    def tick(self, dt):
        ### MOVEMENT OF THE LASER BEAM ###
        self.x_speed = self.speed * math.cos(self.rotation)
        self.y_speed = self.speed * math.sin(self.rotation)
        
        super().tick(dt)
        
        for obj in objects:
            if obj != self:
                if overlaps(self, obj) == True:
                    obj.hit_by_laser(self)
        
        if self.lifespan < 0:
            self.delete()
        self.lifespan -= 1 * dt

def draw():
    """ Funkce na vykreslování """
    window.clear()
    
    

    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            # Remember the current state
            gl.glPushMatrix()
            # Move everything drawn from now on by (x_offset, y_offset, 0)
            gl.glTranslatef(x_offset, y_offset, 0)

            # Draw a background image
            bg_batch.draw()
            
            # Draw a circle under each gameobject
            for obj in objects:
                obj.draw_circle(obj.x, obj.y, obj.radius)

            # Draw main sprite batch
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
    if symbol == key.SPACE:
        keys.add("space")
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
    if symbol == key.SPACE:
        keys.discard("space")
    return None
    
def clamp (hodnota, minimum, maximum):
    return max(minimum, min(hodnota, maximum))

def distance(a, b, wrap_size):
    """Distance in one direction (x or y)"""
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result

def overlaps(a, b):
    """Returns true if two space objects overlap"""
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared

def init_game():
    global window
    
    window.push_handlers(
    on_draw = draw,
    on_key_press = key_press_handler,
    on_key_release = key_release_handler
    )
    
    ### Create 1 spaceship object
    Spaceship(window.width // 2, window.height // 2, 0, IMAGES_PLAYER["player_ship"])
    
    for _ in range(2):
        Asteroid(ASTEROID_LARGE)
        
    return None

### GAME INIT ###
init_game()

### MAIN LOOP ###
pyglet.app.run()
