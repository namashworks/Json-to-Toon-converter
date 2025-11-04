import streamlit as st
import json
from io import BytesIO, StringIO
import sys
from pathlib import Path

# Note: Install required libraries
# pip install python-toon pandas openpyxl pyyaml
try:
    from toon import encode
except ImportError:
    st.error("⚠️ python-toon library not installed. Please run: pip install python-toon")
    st.stop()

import pandas as pd
import yaml
import xml.etree.ElementTree as ET

# Try importing tomli for Python <3.11
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

# Page configuration
st.set_page_config(
    page_title="Multi-Format to TOON Converter",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .format-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        margin: 0.25rem;
        border-radius: 0.25rem;
        background-color: #e1f5ff;
        color: #01579b;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎒 Multi-Format to TOON Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Convert JSON, CSV, Excel, YAML, XML, TOML to TOON — Reduce LLM tokens by 30-60%</div>', unsafe_allow_html=True)

# Format parsers
def parse_json(file_content):
    """Parse JSON file"""
    return json.loads(file_content)

def parse_csv(file_content):
    """Parse CSV file to dict"""
    df = pd.read_csv(StringIO(file_content))
    return df.to_dict(orient='records')

def parse_excel(file_bytes):
    """Parse Excel file to dict"""
    df = pd.read_excel(BytesIO(file_bytes))
    return df.to_dict(orient='records')

def parse_yaml(file_content):
    """Parse YAML file"""
    return yaml.safe_load(file_content)

def parse_xml(file_content):
    """Parse XML to dict (simplified)"""
    def xml_to_dict(element):
        result = {}
        # Add attributes
        if element.attrib:
            result['@attributes'] = element.attrib
        
        # Add text content
        if element.text and element.text.strip():
            if len(element) == 0:
                return element.text.strip()
            result['#text'] = element.text.strip()
        
        # Add children
        for child in element:
            child_data = xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result if result else None
    
    root = ET.fromstring(file_content)
    return {root.tag: xml_to_dict(root)}

def parse_toml(file_content):
    """Parse TOML file"""
    if tomllib is None:
        raise ImportError("TOML parsing requires tomli library. Install with: pip install tomli")
    return tomllib.loads(file_content)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About TOON")
    st.markdown("""
    **TOON** (Token-Oriented Object Notation) is a compact format for LLMs with 30-60% token reduction vs JSON.
    
    **✨ Now supports:**
    """)
    
    formats_html = """
    <div style='line-height: 2;'>
        <span class='format-badge'>JSON</span>
        <span class='format-badge'>CSV</span>
        <span class='format-badge'>Excel</span>
        <span class='format-badge'>YAML</span>
        <span class='format-badge'>XML</span>
        <span class='format-badge'>TOML</span>
    </div>
    """
    st.markdown(formats_html, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("⚙️ Conversion Options")
    
    indent_size = st.slider("Indentation (spaces)", 1, 4, 2)
    
    delimiter = st.selectbox(
        "Array Delimiter",
        options=["comma", "tab", "pipe"],
        index=0,
        format_func=lambda x: {"comma": "Comma (,)", "tab": "Tab (\\t)", "pipe": "Pipe (|)"}[x]
    )
    
    use_length_marker = st.checkbox("Use # length marker", value=False, 
                                   help="Add # prefix to array lengths")
    
    # CSV/Excel specific options
    st.subheader("📊 CSV/Excel Options")
    wrap_in_object = st.checkbox("Wrap tabular data in object", value=True,
                                 help="Wrap CSV/Excel data with a key (e.g., 'data')")
    data_key = st.text_input("Data key name", value="data", 
                            disabled=not wrap_in_object)
    
    st.divider()
    
    st.markdown("""
    **📚 Resources:**
    - [TOON Spec](https://github.com/johannschopplich/toon/blob/main/SPEC.md)
    - [python-toon](https://github.com/xaviviro/python-toon)
    """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Upload File")
    uploaded_file = st.file_uploader(
        "Choose a file to convert",
        type=['json', 'csv', 'xlsx', 'xls', 'yaml', 'yml', 'xml', 'toml'],
        help="Supported: JSON, CSV, Excel, YAML, XML, TOML"
    )
    
    # Sample data options
    st.subheader("📝 Or Load Sample Data")
    sample_col1, sample_col2 = st.columns(2)
    
    with sample_col1:
        if st.button("🗂️ JSON Sample"):
            st.session_state['sample_data'] = {
                "users": [
                    {"id": 1, "name": "Alice", "age": 30, "role": "admin"},
                    {"id": 2, "name": "Bob", "age": 25, "role": "user"}
                ],
                "config": {"timeout": 3000, "retries": 3}
            }
            st.session_state['sample_format'] = 'json'
            st.success("✅ JSON sample loaded!")
    
    with sample_col2:
        if st.button("📊 CSV Sample"):
            st.session_state['sample_data'] = [
                {"product": "Laptop", "price": 999, "stock": 15},
                {"product": "Mouse", "price": 25, "stock": 150},
                {"product": "Keyboard", "price": 75, "stock": 80}
            ]
            st.session_state['sample_format'] = 'csv'
            st.success("✅ CSV sample loaded!")

with col2:
    st.subheader("📤 Download TOON")
    st.info("Upload a file or load sample data to see the conversion")

# Process the file
if uploaded_file is not None or 'sample_data' in st.session_state:
    
    try:
        # Load and parse data based on format
        if uploaded_file is not None:
            file_name = uploaded_file.name.rsplit('.', 1)[0]
            file_ext = uploaded_file.name.rsplit('.', 1)[1].lower()
            
            if file_ext == 'json':
                file_content = uploaded_file.read().decode('utf-8')
                parsed_data = parse_json(file_content)
                original_format = 'JSON'
                
            elif file_ext == 'csv':
                file_content = uploaded_file.read().decode('utf-8')
                parsed_data = parse_csv(file_content)
                if wrap_in_object:
                    parsed_data = {data_key: parsed_data}
                original_format = 'CSV'
                
            elif file_ext in ['xlsx', 'xls']:
                file_bytes = uploaded_file.read()
                parsed_data = parse_excel(file_bytes)
                if wrap_in_object:
                    parsed_data = {data_key: parsed_data}
                original_format = 'Excel'
                
            elif file_ext in ['yaml', 'yml']:
                file_content = uploaded_file.read().decode('utf-8')
                parsed_data = parse_yaml(file_content)
                original_format = 'YAML'
                
            elif file_ext == 'xml':
                file_content = uploaded_file.read().decode('utf-8')
                parsed_data = parse_xml(file_content)
                original_format = 'XML'
                
            elif file_ext == 'toml':
                file_content = uploaded_file.read().decode('utf-8')
                parsed_data = parse_toml(file_content)
                original_format = 'TOML'
            else:
                st.error(f"❌ Unsupported format: {file_ext}")
                st.stop()
        else:
            parsed_data = st.session_state['sample_data']
            file_name = "sample"
            original_format = st.session_state.get('sample_format', 'JSON').upper()
            if original_format == 'CSV' and wrap_in_object:
                parsed_data = {data_key: parsed_data}
        
        # Create encoding options
        encode_options = {
            "indent": indent_size,
            "delimiter": delimiter,
            "lengthMarker": "#" if use_length_marker else False
        }
        
        # Convert to TOON
        toon_output = encode(parsed_data, encode_options)
        
        # Calculate statistics
        json_str = json.dumps(parsed_data, indent=2)
        json_size = len(json_str)
        toon_size = len(toon_output)
        reduction = 100 * (1 - toon_size / json_size)
        
        # Display results in tabs
        tab1, tab2, tab3 = st.tabs(["📊 Comparison", f"📄 Parsed Data (JSON)", "🎒 TOON Output"])
        
        with tab1:
            st.info(f"**Source Format:** {original_format} → **Target Format:** TOON")
            
            # Metrics
            col_m1, col_m2, col_m3 = st.columns(3)
            
            with col_m1:
                st.metric(
                    label="JSON Equivalent",
                    value=f"{json_size} chars"
                )
            
            with col_m2:
                st.metric(
                    label="TOON Size",
                    value=f"{toon_size} chars",
                    delta=f"-{json_size - toon_size} chars"
                )
            
            with col_m3:
                st.metric(
                    label="Reduction",
                    value=f"{reduction:.1f}%",
                    delta=f"Saved {json_size - toon_size} chars"
                )
            
            # Visual comparison
            st.divider()
            st.subheader("📈 Size Comparison")
            
            df = pd.DataFrame({
                'Format': ['JSON Equivalent', 'TOON'],
                'Size (characters)': [json_size, toon_size]
            })
            
            st.bar_chart(df.set_index('Format'))
            
            # Explanation
            st.success(f"""
            **🎯 Conversion Results:**
            
            - **Original Format:** {original_format}
            - **JSON Equivalent:** {json_size} characters
            - **TOON Format:** {toon_size} characters
            - **Reduction:** {reduction:.1f}% ({json_size - toon_size} characters saved)
            
            This reduction translates to similar token savings in LLM APIs, reducing costs and improving efficiency.
            """)
        
        with tab2:
            st.code(json_str, language='json')
            
            # Download JSON
            json_bytes = json_str.encode('utf-8')
            st.download_button(
                label="⬇️ Download as JSON",
                data=json_bytes,
                file_name=f"{file_name}.json",
                mime="application/json"
            )
        
        with tab3:
            st.code(toon_output, language='yaml')
            
            # Download TOON
            toon_bytes = toon_output.encode('utf-8')
            st.download_button(
                label="⬇️ Download TOON",
                data=toon_bytes,
                file_name=f"{file_name}.toon",
                mime="text/plain"
            )
        
        st.success(f"✅ Conversion complete! {original_format} → TOON")
        
    except Exception as e:
        st.error(f"❌ Error during conversion: {str(e)}")
        st.exception(e)

else:
    # Instructions
    st.info("""
    ### 🚀 Get Started
    
    1. **Upload a file** (JSON, CSV, Excel, YAML, XML, or TOML), or
    2. Click a **Sample Data** button to see a demo
    3. Adjust conversion options in the sidebar
    4. Download your optimized .toon file
    
    ### 💡 Supported Formats
    
    - **JSON** (.json) - Standard JSON format
    - **CSV** (.csv) - Comma-separated values
    - **Excel** (.xlsx, .xls) - Spreadsheets
    - **YAML** (.yaml, .yml) - YAML configuration files
    - **XML** (.xml) - Extensible markup
    - **TOML** (.toml) - Configuration format
    
    ### 🎯 Use Cases
    
    - Optimize LLM prompts with structured data
    - Reduce API token costs by 30-60%
    - Convert legacy formats for modern LLM workflows
    - Maximize context window efficiency
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    Multi-Format TOON Converter | 
    Made with <a href='https://streamlit.io'>Streamlit</a> | 
    <a href='https://github.com/johannschopplich/toon'>TOON Format</a>
</div>
""", unsafe_allow_html=True)