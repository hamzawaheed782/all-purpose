# Pastel Binary Calculator

A beautifully styled binary calculator built with pure HTML, CSS, and vanilla JavaScript. Perform exact binary arithmetic with four operations: addition, subtraction, multiplication, and division.

## Features

- **Four Operations**: Addition (+), Subtraction (−), Multiplication (×), Division (÷)
- **Exact Precision**: Uses JavaScript `BigInt` for arbitrary-length binary arithmetic
- **Pastel UI**: Soft lavender, mint, pink, and yellow color palette
- **Binary & Decimal Output**: Shows results in both binary and decimal formats
- **Input Validation**: Rejects invalid binary characters in real-time
- **Division by Zero Handling**: Clear error messages for undefined operations
- **Negative Results**: Supports negative results for subtraction when operand 1 < operand 2

## Operations

| Operation | Example | Result |
|-----------|---------|--------|
| Addition | `101` + `11` | `1000` (5 + 3 = 8) |
| Subtraction | `1010` − `0011` | `111` (10 - 3 = 7) |
| Multiplication | `101` × `11` | `1111` (5 * 3 = 15) |
| Division | `1010` ÷ `10` | `101` (10 / 2 = 5) |

## Usage

1. Select an operation by clicking one of the four buttons (+, −, ×, ÷)
2. Enter binary values (0s and 1s) in the operand fields
3. Click **Calculate** to see the result
4. Click **Clear** to reset the calculator

## Technology

- HTML5
- CSS3 (with CSS variables for theming)
- Vanilla JavaScript (ES6+, using `BigInt`)
- No external dependencies or frameworks
