const opSymbols = { add: '+', sub: '−', mul: '×', div: '÷' };

let selectedOperation = 'add';

const opBtns = document.querySelectorAll('.op-btn');
const opSymbolEl = document.getElementById('op-symbol');
const operand1Input = document.getElementById('operand1');
const operand2Input = document.getElementById('operand2');
const calcBtn = document.getElementById('calc-btn');
const clearBtn = document.getElementById('clear-btn');
const resultBox = document.getElementById('result-box');
const errorMessage = document.getElementById('error-message');
const binaryResultEl = document.getElementById('binary-result');
const decimalResultEl = document.getElementById('decimal-result');

opBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        opBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedOperation = btn.dataset.op;
        opSymbolEl.textContent = opSymbols[selectedOperation];
        hideError();
    });
});

function isValidBinary(str) {
    return /^[01]+$/.test(str);
}

function showError(msg) {
    errorMessage.textContent = msg;
    errorMessage.classList.remove('hidden');
    resultBox.classList.add('hidden');
}

function hideError() {
    errorMessage.classList.add('hidden');
}

function showResult(binaryResult, decimalResult) {
    binaryResultEl.textContent = binaryResult;
    decimalResultEl.textContent = decimalResult;
    resultBox.classList.remove('hidden');
    resultBox.style.animation = 'fadeIn 0.3s ease';
}

function calculate() {
    hideError();

    const val1 = operand1Input.value.trim();
    const val2 = operand2Input.value.trim();

    if (!val1 || !val2) {
        showError('Please enter both binary operands.');
        return;
    }

    if (!isValidBinary(val1) || !isValidBinary(val2)) {
        showError('Invalid binary string. Only 0 and 1 are allowed.');
        return;
    }

    const a = BigInt('0b' + val1);
    const b = BigInt('0b' + val2);

    let binaryResult;
    let decimalResult;

    try {
        switch (selectedOperation) {
            case 'add': {
                const sum = a + b;
                binaryResult = sum.toString(2);
                decimalResult = sum.toString(10);
                break;
            }
            case 'sub': {
                if (a >= b) {
                    binaryResult = (a - b).toString(2);
                    decimalResult = (a - b).toString(10);
                } else {
                    binaryResult = '-' + (b - a).toString(2);
                    decimalResult = '-' + (b - a).toString(10);
                }
                break;
            }
            case 'mul': {
                const product = a * b;
                binaryResult = product.toString(2);
                decimalResult = product.toString(10);
                break;
            }
            case 'div': {
                if (b === 0n) {
                    showError('Division by zero is undefined.');
                    return;
                }
                const quotient = a / b;
                binaryResult = quotient.toString(2);
                decimalResult = quotient.toString(10);
                break;
            }
        }
    } catch (err) {
        showError('Calculation error: ' + err.message);
        return;
    }

    showResult(binaryResult, decimalResult);
}

function clearAll() {
    operand1Input.value = '';
    operand2Input.value = '';
    selectedOperation = 'add';
    opBtns.forEach(b => b.classList.remove('active'));
    opBtns[0].classList.add('active');
    opSymbolEl.textContent = opSymbols['add'];
    resultBox.classList.add('hidden');
    hideError();
    operand1Input.classList.remove('invalid');
    operand2Input.classList.remove('invalid');
}

calcBtn.addEventListener('click', calculate);
clearBtn.addEventListener('click', clearAll);

operand1Input.addEventListener('input', () => {
    if (operand1Input.value && !isValidBinary(operand1Input.value)) {
        operand1Input.classList.add('invalid');
    } else {
        operand1Input.classList.remove('invalid');
    }
});

operand2Input.addEventListener('input', () => {
    if (operand2Input.value && !isValidBinary(operand2Input.value)) {
        operand2Input.classList.add('invalid');
    } else {
        operand2Input.classList.remove('invalid');
    }
});
