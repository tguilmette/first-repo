from tkinter import *
import time
import random

class Pixel:
    # Predefined color list for pixel representation
    color=['black','white','yellow','red','blue','green','orange','purple','brown','cyan']

    def __init__(self,canv,i,j,nrow,ncol,scale,icolor,vector=[0,0]):
        self.canvas = canv
        self.i = i
        self.j = j
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.icolor = icolor
        self.vector = vector
        
        self.id = self.canvas.create_rectangle(self.j*self.scale,self.i*self.scale, (self.j+1)*self.scale,(self.i+1)*self.scale, fill=self.color[self.icolor],outline='black')

    def __str__(self):
        return f"({self.i}, {self.j}) {self.color[self.icolor]}"
   
    def delete(self):
        self.canvas.delete(self.id)

    def left(self):
        self.vector = [0, -1]

    def right(self):
        self.vector = [0, 1]

    def up(self):
        self.vector = [-1, 0]

    def down(self):
        self.vector = [1, 0]

    def next(self):
        new_i = self.i + self.vector[0]
        new_j = self.j + self.vector[1]

        if 0 <= new_i < self.nrow and 0 <= new_j < self.ncol:
            self.i = new_i
            self.j = new_j
            self.canvas.move(self.id, self.vector[1] * self.scale, self.vector[0] * self.scale)
        else:
            print("Boundary reached, pixel cannot move further.")
        
    
#=============================================================================
# Testing Functions for Pixel Class - DO NOT MODIFY
#=============================================================================

def delete_all(canvas):
    """Clear all items from the canvas."""
    canvas.delete("all")
    print("Delete All")


def test1(canvas,nrow,ncol,scale):
    """Test 1: Generate 10 random pixels."""
    print("Generate 10 points at random")
    random.seed(4)  # for reproducibility
    for k in range(10):
        i=random.randint(0,nrow-1) 
        j=random.randint(0,ncol-1)
        c=random.randint(1,9)    # color number
        pix=Pixel(canvas,i,j,nrow,ncol,scale,c)
        print(pix)
       
def test2(root,canvas,nrow,ncol,scale):
    """Test 2: Move one pixel along a square path."""
    print("Move one point along a square")

    pix=Pixel(canvas,35,35,nrow,ncol,scale,3)
    
    # Move up
    pix.vector=[-1,0]
    for i in range(30):
        pix.next()
        root.update()    # update the graphic
        time.sleep(0.05) # animation delay
    
    # Move left
    pix.vector=[0,-1]
    for i in range(30):
        pix.next()
        root.update()
        time.sleep(0.05)
    
    # Move down
    pix.vector=[1,0]
    for i in range(30):
        pix.next()
        root.update()
        time.sleep(0.05)
    
    # Move right
    pix.vector=[0,1]
    for i in range(30):
        pix.next()
        root.update()
        time.sleep(0.05)

    # Clean up
    pix.delete()


def test3(root,canvas,nrow,ncol,scale):
    """Test 3: Move four pixels simultaneously in different directions."""
    print("Move four point along a square")

    # Create four pixels with different starting positions and directions
    pixs=[]
    pixs.append(Pixel(canvas,35,35,nrow,ncol,scale,3,[-1,0]))  # up
    pixs.append(Pixel(canvas,5,35,nrow,ncol,scale,4,[0,-1]))   # left
    pixs.append(Pixel(canvas,5,5,nrow,ncol,scale,5,[1,0]))     # down
    pixs.append(Pixel(canvas,35,5,nrow,ncol,scale,6,[0,1]))    # right
    
    print("Starting coords")
    for p in pixs: print(p)

    # Move all pixels simultaneously
    for i in range(30):
        for p in pixs:
            p.next()
        root.update()
        time.sleep(0.05)

    print("Ending coords")
    for p in pixs:
        print(p)
        p.delete()


def main():
    """Main function to initialize the application and set up test options."""
    # Create window and canvas
    root = Tk()
    nrow=40
    ncol=40
    scale=20
    canvas = Canvas(root,width=ncol*scale,height=nrow*scale,bg="black")
    canvas.pack()

    # Bind keyboard shortcuts for tests
    # Press keys 1-3 to run different tests, 'd' to clear canvas
    root.bind("1",lambda e:test1(canvas,nrow,ncol,scale))
    root.bind("2",lambda e:test2(root,canvas,nrow,ncol,scale))
    root.bind("3",lambda e:test3(root,canvas,nrow,ncol,scale))
    root.bind("<d>",lambda e:delete_all(canvas))
    
    instructions = """
    Press '1' to generate 10 random pixels
    Press '2' to move one pixel along a square path
    Press '3' to move four pixels simultaneously in different directions
    Press 'd' to clear the canvas
    """
    print(instructions)
    
    # Start main event loop
    root.mainloop()
        
if __name__=="__main__":
    main()