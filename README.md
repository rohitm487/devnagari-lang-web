# देवनागरी Programming Language Web IDE

An online IDE for the Devnagari Programming Language, allowing you to write and execute code directly in your browser using Pyiodide.

## Features

- 🌐 Browser-based execution - no installation required
- 📝 Syntax-highlighted code editor
- 🎯 Real-time code execution
- 📚 Built-in code examples
- 🎨 Modern, responsive UI
- 💻 Cross-platform compatibility

## Quick Start

1. Visit the live demo at [rohitm487.github.io/devnagari-lang-web](https://rohitm487.github.io/devnagari-lang-web)
2. Start coding in Devnagari directly in your browser!

## Local Installation

### Method 1: Using Git (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/rohitm487/devnagari-lang-web.git
   cd devnagari-lang-web
   ```

2. Start a local server:
   ```bash
   python3 -m http.server 8000
   ```

3. Open your browser and navigate to `http://localhost:8000`

### Method 2: Direct Download

1. Go to the [releases page](https://github.com/rohitm487/devnagari-lang-web/releases)
2. Download the latest release ZIP file
3. Extract the ZIP file to your desired location
4. Open a terminal in the extracted folder
5. Start a local server:
   ```bash
   python3 -m http.server 8000
   ```
6. Open your browser and navigate to `http://localhost:8000`

## Usage Guide

1. **Writing Code**
   - Use the code editor on the left side
   - Select examples from the dropdown menu to get started
   - The editor supports syntax highlighting and auto-indentation

2. **Running Code**
   - Click the "Run Code" button or press Ctrl+Enter
   - The output will appear in the panel on the right
   - Use the "Clear Output" button to clear the output panel

3. **Examples**
   Try these built-in examples:
   - Factorial Calculator
   - Fibonacci Series
   - Simple Calculator

## Examples

### Factorial Calculator
```
फंक्शन factorial(n) {
    अगर n <= 1 {
        वापस 1;
    }
    वापस n * factorial(n - 1);
}

केलिए (वैरिएबल i = 1; i <= 5; i = i + 1) {
    वैरिएबल result = factorial(i);
    छाप i + "! = " + result;
}
```

### Fibonacci Series
```
फंक्शन fibonacci(n) {
    अगर n <= 1 {
        वापस n;
    }
    वापस fibonacci(n - 1) + fibonacci(n - 2);
}

केलिए (वैरिएबल i = 0; i < 10; i = i + 1) {
    छाप "F(" + i + ") = " + fibonacci(i);
}
```

## Troubleshooting

1. **Server Already Running**
   If you see "Address already in use" error:
   ```bash
   # Find the process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   # Or use this command to kill any process on port 8000
   lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
   ```

2. **Browser Issues**
   - Clear your browser cache if the page doesn't load properly
   - Make sure JavaScript is enabled in your browser
   - Try using a modern browser (Chrome, Firefox, Safari, or Edge)

## Technology Stack

- Pyiodide - Python runtime in the browser
- Ace Editor - Code editor
- Modern HTML/CSS/JavaScript
- GitHub Pages for hosting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/devnagari-lang-web/issues) page
2. Create a new issue if your problem isn't already reported
3. Join our community discussions 
