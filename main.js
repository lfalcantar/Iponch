// Language translations
const translations = {
    en: {
        title: "Stock Cutting Optimizer",
        inputGuide: "Input Guide",
        step1: "Step 1: Enter available stock lengths",
        step2: "Step 2: Enter required piece lengths",
        step3: "Step 3: Enter minimum quantities needed",
        calculate: "Calculate",
        results: "Results",
        visualization: "Visualization",
        example: "Example: Stock: 13,10 | Pieces: 5,2 | Quantities: 2,0",
        tooltips: {
            stock: "Enter lengths separated by commas (e.g., 13,10)",
            required: "Enter required lengths separated by commas (e.g., 5,2)",
            quantity: "Enter minimum quantities for each required length (e.g., 2,0)"
        }
    },
    es: {
        title: "Optimizador de Corte de Material",
        inputGuide: "Guía de Entrada",
        step1: "Paso 1: Ingrese las longitudes de material disponible",
        step2: "Paso 2: Ingrese las longitudes de piezas requeridas",
        step3: "Paso 3: Ingrese las cantidades mínimas necesarias",
        calculate: "Calcular",
        results: "Resultados",
        visualization: "Visualización",
        example: "Ejemplo: Material: 13,10 | Piezas: 5,2 | Cantidades: 2,0",
        tooltips: {
            stock: "Ingrese longitudes separadas por comas (ej., 13,10)",
            required: "Ingrese longitudes requeridas separadas por comas (ej., 5,2)",
            quantity: "Ingrese cantidades mínimas para cada longitud requerida (ej., 2,0)"
        }
    }
};

// Current language
let currentLanguage = 'en';

// Initialize tooltips
document.querySelectorAll('.help-icon').forEach(icon => {
    icon.addEventListener('mouseenter', showTooltip);
    icon.addEventListener('mouseleave', hideTooltip);
});

function showTooltip(event) {
    const tooltip = document.getElementById('tooltip');
    const text = event.target.getAttribute('data-tooltip');
    tooltip.textContent = text;
    tooltip.style.display = 'block';
    tooltip.style.left = event.pageX + 10 + 'px';
    tooltip.style.top = event.pageY + 10 + 'px';
}

function hideTooltip() {
    document.getElementById('tooltip').style.display = 'none';
}

// Language selector
document.getElementById('language-selector').addEventListener('change', (event) => {
    currentLanguage = event.target.value;
    updateLanguage();
});

function updateLanguage() {
    const lang = translations[currentLanguage];
    document.querySelector('.title').textContent = lang.title;
    document.querySelector('.guide-title').textContent = lang.inputGuide;
    document.querySelector('.example').textContent = lang.example;
    document.querySelectorAll('.input-label span:first-child')[0].textContent = lang.step1;
    document.querySelectorAll('.input-label span:first-child')[1].textContent = lang.step2;
    document.querySelectorAll('.input-label span:first-child')[2].textContent = lang.step3;
    document.querySelector('.calculate-btn').textContent = lang.calculate;
    document.querySelector('.vis-title').textContent = lang.visualization;
}

function parseInput(value) {
    return value.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
}

function showError(message) {
    const results = document.getElementById('results');
    results.innerHTML = `Error\n${'='.repeat(50)}\n\n${message}\n\nPlease check your inputs and try again.`;
}

function calculate() {
    try {
        // Get inputs
        const stockSizes = parseInput(document.getElementById('stock-sizes').value);
        const requiredSizes = parseInput(document.getElementById('required-sizes').value);
        const minQuantities = parseInput(document.getElementById('min-quantities').value);

        // Validate inputs
        if (!stockSizes.length || !requiredSizes.length || !minQuantities.length) {
            throw new Error("Please fill in all fields with valid numbers");
        }

        if (requiredSizes.length !== minQuantities.length) {
            throw new Error("Number of required sizes must match number of minimum quantities");
        }

        const maxStock = Math.max(...stockSizes);
        for (const size of requiredSizes) {
            if (size > maxStock) {
                throw new Error(`Required size ${size} is larger than the largest stock size ${maxStock}`);
            }
        }

        // Calculate total required length
        const totalRequired = requiredSizes.reduce((sum, size, i) => sum + size * minQuantities[i], 0);
        const totalStock = stockSizes.reduce((a, b) => a + b, 0);

        if (totalRequired > totalStock) {
            throw new Error(`Insufficient stock. Required length (${totalRequired}) exceeds available stock (${totalStock})`);
        }

        // Solve the cutting stock problem
        const solution = solveCuttingStock(stockSizes, requiredSizes, minQuantities);

        // Display results
        displayResults(solution);

        // Update visualization
        updateVisualization(solution);

    } catch (error) {
        showError(error.message);
        clearVisualization();
    }
}

