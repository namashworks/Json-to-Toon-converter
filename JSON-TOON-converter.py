import streamlit as st
import json
from io import BytesIO
import sys

# Note: You need to install python-toon first
# pip install python-toon
try:
    from toon import encode
except ImportError:
    st.error("⚠️ python-toon library not installed. Please run: pip install python-toon")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="JSON to TOON Converter",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎒 JSON to TOON Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Token-Oriented Object Notation – Reduce LLM token costs by 30-60%</div>', unsafe_allow_html=True)

# Sidebar - Information
with st.sidebar:
    st.header("ℹ️ About TOON")
    st.markdown("""
    **TOON** (Token-Oriented Object Notation) is a compact, human-readable format designed for passing structured data to Large Language Models with significantly reduced token usage.
    
    **Key Features:**
    - 🎯 30-60% token reduction vs JSON
    - 📊 Tabular format for uniform arrays
    - 🌳 YAML-like indentation for nested objects
    - ✅ LLM-friendly with explicit length markers
    
    **Best for:**
    - Uniform arrays of objects
    - Tabular data with repeated structure
    - LLM prompt optimization
    
    **Not ideal for:**
    - Deeply nested structures
    - Non-uniform data
    """)
    
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
                                   help="Add # prefix to array lengths for validation")
    
    st.divider()
    
    st.markdown("""
    **Resources:**
    - [TOON Specification](https://github.com/johannschopplich/toon/blob/main/SPEC.md)
    - [Python Implementation](https://github.com/xaviviro/python-toon)
    - [Original TOON (TypeScript)](https://github.com/johannschopplich/toon)
    """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Upload JSON File")
    uploaded_file = st.file_uploader(
        "Choose a JSON file",
        type=['json'],
        help="Upload a .json file to convert to TOON format"
    )
    
    # Sample data option
    if st.button("📝 Load Sample Data"):
        sample_data = {
            "metadata": {
                "version": "1.0",
                "author": "Sample User",
                "created": "2025-01-15"
            },
            "users": [
                {"id": 1, "name": "Alice Johnson", "age": 30, "role": "admin", "active": True},
                {"id": 2, "name": "Bob Smith", "age": 25, "role": "user", "active": True},
                {"id": 3, "name": "Charlie Brown", "age": 35, "role": "moderator", "active": False},
                {"id": 4, "name": "Diana Prince", "age": 28, "role": "user", "active": True}
            ],
            "tags": ["production", "verified", "enterprise"],
            "config": {
                "timeout": 3000,
                "retries": 3,
                "enableCache": True
            }
        }
        st.session_state['sample_data'] = sample_data
        st.success("✅ Sample data loaded!")

with col2:
    st.subheader("📤 Download TOON File")
    st.info("Upload a JSON file or load sample data to see the conversion")

# Process the file
if uploaded_file is not None or 'sample_data' in st.session_state:
    
    # Load JSON data
    try:
        if uploaded_file is not None:
            json_data = json.load(uploaded_file)
            file_name = uploaded_file.name.rsplit('.', 1)[0]
        else:
            json_data = st.session_state['sample_data']
            file_name = "sample"
        
        # Create encoding options
        encode_options = {
            "indent": indent_size,
            "delimiter": delimiter,
            "lengthMarker": "#" if use_length_marker else False
        }
        
        # Convert to TOON
        toon_output = encode(json_data, encode_options)
        
        # Calculate statistics
        json_str = json.dumps(json_data, indent=2)
        json_size = len(json_str)
        toon_size = len(toon_output)
        reduction = 100 * (1 - toon_size / json_size)
        
        # Display results in tabs
        tab1, tab2, tab3 = st.tabs(["📊 Comparison", "📄 Original JSON", "🎒 TOON Output"])
        
        with tab1:
            # Metrics
            col_m1, col_m2, col_m3 = st.columns(3)
            
            with col_m1:
                st.metric(
                    label="JSON Size",
                    value=f"{json_size} chars",
                    delta=None
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
            
            import pandas as pd
            df = pd.DataFrame({
                'Format': ['JSON', 'TOON'],
                'Size (characters)': [json_size, toon_size]
            })
            
            st.bar_chart(df.set_index('Format'))
            
            # Explanation
            st.info(f"""
            **🎯 Token Efficiency Analysis:**
            
            Your JSON file has been converted to TOON format with a **{reduction:.1f}% reduction** in size.
            
            - **Original JSON:** {json_size} characters
            - **TOON Format:** {toon_size} characters
            - **Savings:** {json_size - toon_size} characters
            
            This size reduction typically translates to similar token savings when used with LLM APIs, 
            potentially reducing costs and improving context window efficiency.
            """)
        
        with tab2:
            st.code(json_str, language='json')
            
            # Download JSON
            json_bytes = json_str.encode('utf-8')
            st.download_button(
                label="⬇️ Download JSON",
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
        
        # Success message
        st.success(f"✅ Conversion complete! Your .toon file is ready for download.")
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON file: {str(e)}")
    except Exception as e:
        st.error(f"❌ Error during conversion: {str(e)}")
        st.exception(e)

else:
    # Instructions when no file is uploaded
    st.info("""
    ### 🚀 Get Started
    
    1. **Upload a JSON file** using the file uploader above, or
    2. Click **"Load Sample Data"** to see a demo conversion
    3. Adjust conversion options in the sidebar (optional)
    4. View the comparison and download your .toon file
    
    ### 💡 Use Cases
    
    - **Optimize LLM prompts**: Reduce token costs for API calls
    - **Efficient data transfer**: Send structured data to language models
    - **Context window optimization**: Fit more data in limited context
    
    ### 📚 Example
    
    **JSON (177 characters):**
    ```json
    {"users": [
      {"id": 1, "name": "Alice", "age": 30},
      {"id": 2, "name": "Bob", "age": 25}
    ]}
    ```
    
    **TOON (85 characters - 52% reduction):**
    ```
    users[2,]{id,name,age}:
    1,Alice,30
    2,Bob,25
    ```
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    Made with ❤️ using <a href='https://streamlit.io'>Streamlit</a> | 
    <a href='https://github.com/xaviviro/python-toon'>python-toon</a> | 
    <a href='https://github.com/johannschopplich/toon'>TOON Format</a>
</div>
""", unsafe_allow_html=True)