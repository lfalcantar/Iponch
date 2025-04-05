// Test cases
const testCases = [
    {
        name: "Basic Case",
        stock: [11, 11],
        required: [5, 2],
        quantities: [3, 3],
        expected: {
            patterns: [
                { stock: 11, cuts: [5, 5] },
                { stock: 11, cuts: [5, 2, 2, 2] }
            ],
            waste: 1
        }
    },
    {
        name: "Perfect Fit",
        stock: [10, 10],
        required: [5, 2],
        quantities: [2, 2],
        expected: {
            patterns: [
                { stock: 10, cuts: [5, 5] },
                { stock: 10, cuts: [2, 2, 2, 2, 2] }
            ],
            waste: 0
        }
    },
    {
        name: "Single Stock",
        stock: [20],
        required: [5, 3],
        quantities: [2, 2],
        expected: {
            patterns: [
                { stock: 20, cuts: [5, 5, 3, 3] }
            ],
            waste: 4
        }
    }
];

// Solver for the cutting stock optimization problem
function solveCuttingStock(stockSizes, requiredSizes, minQuantities) {
    try {
        // Initialize patterns and variables
        const patterns = [];
        let totalUsed = 0;
        const totalStock = stockSizes.reduce((a, b) => a + b, 0);
        
        // Sort stock sizes in descending order
        stockSizes.sort((a, b) => b - a);
        
        // Sort required sizes in descending order with their indices
        const sortedSizes = requiredSizes.map((size, index) => ({ size, index }));
        sortedSizes.sort((a, b) => b.size - a.size);
        
        // For each stock size
        for (let i = 0; i < stockSizes.length; i++) {
            const currentStock = stockSizes[i];
            let remainingQuantities = [...minQuantities];
            let pattern = {
                stock: currentStock,
                cuts: []
            };
            
            // Keep cutting pieces until we can't fit any more
            let remainingLength = currentStock;
            let madeProgress;
            
            do {
                madeProgress = false;
                
                // Try to fit pieces in descending order of size
                for (const { size, index } of sortedSizes) {
                    if (remainingQuantities[index] > 0 && size <= remainingLength) {
                        // Check if we can fit multiple pieces of the same size
                        const maxPieces = Math.min(
                            Math.floor(remainingLength / size),
                            remainingQuantities[index]
                        );
                        
                        if (maxPieces > 0) {
                            for (let p = 0; p < maxPieces; p++) {
                                pattern.cuts.push(size);
                                remainingLength -= size;
                                remainingQuantities[index]--;
                                totalUsed += size;
                            }
                            madeProgress = true;
                            break;
                        }
                    }
                }
            } while (madeProgress);
            
            // If we made any cuts, add the pattern
            if (pattern.cuts.length > 0) {
                patterns.push(pattern);
            }
            
            // Check if we've met all requirements
            if (remainingQuantities.every(q => q <= 0)) {
                break;
            }
        }
        
        // Check if all requirements were met
        const remainingPieces = minQuantities.map((min, i) => {
            const cut = patterns.reduce((sum, pattern) => {
                return sum + pattern.cuts.filter(c => c === requiredSizes[i]).length;
            }, 0);
            return min - cut;
        });
        
        if (remainingPieces.some(r => r > 0)) {
            return {
                status: 'infeasible',
                message: 'Could not meet all requirements with given stock sizes',
                patterns: [],
                totalStock,
                totalUsed: 0,
                waste: 0,
                remainingPieces
            };
        }
        
        // Calculate waste
        const waste = totalStock - totalUsed;
        
        // Calculate efficiency
        const efficiency = ((totalUsed / totalStock) * 100).toFixed(2);
        
        return {
            status: 'optimal',
            patterns,
            totalStock,
            totalUsed,
            waste,
            efficiency,
            remainingPieces: new Array(requiredSizes.length).fill(0)
        };
        
    } catch (error) {
        return {
            status: 'error',
            message: error.message,
            patterns: [],
            totalStock: 0,
            totalUsed: 0,
            waste: 0,
            efficiency: 0,
            remainingPieces: []
        };
    }
}

// Run test cases
function runTestCases() {
    console.log("Running test cases...");
    testCases.forEach(test => {
        const result = solveCuttingStock(test.stock, test.required, test.quantities);
        const passed = JSON.stringify(result.patterns) === JSON.stringify(test.expected.patterns) &&
                      result.waste === test.expected.waste;
        
        console.log(`\nTest Case: ${test.name}`);
        console.log(`Input: Stock=${test.stock}, Required=${test.required}, Quantities=${test.quantities}`);
        console.log(`Expected: ${JSON.stringify(test.expected)}`);
        console.log(`Result: ${JSON.stringify(result)}`);
        console.log(`Status: ${passed ? 'PASSED' : 'FAILED'}`);
    });
}

// Helper function to check if a solution is feasible
function checkFeasibility(patterns, requiredSizes, minQuantities) {
    const actualQuantities = new Array(requiredSizes.length).fill(0);
    
    patterns.forEach(pattern => {
        pattern.cuts.forEach(cut => {
            const index = requiredSizes.indexOf(cut);
            if (index !== -1) {
                actualQuantities[index]++;
            }
        });
    });
    
    return minQuantities.every((min, i) => actualQuantities[i] >= min);
}

// Helper function to calculate total length used
function calculateTotalUsed(patterns) {
    return patterns.reduce((total, pattern) => {
        return total + pattern.cuts.reduce((sum, cut) => sum + cut, 0);
    }, 0);
}

// Helper function to validate input data
function validateInputs(stockSizes, requiredSizes, minQuantities) {
    if (!Array.isArray(stockSizes) || !Array.isArray(requiredSizes) || !Array.isArray(minQuantities)) {
        throw new Error("All inputs must be arrays");
    }
    
    if (stockSizes.length === 0 || requiredSizes.length === 0 || minQuantities.length === 0) {
        throw new Error("All inputs must be non-empty arrays");
    }
    
    if (requiredSizes.length !== minQuantities.length) {
        throw new Error("Number of required sizes must match number of minimum quantities");
    }
    
    if (!stockSizes.every(x => x > 0) || !requiredSizes.every(x => x > 0) || !minQuantities.every(x => x >= 0)) {
        throw new Error("Stock sizes and required sizes must be positive numbers, minimum quantities must be non-negative");
    }
    
    const maxStock = Math.max(...stockSizes);
    if (requiredSizes.some(size => size > maxStock)) {
        throw new Error("All required sizes must be smaller than or equal to the largest stock size");
    }
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        solveCuttingStock,
        runTestCases,
        testCases
    };
} 