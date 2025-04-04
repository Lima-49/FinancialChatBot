from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Substitua pelo seu token do BotFather
TOKEN = "8101413795:AAGlgW2kR8NCJF0kgKqGKbTIhjotCxe_zyY"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Olá! Eu sou um bot do Telegram.")

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot iniciado...")
    app.run_pollling()

if __name__ == "__main__":
    main()
