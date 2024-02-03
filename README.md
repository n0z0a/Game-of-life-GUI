# Conway's Game of Life GUI

## Description
This Python project features a graphical user interface (GUI) for playing Conway's Game of Life. The Game of Life is a cellular automaton devised by the mathematician John Conway. The rules of the game are simple and are based on the state of neighboring cells:

1. Any live cell with fewer than two live neighbors dies, caused by under-population.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, caused by overpopulation.
4. Any dead cell with exactly three live neighbors becomes a live cell, caused by reproduction.

The user can interact with the GUI by clicking on cells to set the initial state and then starting the simulation to observe the evolution of generations.

## Creator

- **Noah Ibarra**

## Features
- **User Interaction**: Click on cells to set the initial live cells.
- **Simulation**: Press the "Start" button to simulate the game and observe the generations.
- **Rule Adherence**: The simulation adheres to Conway's Game of Life rules.

## Usage
1. Run the script:
   ```bash
   python game.py
   
## Future Work
- **Optimization**: Explore opportunities for optimizing the GUI to enhance performance and achieve faster results.
- **Threading**: Investigate the potential for implementing threading to further improve the responsiveness of the application.
- **GUI Styling**: Consider enhancing the visual appeal and user experience by refining the styling of the GUI elements.
