# Stock Cutting Optimizer

This project provides tools for optimizing stock cutting patterns to minimize waste. It includes both a command-line interface and a graphical user interface.

## Dependencies

- Python 3.x
- numpy
- pulp
- tkinter (usually comes with Python)

Install the required packages using pip:
```bash
pip install numpy pulp
```

## Running the Application

### GUI Version
Run the graphical user interface:
```bash
python stock_cutter_gui.py
```

The GUI allows you to input:
- Stock Sizes: Comma-separated list of available stock lengths
- Required Sizes: Comma-separated list of required piece lengths
- Minimum Quantities: Comma-separated list of minimum quantities needed for each required size

Example input:
- Stock Sizes: 13,10
- Required Sizes: 5,2
- Minimum Quantities: 2,0

### Command Line Version
Run the command-line version:
```bash
python bryan_v1.py
```

## Output Format

The application will output:
- Total waste
- Optimization status
- Detailed cutting patterns showing how to cut each stock piece

Example output:
```
Waste = 2.0
Status: Optimal

Cutting Patterns:
Tronco:13,pieza:5 = 2.0
Tronco:13,pieza:2 = 1.0
```

## Authors
- Luis Alcantar @lfalcnatar
- Bryan Felix @bryanfelixg

Version: 0.2
Date: April 4, 2024
