const codeEl = document.getElementById('code');
const outputEl = document.getElementById('output');
const runBtn = document.getElementById('runBtn');
const stopBtn = document.getElementById('stopBtn');
const clearBtn = document.getElementById('clearBtn');
const statusEl = document.getElementById('runtimeStatus');
const timeEl = document.getElementById('executionTime');
const countEl = document.getElementById('charCount');
const exampleEl = document.getElementById('exampleSelect');
const themeBtn = document.getElementById('themeBtn');

let pyodide = null;
let running = false;
let executionToken = 0;

const examples = {
  hello: `name = "Python Runner"
print(f"Hello, {name}!")
print("Python is running in your browser.")`,
  loops: `total = 0
for number in range(1, 11):
    total += number
    print(f"{number:2} -> running total: {total}")

print("Final total:", total)`,
  data: `import statistics

values = [12, 18, 7, 21, 14, 10, 25]
print("Values:", values)
print("Count:", len(values))
print("Mean:", statistics.mean(values))
print("Median:", statistics.median(values))
print("Min / Max:", min(values), "/", max(values))`,
  error: `def divide(a, b):
    return a / b

print(divide(10, 0))`
};

function setStatus(text, state = 'loading') {
  statusEl.className = `status ${state}`;
  statusEl.innerHTML = `<span class="dot"></span>${text}`;
}

function updateCount() {
  countEl.textContent = `${codeEl.value.length.toLocaleString()} chars`;
}

function appendOutput(text) {
  outputEl.textContent += text;
  outputEl.scrollTop = outputEl.scrollHeight;
}

function clearOutput() {
  outputEl.textContent = '';
  outputEl.className = 'output';
  timeEl.textContent = '';
}

async function initPython() {
  try {
    setStatus('Loading Python…', 'loading');
    pyodide = await loadPyodide();
    setStatus(`Python ${pyodide.runPython('import sys; sys.version.split()[0]')}`, 'ready');
    outputEl.textContent = 'Ready. Click Run to execute your Python code.';
    runBtn.disabled = false;
  } catch (error) {
    console.error(error);
    setStatus('Runtime failed to load', 'error');
    outputEl.className = 'output error';
    outputEl.textContent = `Could not load Pyodide.\n\n${error}`;
  }
}

async function runCode() {
  if (!pyodide || running) return;
  const code = codeEl.value;
  const token = ++executionToken;
  running = true;
  runBtn.disabled = true;
  stopBtn.disabled = false;
  clearOutput();
  appendOutput('Running…\n\n');
  setStatus('Running', 'loading');
  const start = performance.now();

  try {
    pyodide.setStdout({ batched: (msg) => {
      if (token === executionToken) appendOutput(msg + '\n');
    }});
    pyodide.setStderr({ batched: (msg) => {
      if (token === executionToken) appendOutput(msg + '\n');
    }});

    await pyodide.runPythonAsync(code);
    if (token === executionToken) {
      outputEl.classList.add('success');
      appendOutput(`\n✓ Finished successfully`);
      setStatus('Ready', 'ready');
    }
  } catch (error) {
    if (token === executionToken) {
      outputEl.classList.add('error');
      appendOutput(`\n✕ ${error}`);
      setStatus('Execution error', 'error');
    }
  } finally {
    pyodide.setStdout({});
    pyodide.setStderr({});
    if (token === executionToken) {
      timeEl.textContent = `${(performance.now() - start).toFixed(0)} ms`;
      running = false;
      runBtn.disabled = false;
      stopBtn.disabled = true;
    }
  }
}

function stopCode() {
  if (!running) return;
  executionToken++;
  running = false;
  stopBtn.disabled = true;
  runBtn.disabled = false;
  setStatus('Ready', 'ready');
  appendOutput('\n\n■ Stopped output collection. A running Python operation may finish in the background.');
}

codeEl.addEventListener('input', updateCount);
runBtn.addEventListener('click', runCode);
stopBtn.addEventListener('click', stopCode);
clearBtn.addEventListener('click', clearOutput);

exampleEl.addEventListener('change', () => {
  const example = examples[exampleEl.value];
  if (example !== undefined) {
    codeEl.value = example;
    updateCount();
    clearOutput();
    outputEl.textContent = 'Example loaded. Click Run to execute it.';
  }
  exampleEl.value = '';
});

themeBtn.addEventListener('click', () => {
  document.documentElement.classList.toggle('light');
  themeBtn.textContent = document.documentElement.classList.contains('light') ? '☀' : '☾';
});

codeEl.addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    event.preventDefault();
    runCode();
  }
  if (event.key === 'Tab') {
    event.preventDefault();
    const start = codeEl.selectionStart;
    const end = codeEl.selectionEnd;
    codeEl.value = codeEl.value.slice(0, start) + '    ' + codeEl.value.slice(end);
    codeEl.selectionStart = codeEl.selectionEnd = start + 4;
    updateCount();
  }
});

updateCount();
initPython();
