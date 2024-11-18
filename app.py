import streamlit as st
import pandas as pd
import summerise
import bot
import telegram
import asyncio 
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler

# Initialize session state variables
if 'summaries' not in st.session_state:
    st.session_state.summaries = None
if 'df' not in st.session_state:
    st.session_state.df = None

def initialize_bot():
    """Initialize the bot without running it in the main event loop"""
    from bot import token, hello, help, start, Conv_handler, send_message
    
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(Conv_handler)
    app.add_handler(CommandHandler("sendmessage", send_message))
    return app

if "bot_app" not in st.session_state:
    st.session_state.bot_app = initialize_bot()

async def start_bot():
    try:
        await st.session_state.bot_app.initialize()
        await st.session_state.bot_app.start()
        await st.session_state.bot_app.run_polling()
    except Exception as e:
        st.error(f"Bot Error: {str(e)}")

# Run the bot in the background
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = True
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(start_bot())


# Page Configuration
st.set_page_config(
    page_title="Text Alchemy ✨",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
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
        .telegram-section {
            background-color: #f0f7ff;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            text-align: center;
            border: 2px solid #e1efff;
        }
        .telegram-link {
            display: inline-block;
            margin: 1rem 0;
            padding: 0.8rem 1.5rem;
            background-color: #0088cc;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        .telegram-link:hover {
            background-color: #006699;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .telegram-instructions {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
            border-left: 4px solid #0088cc;
        }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("✨ Text Alchemy ")
st.markdown("""
    <div style='background-color: #e6e6fa; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h3 style='color: #4B0082; margin-bottom: 0.5rem;'>Transform Your Text into Concise Summaries</h3>
        <p style='color: #483D8B;'>Upload your articles and let our AI magic create perfect summaries for you!</p>
    </div>
""", unsafe_allow_html=True)

ARTICLE_LIMIT = 1

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
        if st.button("🚀 Generate Summaries", type="primary", use_container_width=True):
            if upload_file:
                with st.spinner('🔮 Magic in progress...'):
                    try:
                        st.session_state.df = pd.read_csv(upload_file)
                        responses = []
                        
                        progress_bar = st.progress(0)
                        for i in range(ARTICLE_LIMIT):
                            response = summerise.give_responces(st.session_state.df.iloc[i, 2])
                            responses.append(response)
                            progress_bar.progress((i + 1) / ARTICLE_LIMIT)
                        
                        st.session_state.summaries = responses
                        # st.experimental_rerun()
                                    
                    except Exception as e:
                        st.error(f"⚠️ An error occurred: {str(e)}")
            else:
                st.warning("⚠️ Please upload a CSV file first!")

    # Display summaries if they exist in session state
    if st.session_state.summaries:
        st.success("✨ Summaries generated successfully!")
        st.markdown("### 📚 Your Article Summaries")
        
        for i, resp in enumerate(st.session_state.summaries, 1):
            with st.container():
                st.markdown(f"""
                    <div class='summary-card'>
                        <h4 style='color: #6C63FF;'>Article {i}</h4>
                        <div style='margin-top: 1rem;color: #6C63FF'>{resp}</div>
                    </div>
                """, unsafe_allow_html=True)
                
        colu1, colu2, colu3 = st.columns([1,2,1])
        with colu2:
            st.markdown("""
                <div class='telegram-section'>
                    <h3 style='color: #0088cc; margin-bottom: 1rem;'>📱 Continue on Telegram</h3>
                    <p style='color: #666; margin-bottom: 1.5rem;'>Get your summaries directly on Telegram for easier access and sharing!</p>
                </div>
            """, unsafe_allow_html=True)
            
            teleButton = st.button(
                "🤖 Open Telegram Bot",
                type="primary",
                use_container_width=True
            )

        if teleButton:
            url = "https://t.me/shantnu_prod_bot"
            st.markdown("""
                <div class='telegram-section'>
                    <h4 style='color: #0088cc; margin-bottom: 1rem;'>🎉 You're almost there!</h4>
                    <a href='{}' target='_blank' class='telegram-link'>
                        <i class='fab fa-telegram'></i> Open Telegram Bot
                    </a>
                </div>
            """.format(url), unsafe_allow_html=True)
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