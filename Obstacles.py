from tkinter import *
from Pixel import Pixel
import random
import numpy as np


class Obstacles:
    def __init__(self, canv, nrow, ncol, scale, c = 2, pattern = None):
        self.canv = canv
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.c = c
        self.pattern = pattern
        self.pixels = []
        self.i = 0
        self.j = 0
        self.w = 0
        self.h = 0
        self._id = None
        self.paused = False
        
    
    def activate(self):
        if self.pattern is None:
            return  
        
        pattern_array = np.array(self.pattern) 
        self.h, self.w = pattern_array.shape
        self.i = self.nrow // 2 - self.h // 2  
        self.j = self.ncol - self.w  
        
        
        for row in range(self.h):  
            for col in range(self.w):  
                if pattern_array[row, col] != 0: 
                    new_pixel = Pixel(canv=self.canv, i=self.i + row, j=self.j + col, nrow=self.nrow, ncol=self.ncol, scale=self.scale, icolor=pattern_array[row, col], vector=[0,0])
                    self.pixels.append(new_pixel)


    def left(self):
        if self.paused:
            return
       
        self.j -= 1 
        
        for pixel in self.pixels:
            pixel.delete() 
            pixel.j -= 1 
            pixel.id = self.canv.create_rectangle(pixel.j * self.scale, pixel.i * self.scale, (pixel.j + 1) * self.scale, (pixel.i + 1) * self.scale, fill = Pixel.color[pixel.icolor], outline='black')
    
    @staticmethod
    def random_select(canv, nrow, ncol, scale):
        obstacle_choices = [Box, Tree, Pencil]
        obstacle_type = random.choice(obstacle_choices)
        return obstacle_type(canv, nrow, ncol, scale)
    
    


#=============================================================================
# All Child Classes
#=============================================================================

class Box(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        pattern = [
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2]
        ]
        super().__init__(canv, nrow, ncol, scale, c = 2, pattern = pattern)
        

class Tree(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        pattern = [
            [3, 3, 3],
            [3, 3, 3],
            [0, 3, 0]
        ]
        super().__init__(canv, nrow, ncol, scale, c = 3, pattern = pattern)
class Pencil(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        pattern = [
            [5, 0, 0, 0],
            [5, 0, 0, 0],
            [5, 0, 0, 0],
            [5, 0, 0, 0],
        ]
        super().__init__(canv, nrow, ncol, scale, c = 4, pattern = pattern)



#=============================================================================
# Testing Functions for Obstacles Class - DO NOT MODIFY
#=============================================================================

def delete_all(canvas):
    """Clear all elements from the canvas."""
    canvas.delete("all")
    print("Canvas cleared")


def test1(root, canvas, nrow, ncol, scale):
    print("\nPress left arrow key to move the obstacle left\n")
    obs = Obstacles.random_select(canvas, nrow, ncol, scale)
    obs.activate()

    def left():
        obs.left()  # Move the obstacle left

    root.bind("<Left>", lambda e: left())  # Bind left arrow key to move obstacle

def test2(root, canvas, nrow, ncol, scale):
    obstacle = None  # Only one obstacle active at a time
    paused = False   # Pause flag
    print("\nPress 'p' to pause/resume the obstacle movement\n")

    def toggle_pause(event=None):
        nonlocal paused
        paused = not paused
        print("Paused" if paused else "Resumed")

    # Bind the "p" key to toggle pause
    root.bind("<p>", toggle_pause)

    def update():
        nonlocal obstacle, paused
        if not paused:
            if obstacle is None:
                obstacle = Obstacles.random_select(canvas, nrow, ncol, scale)
                obstacle.activate()
            else:
                obstacle.left()  # Move the obstacle one step left using your updated left() method
                # Check if the obstacle is completely off-screen
                if obstacle.j + obstacle.w <= 0:  # Clear the canvas when the obstacle leaves
                    obstacle = None
                    
        # Schedule the next update after 20 milliseconds (adjust as needed)
        root.after(20, update)

    update()  # Start the update loop


def main():
    """
    Main function to set up and run the obstacle testing interface.
    """
    root = Tk()
    root.title("Obstacle Test")
    nrow = 40
    ncol = 80
    scale = 10
    canvas = Canvas(root, width=ncol*scale, height=nrow*scale, bg="black")
    canvas.pack()

    # Key bindings
    root.bind("1", lambda e: test1(root, canvas, nrow, ncol, scale))
    root.bind("2", lambda e: test2(root, canvas, nrow, ncol, scale))
    root.bind("<d>", lambda e: delete_all(canvas))

    instructions = """
    Press '1' to simulate Dino Run obstacles moving left
    Press '2' to simulate Dino Run obstacles continuously moving left
    Press 'd' to clear the canvas
    """
    print(instructions)
    
    root.mainloop()

if __name__ == "__main__":
    main()