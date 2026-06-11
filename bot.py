
import logging
import os
import threading
from io import BytesIO
import pytesseract
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TOKEN = "8724911398:AAEbgd4qbg3dVxtv_Z0XoQSxtYySVZyey_A"

app = Flask(__name__)

@app.route("/health")
def health_check():
    return "OK", 200

def run_flask():
    app.run(host="0.0.0.0", port=10000)

async def start(update: Update, context) -> None:
    await update.message.reply_text("مرحباً بك! أرسل لي صورة وسأقوم باستخراج النص منها.")

async def ocr_image(update: Update, context) -> None:
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = BytesIO()
        await photo_file.download_to_memory(photo_bytes)
        photo_bytes.seek(0)
        img = Image.open(photo_bytes)
        text = pytesseract.image_to_string(img, lang='ara+eng')
        if text.strip():
            await update.message.reply_text(f"النص المستخرج:\n{text}")
        else:
            await update.message.reply_text("لم يتم العثور على نص في الصورة.")
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        await update.message.reply_text("حدث خطأ أثناء معالجة الصورة. يرجى المحاولة مرة أخرى.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, ocr_image))
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()


