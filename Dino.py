from tkinter import *
from Pixel import Pixel
import numpy as np

class Dino(Pixel):
    def __init__(self, canv, nrow, ncol, scale, c = 2, game = None):
        self.canvas = canv
        self.i = nrow / 2
        self.j = ncol / 2 
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.color = c  
        self.pattern = self.get_pattern()
        self.jumping = False
        self.game = game 

    def get_pattern(self):
        return np.array([[0, 0, 1, 1, 1, 1],
                         [0, 0, 1, 1, 0, 1],
                         [0, 0, 1, 1, 1, 1],
                         [0, 0, 1, 1, 0, 0],
                         [1, 0, 1, 1, 1, 1],
                         [1, 0, 1, 1, 0, 0],
                         [1, 1, 1, 1, 0, 0],
                         [0, 1, 0, 1, 0, 0],
                         [0, 1, 0, 1, 0, 0]])
    

    def activate(self):
        dino_pixels = []
        
        for r in range(self.pattern.shape[0]):
            for c in range(self.pattern.shape[1]):
                if (self.pattern[r, c]) == 1:
                    pixel = Pixel(self.canvas,
                                 (self.i + r),
                                 (self.j + c),
                                 self.nrow,
                                 self.ncol,
                                 self.scale,
                                 self.color
                                 )
                    dino_pixels.append(pixel)

        self.dino_pixels = dino_pixels
    

    def down(self):
        new_dino_pixels = []

        for pixel in reversed(self.dino_pixels):
            if pixel.i < self.nrow - .5 * self.scale: 
                pixel.delete() 
                pixel.i += 1 
                pixel = Pixel(pixel.canvas, pixel.i, pixel.j, self.nrow, self.ncol, self.scale, self.color)
                new_dino_pixels.append(pixel)
            elif pixel.i >= self.nrow - .5 * self.scale: 
                print("Dino at the bottom!")
                break

        self.dino_pixels = new_dino_pixels
    

    def up(self):
        new_dino_pixels = []

        for pixel in self.dino_pixels:
            if pixel.i > .5 * self.scale: 
                pixel.delete() 
                pixel.i -= 1
                pixel = Pixel(pixel.canvas,
                              pixel.i, pixel.j,
                              self.nrow,
                              self.ncol,
                              self.scale, 
                              self.color
                              )
                new_dino_pixels.append(pixel)
            elif pixel.i <= .5 * self.scale: 
                print("Dino at the top!")
                break

        self.dino_pixels = new_dino_pixels

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.activate_jump(0)

    def activate_jump(self, step):
        if self.game and self.game.is_pause():
            self.canvas.after(50, self.activate_jump, step)  
            return
        
        if step < 10:
            self.up()
            self.canvas.after(50, self.activate_jump, step + 1)
        elif step < 20:
            self.down()
            self.canvas.after(50, self.activate_jump, step + 1)
        else:
            self.jumping = False

#=============================================================================
# Testing Functions for Dinosaur Class - DO NOT MODIFY
#=============================================================================

def delete_all(canvas):
    canvas.delete("all")

def test1(root, canvas, nrow, ncol, scale):
    d = Dino(canvas, nrow, ncol, scale)
    # Activate the dino in the middle left of the canvas
    d.activate()
    
    # Bind only up and down arrow keys to test basic movement
    root.bind("<Up>", lambda e: d.up())
    root.bind("<Down>", lambda e: d.down())
    
    # Add a visual indicator for test1
    print("\nPress Up/Down arrow keys to move the dinosaur up and down.\n")

def test2(root, canvas, nrow, ncol, scale):
    d = Dino(canvas, nrow, ncol, scale)
    # Activate the dino in the middle of the canvas.
    d.activate()
    
    # Bind arrow keys to move the dino
    root.bind("<space>", lambda e: d.jump())  # Bind spacebar to jump

    print("\nPress Spacebar to make the dinosaur jump.\n")



def main():
    """Initialize the game window and start the application."""
    root = Tk()
    nrow = 40
    ncol = 80
    scale = 20
    canvas = Canvas(root, width=ncol * scale, height=nrow * scale, bg="black")
    canvas.pack()

    # Bind a key for clearing the canvas.
    root.bind("1", lambda e: test1(root, canvas, nrow, ncol, scale))
    root.bind("2", lambda e: test2(root, canvas, nrow, ncol, scale))
    root.bind("d", lambda e: delete_all(canvas))

    instructions = """
    Press '1' to test basic up/down movement.
    Press '2' to test jump movement.
    Press 'd' to clear the canvas.
    """
    print(instructions)

    root.mainloop()

if __name__ == "__main__":
    main()