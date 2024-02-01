import tkinter as tk
class Grid:
    def __init__(self, master, rows, cols, block_size):
        self.iteration_counter = 0 
        self.master = master
        self.rows = rows
        self.cols = cols
        self.block_size = block_size
        self.blocks = [[Block(master, row, col, block_size, self.on_block_click) for col in range(cols)] for row in range(rows)]
        self.is_enabled = True
        self.count = 0
        self.is_enabled = True
        self.is_iterating = False
        
    def get_block(self, row, col):
        return self.blocks[row][col]

    def on_block_click(self, block):
        if self.is_enabled: 
            block.change_status()
            self.update_grid()
            print(f"Clicked on block at row {block.row}, column {block.col}, block status:{block.status}")
    
    def update_grid(self):
        for row in self.blocks:
            for block in row:
                block.update_canvas()
    
    def copy_grid(self):
        new_grid = Grid(self.master, self.rows, self.cols, self.block_size)
        for i in range(self.rows):
            for j in range(self.cols):
                new_status = self.get_block(i, j).status
                new_grid.get_block(i, j).status = new_status
                new_grid.get_block(i, j).color = 'black' if new_status == 1 else 'white'
                new_grid.get_block(i, j).update_canvas()

        return new_grid
    
    def next_iteration(self):
        new_grid = self.copy_grid()

        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = self.calc_neighbors(row, col)
                status = self.get_block(row, col).status

                if status and (neighbors == 2 or neighbors == 3):  # Keep alive
                    new_grid.get_block(row, col).status = 1
                elif not status and (neighbors == 3):  # Born
                    new_grid.get_block(row, col).status = 1
                else:  # Kill off
                    new_grid.get_block(row, col).status = 0

        # Update the visual representation of the grid without creating new Canvas widgets
        for row in range(self.rows):
            for col in range(self.cols):
                current_block = self.get_block(row, col)
                new_status = new_grid.get_block(row, col).status
                current_block.status = new_status
                current_block.color = 'black' if new_status == 1 else 'white'
                current_block.update_canvas()

        self.master.update_iteration_label(self.iteration_counter)
        self.iteration_counter += 1
        
    def enable_grid(self):
        self.is_enabled = True
        self.is_iterating = False
    
    def disable_grid(self):
        self.is_enabled = False
        self.is_iterating = True
    
    def reset_grid(self):
        for row in self.blocks:
            for block in row: 
                block.status = 0 
                block.color = 'white'
                block.update_canvas()
    
    def calc_neighbors(self, k, j):
        current_n = 0
        max_index = self.rows - 1
        # check left
        if j - 1 >= 0 and self.blocks[k][j - 1].status:
            current_n += 1
        # Check Right
        if j + 1 <= max_index and self.blocks[k][j + 1].status:
            current_n += 1
        # Check up
        if k - 1 >= 0 and self.blocks[k - 1][j].status:
            current_n += 1
        # Check Down
        if k + 1 <= max_index and self.blocks[k + 1][j].status:
            current_n += 1
        # Check top left
        if k - 1 >= 0 and j - 1 >= 0 and self.blocks[k - 1][j - 1].status:
            current_n += 1
        # Check top right
        if k - 1 >= 0 and j + 1 <= max_index and self.blocks[k - 1][j + 1].status:
            current_n += 1
        # Check bottom left
        if k + 1 <= max_index and j - 1 >= 0 and self.blocks[k + 1][j - 1].status:
            current_n += 1
        # Check bottom right
        if k + 1 <= max_index and j + 1 <= max_index and self.blocks[k + 1][j + 1].status:
            current_n += 1
        return current_n
        

class Block:
    def __init__(self, master, row, col, size, click_callback):
        self.master = master
        self.status = 0  # All initialized to dead
        self.color = 'white'
        self.row = row
        self.col = col
        self.size = size
        self.click_callback = click_callback
        self.canvas = tk.Canvas(master.master, width=size, height=size, bg=self.color)
        self.canvas.grid(row=row, column=col)
        self.canvas.bind("<Button-1>", self.on_click)


    def change_status(self): #toggle between dead and alive
        if self.status == 0:
            self.status = 1
            self.color = 'black'
        else:
            self.status = 0
            self.color = 'white'
    
    def on_click(self, event):
        self.click_callback(self)
    
    def update_canvas(self):
        self.canvas.configure(bg=self.color)
    
class App:
    def __init__(self, master, rows, cols, block_size):
        self.master = master
        self.master.title("Conway's Game of Life")
        self.grid = Grid(self, rows, cols, block_size)
        
        self.start_button = tk.Button(master, text='Start', command=self.start)
        self.start_button.grid(row=rows, columnspan=cols)
        
        self.stop_button = tk.Button(master, text='Stop', command=self.stop)
        self.stop_button.grid(row=rows+1, columnspan=cols+1)
        
        self.iteration_var = tk.IntVar()
        self.iteration_var.set(0)
        self.iteration_label = tk.Label(master, text=f"Iteration number: {self.iteration_var.get()}")
        self.iteration_label.grid(row=rows+2, columnspan=cols+1)

        self.reset_button = tk.Button(master, text='Reset', command=self.reset)
        self.reset_button.grid(row=rows+3, columnspan=cols+2)

        self.terminate_button = tk.Button(master, text="Terminate", command=self.terminate)
        self.terminate_button.grid(row=rows+4, columnspan=cols+3)

    def start(self):
        print("Start button pressed.")
        self.grid.disable_grid()
        self.reset_iteration_label()
        self.animate_iteration()
    
    def terminate(self):
        print("Terminate button pressed")
        self.master.destroy()
    
    def animate_iteration(self, iteration_counter=None):
        if iteration_counter is None:
            iteration_counter = self.iteration_var.get()

        if self.grid.is_iterating:
            self.grid.next_iteration()

            # Update the iteration label without passing iteration_counter
            self.update_iteration_label()

            # Use lambda to pass the updated iteration_counter
            self.master.after(1000, lambda counter=iteration_counter + 1: self.animate_iteration(counter))

    def stop(self):
        print("Stop button has been pushed")
        self.grid.enable_grid()
        self.update_iteration_label(self.grid.iteration_counter)

    def update_iteration_label(self, iteration_counter=None):
        if iteration_counter is None:
            iteration_counter = self.iteration_var.get()
        self.iteration_var.set(iteration_counter)
        self.iteration_label.config(text=f"Iteration number: {iteration_counter}")

    def reset_iteration_label(self): #intializing back to 0
        self.iteration_var.set(0)
        self.iteration_label.config(text=f"Iteration number: {0}")
    
    def reset(self):
        print("Reset button pressed")
        self.grid.reset_grid()
        self.reset_iteration_label()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, rows=20, cols=20, block_size=20)
    root.mainloop()