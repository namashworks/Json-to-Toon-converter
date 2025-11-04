# 🎒 Multi-Format to TOON Converter

**Cut your LLM token costs by 30-60%** — Convert JSON, CSV, Excel, YAML, XML, and TOML to [TOON format](https://github.com/johannschopplich/toon) for efficient prompt engineering.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)

## ✨ Features

- 🔄 **6 Input Formats**: JSON, CSV, Excel, YAML, XML, TOML
- 📉 **30-60% Token Reduction** vs JSON
- 🎨 **Interactive UI** with live preview
- 📊 **Visual Comparisons** and metrics
- ⚙️ **Customizable Options**: delimiters, indentation, length markers

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/namashworks/Json-to-Toon-converter.git
cd toon-converter

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run JSON-TOON-converter.py
```

Open your browser to `http://localhost:8501`

## 📦 Supported Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| JSON | `.json` | APIs, configurations |
| CSV | `.csv` | Tabular data |
| Excel | `.xlsx`, `.xls` | Spreadsheets |
| YAML | `.yaml`, `.yml` | Config files |
| XML | `.xml` | Legacy data |
| TOML | `.toml` | Python configs |

## 💡 Why TOON?

**Before (JSON - 177 chars):**
```json
{"users": [
  {"id": 1, "name": "Alice", "age": 30},
  {"id": 2, "name": "Bob", "age": 25}
]}
```

**After (TOON - 85 chars - 52% reduction):**
```
users[2,]{id,name,age}:
1,Alice,30
2,Bob,25
```

Perfect for:
- 🤖 LLM API cost optimization
- 📝 Efficient prompt engineering
- 🎯 Context window maximization

## 🛠️ Usage

1. **Upload** any supported file format
2. **Adjust** conversion settings in sidebar
3. **Compare** original vs TOON sizes
4. **Download** your optimized `.toon` file

Or try the built-in sample data for a quick demo!

## 📚 Resources

- [TOON Specification](https://github.com/johannschopplich/toon/blob/main/SPEC.md)
- [python-toon Library](https://github.com/xaviviro/python-toon)
- [Streamlit Documentation](https://docs.streamlit.io)

## 🤝 Contributing

Contributions welcome! Open an issue or submit a PR.

## 📄 License

MIT License - feel free to use in your projects!

## 🙏 Credits

- [TOON Format](https://github.com/johannschopplich/toon) by Johann Schopplich
- [python-toon](https://github.com/xaviviro/python-toon) by Xavier Virolés

---

**Made with ❤️ for efficient LLM prompting**
