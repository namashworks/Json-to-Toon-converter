## Overview

TOON (Token-Oriented Object Notation) is a compact data format optimized for transmitting structured information to Large Language Models. This converter provides an intuitive interface to transform JSON files into TOON format, reducing token costs and improving context efficiency.

### Key Benefits

- **Cost Reduction**: Save 30-60% on LLM API costs (OpenAI, Anthropic, etc.)
- **Context Efficiency**: Fit more data within token limits
- **Human Readable**: Maintains clarity while optimizing for machines
- **Production Ready**: Built-in validation, error handling, and file size limits

---

## Features

- 📤 **Drag & Drop Upload** - Instant JSON file processing
- 📊 **Visual Analytics** - Real-time token savings metrics with charts
- ⚙️ **Customizable Options** - Configure indentation, delimiters, and markers
- 🔄 **Side-by-Side Comparison** - View JSON and TOON outputs simultaneously
- 💾 **Download Support** - Export `.toon` files instantly
- 🎯 **Sample Data** - Built-in examples for testing
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

---

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/namashworks/Json-to-Toon-converter.git
cd Json-to-Toon-converter

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

### Docker Deployment

```bash
docker-compose up
```

---

## Usage

### Basic Conversion

1. Upload a JSON file or click "Load Sample Data"
2. Adjust conversion settings in the sidebar (optional)
3. View comparison and statistics
4. Download the converted `.toon` file

### Conversion Options

| Option | Description | Default |
|--------|-------------|---------|
| **Indentation** | Spaces per indentation level (1-4) | 2 |
| **Delimiter** | Array separator: comma, tab, or pipe | comma |
| **Length Marker** | Add `#` prefix to array lengths | Off |

### Example Conversion

**Input JSON (177 characters)**
```json
{
  "users": [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25}
  ]
}
```

**Output TOON (85 characters - 52% reduction)**
```
users[2,]{id,name,age}:
1,Alice,30
2,Bob,25
```


### Other Platforms

<details>
<summary><b>Docker</b></summary>

```bash
docker build -t json-toon-converter .
docker run -p 8501:8501 json-toon-converter
```
</details>

<details>
<summary><b>Heroku</b></summary>

```bash
heroku create your-app-name
git push heroku main
```

Requires `Procfile` and `setup.sh` (included in repository)
</details>

<details>
<summary><b>Railway / Render</b></summary>

Connect your GitHub repository - auto-detection handles deployment automatically.
</details>

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## Technical Details

### TOON Format

TOON combines:
- **YAML-style indentation** for nested objects
- **CSV-style rows** for uniform arrays
- **Explicit length markers** for validation

#### Format Rules

- **Objects**: Key-value pairs with colon separation
- **Arrays**: Length indicator `[N]` with optional delimiter marker
- **Tabular Arrays**: CSV-like format `[N,]{fields}:` for uniform objects
- **Strings**: Quoted only when necessary (keywords, numbers, special chars)

### Dependencies

- `streamlit>=1.28.0` - Web framework
- `python-toon>=0.1.0` - TOON encoder
- `pandas>=2.0.0` - Data visualization

### File Structure

```
json-toon-converter/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
```

---

## Use Cases

### LLM Prompt Optimization
```python
from toon import encode

# Reduce token usage in prompts
data = load_large_dataset()
optimized_prompt = f"Analyze this data:\n{encode(data)}"
# 40-60% fewer tokens than JSON
```

### API Cost Reduction
- **OpenAI GPT-4**: Save ~$0.03 per 1K tokens
- **Anthropic Claude**: Save ~$0.015 per 1K tokens
- **Context Windows**: Fit more data within limits

### Data Transfer
- Compress structured data for LLMs
- Maintain human readability
- Validate with length markers

---

## Performance

| Metric | Value |
|--------|-------|
| Average Token Reduction | 30-60% |
| Max File Size | 200 MB |
| Conversion Speed | < 1 second for typical files |
| Memory Usage | Optimized for large datasets |

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone repository
git clone https://github.com/namashworks/Json-to-Toon-converter.git
cd Json-to-Toon-converter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **[Johann Schopplich](https://github.com/johannschopplich)** - Creator of TOON format ([Original TypeScript Implementation](https://github.com/johannschopplich/toon))
- **[Xavi Vinaixa](https://github.com/xaviviro)** - Python TOON implementation ([python-toon](https://github.com/xaviviro/python-toon))
- **[Streamlit](https://streamlit.io)** - Web application framework

---

## Resources

- [TOON Format Specification](https://github.com/johannschopplich/toon/blob/main/SPEC.md)
- [Python TOON Library](https://github.com/xaviviro/python-toon)
- [Streamlit Documentation](https://docs.streamlit.io)

---

## Support

- **Issues**: [Open an issue](https://github.com/yourusername/json-toon-converter/issues)
- **Discussions**: [Join the discussion](https://github.com/yourusername/json-toon-converter/discussions)
- **Email**: namash.work@gmail.com

---

<div align="center">

**[⬆ Back to Top](#json-to-toon-converter)**

Made with ❤️ using [Streamlit](https://streamlit.io)

**Star ⭐ this repository if you find it helpful!**

</div>
