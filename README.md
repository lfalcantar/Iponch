# Stock Cutting Optimizer

A web-based tool for optimizing stock cutting patterns to minimize waste. The application helps determine the most efficient way to cut stock material into required pieces while meeting minimum quantity requirements.

## Features

- Modern, responsive web interface
- Real-time visualization of cutting patterns
- Bilingual support (English/Spanish)
- Interactive tooltips and help guides
- Detailed results and waste calculations
- Dark theme UI

## Prerequisites

- A modern web browser (Chrome, Firefox, Safari, or Edge)
- No additional software installation required

## Running the Project

### Option 1: Using a Local Web Server

1. Clone or download the repository
2. Open a terminal/command prompt in the project directory
3. Start a local web server using one of these methods:

#### Using Python (if installed):
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

#### Using Node.js (if installed):
```bash
npx http-server
```

4. Open your web browser and navigate to:
   - `http://localhost:8000` (if using Python)
   - `http://localhost:8080` (if using Node.js)

### Option 2: Direct File Access

1. Simply open the `index.html` file in your web browser
2. Note: Some features might be limited due to browser security restrictions

## Usage

1. Enter available stock lengths (comma-separated)
   - Example: `13,10`

2. Enter required piece lengths (comma-separated)
   - Example: `5,2`

3. Enter minimum quantities needed (comma-separated)
   - Example: `2,0`

4. Click "Calculate" to see the results

## Input Format

- All inputs should be comma-separated numbers
- Stock sizes: Available lengths of material
- Required sizes: Lengths of pieces needed
- Minimum quantities: Minimum number of each required piece

Example:
```
Stock: 13,10
Pieces: 5,2
Quantities: 2,0
```

## Output

The application provides:
- Total stock length used
- Total waste
- Detailed cutting patterns
- Visual representation of cuts
- Optimization status

## Troubleshooting

If you encounter any issues:
1. Ensure all inputs are valid numbers
2. Check that required piece sizes are not larger than stock sizes
3. Verify that total required length does not exceed available stock
4. Try using a different web browser
5. Make sure JavaScript is enabled in your browser

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is open source and available under the MIT License.
