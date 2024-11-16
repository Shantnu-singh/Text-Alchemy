import streamlit as st
import pandas as pd
import summerise

# Page Configuration
st.set_page_config(
    page_title="Text Alchemy ✨",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .stTitle {
            font-size: 3rem !important;
            font-weight: 700 !important;
            color: #6C63FF !important;
            margin-bottom: 2rem !important;
        }
        .stMarkdown {
            font-size: 1.2rem !important;
        }
        .stButton button {
            width: 100%;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-size: 1.2rem;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .upload-section {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 2rem 0;
        }
        .summary-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #6C63FF;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("✨ Text Alchemy")
st.markdown("""
    <div style='background-color: #e6e6fa; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h3 style='color: #4B0082; margin-bottom: 0.5rem;'>Transform Your Text into Concise Summaries</h3>
        <p style='color: #483D8B;'>Upload your articles and let our AI magic create perfect summaries for you!</p>
    </div>
""", unsafe_allow_html=True)

# Constants
ARTICLE_LIMIT = 2

# Main content
with st.container():
    st.markdown("### 📄 Upload Your Articles")
    st.info("Please ensure your CSV file has the following columns: title | link | content", icon="ℹ️")
    
    # File upload section
    with st.expander("📥 Upload Section", expanded=True):
        upload_file = st.file_uploader(
            "Drop your CSV file here",
            type=['csv'],
            accept_multiple_files=False,
            key='uploaded_file'
        )

    # Generate button with loading animation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        genBut = st.button(
            "🚀 Generate Summaries",
            type="primary",
            use_container_width=True
        )

    # Processing and Results
    if genBut:
        if upload_file:
            with st.spinner('🔮 Magic in progress...'):
                try:
                    df = pd.read_csv(upload_file)
                    responses = []
                    
                    progress_bar = st.progress(0)
                    for i in range(ARTICLE_LIMIT):
                        response = summerise.give_responces(df.iloc[i, 2])
                        responses.append(response)
                        progress_bar.progress((i + 1) / ARTICLE_LIMIT)
                    
                    if responses:
                        st.success("✨ Summaries generated successfully!")
                        st.markdown("### 📚 Your Article Summaries")
                        
                        for i, resp in enumerate(responses, 1):
                            with st.container():
                                st.markdown(f"""
                                    <div class='summary-card'>
                                        <h4 style='color: #6C63FF;'>Article {i}</h4>
                                        <div style='margin-top: 1rem;color: #6C63FF'>{resp}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                except Exception as e:
                    st.error(f"⚠️ An error occurred: {str(e)}")
        else:
            st.warning("⚠️ Please upload a CSV file first!")

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 3rem; padding: 1rem; background-color: #f8f9fa; border-radius: 10px;'>
        <p style='color: #666; font-size: 0.9rem;'>Made with ❤️ by Shantnu - Prodigal AI</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. Prepare your CSV file with columns:
        - title
        - link
        - content
    2. Upload your file using the upload section
    3. Click 'Generate Summaries'
    4. View your beautifully summarized articles!
    """)
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    Text Alchemy transforms lengthy articles into 
    clear, concise summaries while maintaining 
    the essential information.
    """)