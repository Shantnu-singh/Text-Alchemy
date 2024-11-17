import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup , ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import Updater , CommandHandler , ContextTypes , ApplicationBuilder, ConversationHandler, MessageHandler, filters
from summerise import give_responces

load_dotenv()
token = os.getenv("TELEGRAM_BOT_API")
WATING_FOR_TEXT = 1 

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Welcome to TextSummarizer AI!\n\n"
        "✨ We specialize in transforming lengthy texts into clear, "
        "concise summaries using state-of-the-art AI technology. "
        "Let us help you save time and extract key insights from your content. 📚✍️"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🌟 Welcome aboard, {update._effective_user.first_name}!\n\n"
        "Thank you for choosing TextSummarizer AI. We're here to make your "
        "reading experience more efficient and productive.\n\n"
        "🚀 To begin, simply use the /summarize command followed by your text.\n\n"
        "Need help? Type /help for a complete list of commands. 💡"
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📚 Available Commands:\n\n"
        "🔹 /start - Initialize TextSummarizer AI\n"
        "🔹 /hello - Learn about our capabilities\n"
        "🔹 /help - View all available commands\n"
        "🔹 /summarize - Generate a concise summary of your text\n\n"
        "💫 For optimal results, ensure your text is clear and well-formatted.\n"
        "📧 Questions or feedback? Contact our support team at singhshantnu2001.bot@gmail.com"
    )

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "📝 Ready to create your summary!\n\n"
        "Please share the text you'd like to analyze. For optimal results:\n"
        "• Maximum length: 6000 words\n"
        "• Any language supported\n"
        "• Plain text format preferred\n\n"
        "⚡ Our AI will process your text instantly! 🔄"
    )
    return WATING_FOR_TEXT

async def action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text_input = update.message.text
    try:
        response = give_responces(text_input)
        await update.message.reply_text(
            "🎯 Summary Generated Successfully!\n\n"
            f"{response}\n\n"
            "📊 Want to summarize another text? Just send it over!\n"
            "💡 Tip: Use /help to explore more features."
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        await update.message.reply_text(
            "⚠️ Oops! We encountered an issue while processing your request.\n\n"
            "This might be due to:\n"
            "• Text exceeding length limit\n"
            "• Unsupported formatting\n"
            "• Temporary service disruption\n\n"
            "🔄 Please try again or contact our support if the issue persists."
        )
        
    return ConversationHandler.END

async def cancel(update: Update ,context:ContextTypes.DEFAULT_TYPE)->int:
    await update.message.reply_text(
                "❌ Text summarization canceled.\n"
                "Use /summarize when you're ready to try again!"
            )
    return ConversationHandler.END
    
Conv_handler = ConversationHandler(
    entry_points= [CommandHandler("summarize" , summarize)],
    states={
        WATING_FOR_TEXT:[
            MessageHandler(filters.TEXT & ~filters.COMMAND , action), CommandHandler('cancel' , cancel)
        ]
    },
    fallbacks= [CommandHandler('cancel' , cancel)]   
)    

async def send_message(update: Update , context: ContextTypes.DEFAULT_TYPE)->None:
    if context.args: 
        custom_message = " ".join(context.args)
        await update.message.reply_text(f"you send {custom_message} ")
    else:
        await update.message.reply_text("⚠️ Something Went wrong try on more time....")
        
        
         
def main():
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello" , hello))
    app.add_handler(CommandHandler("help" , help))
    app.add_handler(CommandHandler("start" , start))
    app.add_handler(Conv_handler)
    app.add_handler(CommandHandler("sendmessage", send_message))
    app.run_polling()
    
if __name__ == "__main__":
    main()


