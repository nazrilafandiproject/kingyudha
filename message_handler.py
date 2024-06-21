import random
from fuzzywuzzy import process
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json

TOKEN = '6833237090:AAFDqANMM-UBEygaGPMXiioICIgrOuA0ML4'
BOT_USERNAME = '@ItsYessiGrossirBot'

# Load responses from JSON file
with open('response.json', 'r') as f:
    data = json.load(f)
    responses = data['responses']

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.first_name
    response = f'Selamat datang {user}! Ada yang bisa saya bantu?! saya adalah bot Yessi Grosir.'
    await update.message.reply_text(response)

async def kontak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Berikut adalah kontak yang dapat kamu hubungi untuk memesan belanjaan secara online.
                                    
WhatsApp : ''')

async def bantuan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ketik '/' lalu pilih opsi '/start' untuk memulai percakapan.")

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_diterima = update.message.text.lower()
    
    print('Text diterima: ', text_diterima)

    # Use fuzzy matching to find the best response
    matched_response = process.extractOne(text_diterima, responses.keys(), score_cutoff=86)
    
    if matched_response:
        response_options = responses[matched_response[0]]
        response_text = random.choice(response_options)
    else:
        response_options = responses['default']
        response_text = random.choice(response_options)

    await update.message.reply_text(response_text)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'error: {context.error}')

if __name__ == '__main__':
    print('Bot dimulai.....')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('kontak', kontak_command))
    app.add_handler(CommandHandler('bantuan', bantuan_command))

    app.add_handler(MessageHandler(filters.TEXT, text_message))

    app.add_error_handler(error)

    print('polling...')
    app.run_polling(poll_interval=1)
