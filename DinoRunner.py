from tkinter import *
import time, random
from Obstacles import Obstacles
from Dino import Dino
import pygame

class DinoGame:
    
    #-------------------------------------------------------------------------
    # Initialization and Setup
    #-------------------------------------------------------------------------
    
    def __init__(self, root, nrow, ncol, scale):
        
        self.root = root
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
 
        #setter getter methods

        # initialize game state variables
        self.__game_over = False
        self.__pause = False
        self.__started = False
        
        # initialize game time variables
        self.__score = 0
        self.__pause_time = 0
        self.__next_spawn_time = self.__next_spawn_time = time.time() + random.uniform(1, 2)
        
        # initialize canvas w/ proper scale and color
        self.__canvas = Canvas(root, width=ncol*scale, height=nrow*scale, bg='black') 
        self.__canvas.pack()


        # create a start message for the game
        self.__start_msg = self.__canvas.create_text( 
            (ncol * scale) / 2, (nrow * scale) / 2,text="Hit 'S' to start game", font=('Times', 25))
        
        # define dino and obstacle classes
        self.__obstacles = [] #empty list to store obstacles
        self.__dino = Dino(self.__canvas, self.nrow//2 + 28, self.ncol - 100, self.scale) # positions dino in correct spot on canvas

        # Initialize sound effects
        pygame.init()
        pygame.mixer.init()
        self.jump_sound = pygame.mixer.Sound('/Users/timguilmette/Documents/ECE122_Project3/Code Template/jump_sound.mp3')
        self.game_over = pygame.mixer.Sound('/Users/timguilmette/Documents/ECE122_Project3/Code Template/game_over.mp3')
        self.start_sound = pygame.mixer.Sound('/Users/timguilmette/Documents/ECE122_Project3/Code Template/game_start.mp3')

        # bind keys to game reset function
        self.root.bind("<r>", lambda e: self.restart())

       #creates the score bar
        self.__score_text = self.__canvas.create_text( 
            self.scale * 10, self.scale * 2, 
            text="Score: 0", 
            font=('Times', 20), 
            anchor='w', 
            fill='white'
        )

        # In update_survival_score():
        self.__canvas.itemconfig(self.__score_text, text=f"Score: {self.__score}")                                       


    #-------------------------------------------------------------------------
    # Game State Methods
    #-------------------------------------------------------------------------
    
    def is_game_over(self):
        return self.__game_over
    
    
    def set_game_over(self, value):
        self.__game_over = value
    
        
    def is_pause(self):
        return self.__pause
    
    
    def set_pause(self, value):
        self.__pause = value
   
        
    def is_started(self):
        return self.__started
    
    
    def set_started(self, value):
        self.__started = value
      
        
    def get_next_spawn_time(self):
        return self.__next_spawn_time
    
    
    def set_next_spawn_time(self, value):
        self.__next_spawn_time = value
     
        
    def get_score(self):
        return self.__score
    
    
    def set_score(self, value):
        self.__score = value
    
        
    def get_pause_time(self):
        return self.__pause_time
    
    
    def set_pause_time(self, value):
        self.__pause_time = value
    
    #-------------------------------------------------------------------------
    # Game Logic
    #-------------------------------------------------------------------------
    
    def start_game(self):
        if not self.__game_over and not self.__started:
            # Start the game - delete message, set game state, and start timer
            self.__canvas.delete(self.__start_msg)
            self.__score = 0
            self.__started = True
            self.__start_time = time.time()
            self.__dino.activate()
            self.start_sound.play()
            print("Game started!")

            # Schedules the update_obstacles function to run every 50ms, creating a game loop for obstacle updates.
            # Helpful for the reset of the game as it allows the obsacles to be updated according the the game score/time
            self.root.after(50, update_obstacles, self, self.root)
        
    def next(self):
        # Checks if gave is active (not paused or over)
        if not self.__started or self.__pause or self.__game_over:
            return 

        # Get the current time
        current_time = time.time()

        # Check if it's time to spawn a new obstacle
        if current_time >= self.__next_spawn_time: 
            # Spawn a new obstacle and add it to the list
            new_obstacle = Obstacles.random_select(self.__canvas, self.nrow, self.ncol, self.scale)
            new_obstacle.activate()
            # Add the new obstacle to the list of obstacles
            self.__obstacles.append(new_obstacle)
            # Set the next spawn time to a random value between 1 and 2 seconds
            self.__next_spawn_time = current_time + random.uniform(1, 2) 

        # Iterate through the list of obstacles
        for obstacle in self.__obstacles[:]: 
            # Move the obstacle to the left
            obstacle.left() 
            # Check for collisions by overlapping pixels
            for dino_pixel in self.__dino.dino_pixels:
                for pixel in obstacle.pixels:
                    # Game over message on collision
                    if (dino_pixel.i == pixel.i and dino_pixel.j == pixel.j):
                        self.__canvas.create_text(self.ncol * self.scale / 2, self.nrow * self.scale / 2, text="GAME OVER", font=('Times', 30), fill='red')
                        self.game_over.play()
                        self.__game_over = True
                        return
                
            if obstacle.j + obstacle.w < 0:  #
                for pixel in obstacle.pixels:
                    pixel.delete()
                self.__obstacles.remove(obstacle)
                continue
        self.update_survival_score()

    
    def check_collision(self, obstacle): 
        for dino_pixel in self.__dino.dino_pixels: 
            for obs_pixel in obstacle.pixels:
                if dino_pixel.i == obs_pixel.i and dino_pixel.j == obs_pixel.j:
                    self.game_over.play()
                    return True  
        return False 
    

    def jump(self):
        # Jump if game is active, dino not already jumping, and not paused
        if self.__started and not self.__game_over and not self.__pause and not self.__dino.jumping: 
            self.__dino.jump()
            self.jump_sound.play()  # Play jump sound

    def pause(self):
        # Game must be active to pause
        if not self.__started: 
            return
        
        # Pause or resume the game
        if not self.__pause:
            self.__pause = True
            self.__pause_start = time.time() 
            print("Game paused")
        else:
            self.__pause = False
            pause_duration = time.time() - self.__pause_start #make up for paused game so timer is consitent
            self.__start_time += pause_duration
            print("Game resumed")


    def update_survival_score(self):
        # Update the score based on time survived
        if self.__started and not self.__pause and not self.__game_over:
            current_time = time.time()
            seconds_survived = int(current_time - self.__start_time)
            # Calculate the score based on survival time
            base_score = seconds_survived
            # Apply a bonus multiplier that increases every 30 seconds
            bonus_multiplier = 1.0 + (0.1 * (seconds_survived // 30)) 
            # Calculate final score
            self.__score = int(base_score * bonus_multiplier)
            # Update the score on the canvas
            self.__canvas.itemconfig(self.__score_text, text=f"Score: {self.__score}", fill = "white")
            

    def restart(self):
        # Clear the canvas
        self.__canvas.delete("all")

        # Clear the obstacles
        for obs in self.__obstacles:
            for pixel in obs.pixels:
                pixel.delete()
        self.__obstacles.clear()

        # Reset game state variables
        self.set_game_over(False)
        self.set_started(False)
        self.set_pause(False)
        self.set_score(0)
        self.set_pause_time(0)
        self.set_next_spawn_time(time.time() + random.uniform(1, 3))
        self.__start_time = time.time()

        # Recreate the canvas
        self.__start_msg = self.__canvas.create_text((self.ncol * self.scale) / 2, (self.nrow * self.scale) / 2, text="Hit 'S' to start game", font=('Times', 25))
        # Create score text on canvas 
        self.__score_text = self.__canvas.create_text(self.scale * 10, self.scale * 2, text="Score: 0", font=('Times', 20), anchor='w', fill='white')

    # Reactivate the same Dino object — DO NOT recreate it
    # Instead, just reset its internal pixels
        self.__dino = Dino(self.__canvas, self.nrow//2 + 28, self.ncol- 100, self.scale, game = self)
        print("Game reset. Press 'S' to start.")
        
#=============================================================================
# Main Game Runner - DO NOT MODIFY
#=============================================================================

def update_obstacles(game, root):
    if not game.is_pause() and (game.is_started() or game.is_game_over()):
        game.next()  # Unified method with feature flag
            
        if game.is_game_over():
            return  # Don't schedule another update if game is over
    
    # Schedule next update (50ms = 20 FPS)
    root.after(50, update_obstacles, game, root)

def main():
    """
    Main function to set up and run the game.
    """
    # Create the main window
    root = Tk()
    root.title("Dino Run Game")
    
    # Create the game instance
    game = DinoGame(root, nrow=80, ncol=160, scale=10)

    # Set up key bindings
    root.bind("<space>", lambda e: game.jump())
    root.bind("<p>", lambda e: game.pause())
    root.bind("<s>", lambda e: game.start_game())

    # Start the game loop
    root.after(10, update_obstacles, game, root)
    
    # Start Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()