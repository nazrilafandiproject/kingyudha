from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from fuzzywuzzy import process

TOKEN = '6833237090:AAFDqANMM-UBEygaGPMXiioICIgrOuA0ML4'
BOT_USERNAME = '@ItsYessiGrossirBot'

# List to store user questions
user_questions = []

responses = {
    #sapaan
    'hai' 'hello' 'hi' 'p': 'Hello',
    'woy kutu loncat' : 'woy',
    
    #topik terkait toko
    'kapan toko akan tutup' 'toko kapan tutup' 'toko buka sampe kapan': 'Toko biasanya tutup pada pukul 19:00 WIB untuk Weekdays dan pukul 13:00 WIB untuk hari Minggu.',
    'siapa nama pemilik toko' 'ko ini punya siapa': 'Nama pemilik toko ini adalah Yulianti yang biasa dikenal oleh orang sekitar yaitu Yessi.',
    'kapan pesanan diantar' 'mana pesenan saya': 'Pesanan akan di antar minimal 10 menit setelah kamu memesan.',
    'apa saja produk sembako yang tersedia di toko ini?' 'di toko ini ada apa aja': 'Kami menyediakan berbagai produk sembako seperti beras, gula, minyak goreng, tepung, garam, telur, dan masih banyak lagi. Apakah Anda mencari produk tertentu?',
    'apakah ada beras organik di toko ini?' 'di toko ada beras putih ga': 'Ya, kami memiliki beras organik dalam berbagai jenis dan ukuran kemasan. Kamu bisa memilih antara beras merah, beras hitam, atau beras putih organik.',
    'berapa harga beras 5 kg di toko ini?' 'harga beras 5 kilo berapa': 'Nah, kalo kamu mau tau harga per karung atau per kg, kamu bisa menghubungi kontak yang tertera ya untuk bisa mendapatkan informasi harga secara real time.',
    'apakah bisa bayar dengan e-wallet?' 'bisa bayar transfer ga': 'Tentu, kami menerima pembayaran dengan berbagai e-wallet seperti GoPay dan OVO. Kamu juga bisa membayar dengan debit.',
    'apakah stok telur masih tersedia?' 'telor masih ada tah': 'Ya, stok telur kami saat ini masih tersedia. Namun, ketersediaan bisa berubah cepat, jadi sebaiknya segera datang atau hubungi kami untuk memastikan.',
    'minyak masih ada tah' 'apakah minyak masih ada?' : 'Ya, stok minyak masih banyak banget. Yuk!! segera di pesen secara delivery dengan menghubingi kontak atau bisa melalui toko secara langsung',
    'Bagaimana jika produk yang saya cari tidak tersedia?' 'kaya mana kalo saya mau beli tapi barangnya ga ada': 'Jika produk yang kamu cari gak ada, kamu bisa memesan terlebih dahulu. Kami sebisa mungkin akan memberitahu kamu saat produk tersebut sudah kembali tersedia di toko.',
    'pakah ada layanan pengantaran?' 'belanjaan bisa di anter ga': 'Ya, kami menyediakan layanan pengantaran untuk area tertentu. Kamu bisa memilih opsi pengantaran saat melakukan pembayaran online atau bertanya kepada ibu Yessi di toko untuk informasi lebih lanjut.',
    'bagaimana cara melakukan pemesanan online?' 'gimana cara mesennya': 'Kamu bisa melakukan pemesanan online melalui WhatsApp. Lalu list produk yang kamu inginkan pada kontak yang telah kami sediakan. Kami akan mengonfirmasi pesanan Anda melalui kontak anda.',
    'bagaimana jika saya ingin mengembalikan produk yang sudah dibeli?' 'cara balikin belanjaan': 'Jika Anda ingin mengembalikan produk, Anda bisa datang ke toko dengan membawa produk dan bukti pembelian dalam waktu 7 hari setelah pembelian. Syarat dan ketentuan berlaku, dan produk harus dalam kondisi baik dan belum digunakan.',
    
    'default': 'Program saya masih terbatas. Saya hanya dapat membantu anda melalui pertanyaan terkait toko ini :)'
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.first_name
    response = f'hello {user}! saya adalah bot Yessi Grosir. Ada yang bisa di bantu?'
    await update.message.reply_text(response)
    # await update.message.reply_text('Halo, saya adalah bot Yessi Grosir. saya akan membantu kamu jika ada yang membuatmu bingung.')

async def kontak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ketikan pertanyaan apa saja terkait toko ini.')

async def bantuan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ini adalah kustomisasi perintah bot')

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_diterima = update.message.text.lower()

    print('Text diterima: ', text_diterima)

    # Store the received text
    user_questions.append(text_diterima)

    # Use fuzzy matching to find the best response
    matched_response = process.extractOne(text_diterima, responses.keys(), score_cutoff=60)
    
    if matched_response:
        response_text = responses[matched_response[0]]
    else:
        response_text = responses['default']

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