function displayResults(solution) {
    const results = document.getElementById('results');
    results.innerHTML = 'Optimization Results\n' + '='.repeat(50) + '\n\n';
    
    if (solution.status === 'optimal') {
        results.innerHTML += `Total Stock Length: ${solution.totalStock}\n`;
        results.innerHTML += `Total Used Length: ${solution.totalUsed}\n`;
        results.innerHTML += `Total Waste: ${solution.waste}\n`;
        results.innerHTML += `Efficiency: ${solution.efficiency}%\n`;
        results.innerHTML += `Status: ${solution.status}\n\n`;
        results.innerHTML += 'Cutting Patterns:\n' + '-'.repeat(50) + '\n';
        
        solution.patterns.forEach((pattern, i) => {
            const waste = pattern.stock - pattern.cuts.reduce((a, b) => a + b, 0);
            results.innerHTML += `• Log ${i + 1} (${pattern.stock}): ${pattern.cuts.join(', ')}`;
            if (waste > 0) {
                results.innerHTML += ` [Waste: ${waste}]`;
            }
            results.innerHTML += '\n';
        });
    } else {
        results.innerHTML += `Status: ${solution.status}\n`;
        results.innerHTML += `Message: ${solution.message}\n`;
        if (solution.remainingPieces && solution.remainingPieces.some(r => r > 0)) {
            results.innerHTML += '\nRemaining Requirements:\n';
            // Get the required sizes from the input fields
            const requiredSizes = document.getElementById('required-sizes').value
                .split(',')
                .map(size => parseFloat(size.trim()))
                .filter(size => !isNaN(size));
                
            solution.remainingPieces.forEach((remaining, i) => {
                if (remaining > 0 && requiredSizes[i]) {
                    results.innerHTML += `- ${remaining} more pieces of size ${requiredSizes[i]} needed\n`;
                }
            });
        }
    }
}

function updateVisualization(solution) {
    const container = document.getElementById('visualization-container');
    container.innerHTML = '';

    // Set up SVG
    const margin = { top: 40, right: 20, bottom: 60, left: 40 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = Math.max(solution.patterns.length * 100, 400);

    const svg = d3.select('#visualization-container')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Create scales
    const xScale = d3.scaleLinear()
        .domain([0, d3.max(solution.patterns, d => d.stock)])
        .range([0, width]);

    const yScale = d3.scaleBand()
        .domain(solution.patterns.map((_, i) => i))
        .range([0, height])
        .padding(0.3);

    // Draw logs
    solution.patterns.forEach((pattern, i) => {
        // Draw the log
        svg.append('rect')
            .attr('x', 0)
            .attr('y', yScale(i))
            .attr('width', xScale(pattern.stock))
            .attr('height', yScale.bandwidth())
            .attr('fill', d3.schemeCategory10[i % 10])
            .attr('opacity', 0.7);

        // Draw cuts
        let currentX = 0;
        pattern.cuts.forEach(cut => {
            // Draw cut line
            svg.append('line')
                .attr('x1', xScale(currentX))
                .attr('y1', yScale(i) - 5)
                .attr('x2', xScale(currentX))
                .attr('y2', yScale(i) + yScale.bandwidth() + 5)
                .attr('stroke', 'red')
                .attr('stroke-width', 1.5)
                .attr('opacity', 0.8);

            // Add size label
            svg.append('text')
                .attr('x', xScale(currentX + cut/2))
                .attr('y', yScale(i) - 8)
                .attr('text-anchor', 'middle')
                .attr('fill', 'white')
                .attr('font-size', '10px')
                .text(cut);

            currentX += cut;
        });

        // Draw final cut line
        if (currentX < pattern.stock) {
            svg.append('line')
                .attr('x1', xScale(currentX))
                .attr('y1', yScale(i) - 5)
                .attr('x2', xScale(currentX))
                .attr('y2', yScale(i) + yScale.bandwidth() + 5)
                .attr('stroke', 'red')
                .attr('stroke-width', 1.5)
                .attr('opacity', 0.8);
        }

        // Add log label
        svg.append('text')
            .attr('x', xScale(pattern.stock/2))
            .attr('y', yScale(i) + yScale.bandwidth()/2)
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .attr('fill', 'white')
            .attr('font-size', '10px')
            .text(`Log ${i + 1} (${pattern.stock})`);

        // Add waste information
        const waste = pattern.stock - pattern.cuts.reduce((a, b) => a + b, 0);
        if (waste > 0) {
            svg.append('text')
                .attr('x', xScale(currentX + waste/2))
                .attr('y', yScale(i) + yScale.bandwidth() + 15)
                .attr('text-anchor', 'middle')
                .attr('fill', '#ff6b6b')
                .attr('font-size', '10px')
                .text(`Waste: ${waste}`);
        }
    });

    // Add axes
    const xAxis = d3.axisBottom(xScale);
    svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis)
        .attr('color', 'white');

    // Add axis labels
    svg.append('text')
        .attr('x', width/2)
        .attr('y', height + margin.bottom - 10)
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .text('Length');

    // Add summary information
    svg.append('text')
        .attr('x', width/2)
        .attr('y', -10)
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .attr('font-size', '14px')
        .text(`Total Waste: ${solution.waste} (${solution.efficiency}% Efficiency)`);

    // Add legend
    const legend = svg.append('g')
        .attr('transform', `translate(${width - 150}, -30)`);

    legend.append('rect')
        .attr('width', 10)
        .attr('height', 10)
        .attr('fill', 'red')
        .attr('opacity', 0.8);

    legend.append('text')
        .attr('x', 15)
        .attr('y', 9)
        .attr('fill', 'white')
        .attr('font-size', '10px')
        .text('Cut Lines');

    legend.append('rect')
        .attr('y', 15)
        .attr('width', 10)
        .attr('height', 10)
        .attr('fill', d3.schemeCategory10[0])
        .attr('opacity', 0.7);

    legend.append('text')
        .attr('x', 15)
        .attr('y', 24)
        .attr('fill', 'white')
        .attr('font-size', '10px')
        .text('Stock Material');
}

function clearVisualization() {
    const container = document.getElementById('visualization-container');
    container.innerHTML = '';
} 