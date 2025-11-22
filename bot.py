import os
from uuid import uuid4

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# import fungsi generator dari all.py
from all import (
    generate_uk_card,
    generate_india_card,
    generate_bangladesh_receipt,
)

# ================== KONFIGURASI SIMPLE ==================

# Link channel / grup (ubah sesuai punya lu)
CHANNEL_URL = "https://t.me/VanzDisscusion"
GROUP_URL = "https://t.me/VANZSHOPGROUP"

# ================== STATE CONVERSATION ==================

(
    CHOOSING_TEMPLATE,
    # UK
    UK_NAME,
    UK_ID,
    UK_BIRTH,
    UK_ADDRESS,
    UK_ACTIVE,
    UK_PHOTO,
    # INDIA
    IN_IDNO,
    IN_CLASS,
    IN_DOB,
    IN_VALIDITY,
    IN_MOBILE,
    IN_PHOTO,
    # BANGLADESH
    BD_STUDENT_ROLL,
    BD_CENTRE,
    BD_REG_DATE,
    BD_NAME,
    BD_AMOUNT_NUMBER,
    BD_AMOUNT_WORDS,
    BD_INSTRUMENT_NO,
    BD_INSTRUMENT_DATE,
    BD_PAYMENT_TYPE,
    BD_BANK,
    BD_SESSION_TEXT,
) = range(24)


# ================== HANDLER /start ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Selamat datang di *VanzShop ID Card Bot!*\n\n"
        "Bikin ID Card otomatis dengan cepat.\n\n"
        "Pilih menu di bawah atau pakai perintah:\n"
        "• /card → Pilih template & buat 1 kartu\n"
        "• /batch → Buat banyak kartu sekaligus\n"
    )

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 Generate Card UK", callback_data="single_uk"),
            InlineKeyboardButton("🇮🇳 Generate Card India", callback_data="single_india"),
        ],
        [
            InlineKeyboardButton("🇧🇩 Generate Receipt BD", callback_data="single_bd"),
        ],
        [
            InlineKeyboardButton("📦 Batch Card UK", callback_data="batch_uk"),
            InlineKeyboardButton("📦 Batch Card India", callback_data="batch_india"),
        ],
        [
            InlineKeyboardButton("📢 Channel", url=CHANNEL_URL),
            InlineKeyboardButton("👥 Group", url=GROUP_URL),
        ],
    ]

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ================== /batch (placeholder) ==================

async def batch_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Fitur *batch* belum dibuat di versi ini.\n"
        "Sementara pakai /card dulu ya 👀",
        parse_mode="Markdown",
    )


# ================== /card: pilih template ==================

async def card_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 UK", callback_data="TPL_UK"),
            InlineKeyboardButton("🇮🇳 India", callback_data="TPL_IN"),
            InlineKeyboardButton("🇧🇩 Bangladesh", callback_data="TPL_BD"),
        ]
    ]
    await update.message.reply_text(
        "Pilih template kartu yang mau dibuat:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return CHOOSING_TEMPLATE


async def card_from_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Masuk flow /card tapi dari tombol di /start."""
    query = update.callback_query
    await query.answer()

    data = query.data  # single_uk, single_india, single_bd
    if data == "single_uk":
        context.user_data["template"] = "UK"
        await query.message.reply_text("🇬🇧 *Kartu UK*\n\nMasukin *Nama lengkap*:", parse_mode="Markdown")
        return UK_NAME

    if data == "single_india":
        context.user_data["template"] = "INDIA"
        await query.message.reply_text("🇮🇳 *Kartu India*\n\nMasukin *ID No*:", parse_mode="Markdown")
        return IN_IDNO

    if data == "single_bd":
        context.user_data["template"] = "BD"
        await query.message.reply_text("🇧🇩 *Fee Receipt Bangladesh*\n\nMasukin *Student Roll no*:", parse_mode="Markdown")
        return BD_STUDENT_ROLL

    # fallback
    await query.message.reply_text("Pilihan tidak dikenal.")
    return ConversationHandler.END


async def template_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dipanggil kalau user pilih template lewat /card."""
    query = update.callback_query
    await query.answer()

    tpl = query.data  # TPL_UK / TPL_IN / TPL_BD
    if tpl == "TPL_UK":
        context.user_data["template"] = "UK"
        await query.message.reply_text("🇬🇧 *Kartu UK*\n\nMasukin *Nama lengkap*:", parse_mode="Markdown")
        return UK_NAME

    if tpl == "TPL_IN":
        context.user_data["template"] = "INDIA"
        await query.message.reply_text("🇮🇳 *Kartu India*\n\nMasukin *ID No*:", parse_mode="Markdown")
        return IN_IDNO

    if tpl == "TPL_BD":
        context.user_data["template"] = "BD"
        await query.message.reply_text("🇧🇩 *Fee Receipt Bangladesh*\n\nMasukin *Student Roll no*:", parse_mode="Markdown")
        return BD_STUDENT_ROLL

    await query.message.reply_text("Pilihan tidak dikenal.")
    return ConversationHandler.END


# ================== FLOW KARTU UK ==================

async def uk_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["uk_name"] = update.message.text
    await update.message.reply_text("Masukin *Student ID*:", parse_mode="Markdown")
    return UK_ID


async def uk_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["uk_id"] = update.message.text
    await update.message.reply_text("Masukin *Tanggal lahir* (contoh: 10/10/2005):", parse_mode="Markdown")
    return UK_BIRTH


async def uk_birth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["uk_birth"] = update.message.text
    await update.message.reply_text("Masukin *Alamat* (contoh: London, UK):", parse_mode="Markdown")
    return UK_ADDRESS


async def uk_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["uk_address"] = update.message.text
    await update.message.reply_text("Masukin *Active until* (contoh: 06/2028):", parse_mode="Markdown")
    return UK_ACTIVE


async def uk_active(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["uk_active"] = update.message.text
    await update.message.reply_text("Kirim *foto* untuk dimasukin ke kartu (kirim sebagai foto, bukan file).",
                                    parse_mode="Markdown")
    return UK_PHOTO


async def uk_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    tmp_photo = f"uk_photo_{uuid4().hex}.jpg"
    await file.download_to_drive(tmp_photo)

    data = context.user_data
    out_path = f"uk_card_{uuid4().hex}.png"

    try:
        generate_uk_card(
            name=data["uk_name"],
            student_id=data["uk_id"],
            birth=data["uk_birth"],
            address=data["uk_address"],
            active_until=data["uk_active"],
            photo_path=tmp_photo,
            out_path=out_path,
        )
        with open(out_path, "rb") as img:
            await update.message.reply_photo(
                img,
                caption="✅ Kartu UK berhasil dibuat.",
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal generate kartu UK.\nError: {e}")
    finally:
        if os.path.exists(tmp_photo):
            os.remove(tmp_photo)
        if os.path.exists(out_path):
            os.remove(out_path)
        context.user_data.clear()

    return ConversationHandler.END


# ================== FLOW KARTU INDIA ==================

async def in_idno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["in_idno"] = update.message.text
    await update.message.reply_text("Masukin *Class* (contoh: ECE):", parse_mode="Markdown")
    return IN_CLASS


async def in_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["in_class"] = update.message.text
    await update.message.reply_text("Masukin *D.O.B* (contoh: 15/01/2000):", parse_mode="Markdown")
    return IN_DOB


async def in_dob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["in_dob"] = update.message.text
    await update.message.reply_text("Masukin *Validity* (contoh: 11/25 - 11/26):", parse_mode="Markdown")
    return IN_VALIDITY


async def in_validity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["in_validity"] = update.message.text
    await update.message.reply_text("Masukin *Mobile* (contoh: +917546728719):", parse_mode="Markdown")
    return IN_MOBILE


async def in_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["in_mobile"] = update.message.text
    await update.message.reply_text("Kirim *foto* untuk dimasukin ke kartu (kirim sebagai foto, bukan file).",
                                    parse_mode="Markdown")
    return IN_PHOTO


async def in_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    tmp_photo = f"in_photo_{uuid4().hex}.jpg"
    await file.download_to_drive(tmp_photo)

    data = context.user_data
    out_path = f"india_card_{uuid4().hex}.png"

    try:
        generate_india_card(
            id_no=data["in_idno"],
            class_name=data["in_class"],
            dob=data["in_dob"],
            validity=data["in_validity"],
            mobile=data["in_mobile"],
            photo_path=tmp_photo,
            out_path=out_path,
        )
        with open(out_path, "rb") as img:
            await update.message.reply_photo(
                img,
                caption="✅ Kartu India berhasil dibuat.",
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal generate kartu India.\nError: {e}")
    finally:
        if os.path.exists(tmp_photo):
            os.remove(tmp_photo)
        if os.path.exists(out_path):
            os.remove(out_path)
        context.user_data.clear()

    return ConversationHandler.END


# ================== FLOW BANGLADESH RECEIPT ==================

async def bd_student_roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_student_roll"] = update.message.text
    await update.message.reply_text("Masukin *Centre*:", parse_mode="Markdown")
    return BD_CENTRE


async def bd_centre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_centre"] = update.message.text
    await update.message.reply_text("Masukin *Registration Date* (contoh: 14.10.25):", parse_mode="Markdown")
    return BD_REG_DATE


async def bd_reg_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_reg_date"] = update.message.text
    await update.message.reply_text("Masukin *Name*:", parse_mode="Markdown")
    return BD_NAME


async def bd_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_name"] = update.message.text
    await update.message.reply_text("Masukin *Amount angka* (contoh: 18500):", parse_mode="Markdown")
    return BD_AMOUNT_NUMBER


async def bd_amount_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_amount_number"] = update.message.text
    await update.message.reply_text("Masukin *Amount dalam kata* (contoh: Eighteen thousand ...):",
                                    parse_mode="Markdown")
    return BD_AMOUNT_WORDS


async def bd_amount_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_amount_words"] = update.message.text
    await update.message.reply_text("Masukin *Instrument No*:", parse_mode="Markdown")
    return BD_INSTRUMENT_NO


async def bd_instr_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_instr_no"] = update.message.text
    await update.message.reply_text("Masukin *Instrument Date* (contoh: 14.10.25):", parse_mode="Markdown")
    return BD_INSTRUMENT_DATE


async def bd_instr_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_instr_date"] = update.message.text
    await update.message.reply_text("Masukin *Payment Type* (contoh: BDT):", parse_mode="Markdown")
    return BD_PAYMENT_TYPE


async def bd_payment_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_payment_type"] = update.message.text
    await update.message.reply_text("Masukin *Bank* (contoh: Islami Bank):", parse_mode="Markdown")
    return BD_BANK


async def bd_bank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_bank"] = update.message.text
    await update.message.reply_text("Masukin *teks session* (contoh: tuition fees of 1st semester ...):",
                                    parse_mode="Markdown")
    return BD_SESSION_TEXT


async def bd_session_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["bd_session_text"] = update.message.text

    data = context.user_data
    out_path = f"bd_receipt_{uuid4().hex}.png"

    try:
        generate_bangladesh_receipt(
            student_roll=data["bd_student_roll"],
            centre=data["bd_centre"],
            registration_date=data["bd_reg_date"],
            name=data["bd_name"],
            amount_number=data["bd_amount_number"],
            amount_words=data["bd_amount_words"],
            instrument_no=data["bd_instr_no"],
            instrument_date=data["bd_instr_date"],
            payment_type=data["bd_payment_type"],
            bank=data["bd_bank"],
            session_text=data["bd_session_text"],
            out_path=out_path,
        )
        with open(out_path, "rb") as img:
            await update.message.reply_photo(
                img,
                caption="✅ Fee receipt Bangladesh berhasil dibuat.",
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal generate receipt BD.\nError: {e}")
    finally:
        if os.path.exists(out_path):
            os.remove(out_path)
        context.user_data.clear()

    return ConversationHandler.END


# ================== /cancel ==================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("❌ Proses dibatalkan.")
    return ConversationHandler.END


# ================== MAIN ==================

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable belum di-set.")

    app = ApplicationBuilder().token(token).build()

    # /start & /batch
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("batch", batch_cmd))

    # Conversation untuk /card
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("card", card_cmd),
            CallbackQueryHandler(card_from_start_button, pattern="^single_"),
        ],
        states={
            CHOOSING_TEMPLATE: [
                CallbackQueryHandler(template_chosen, pattern="^TPL_"),
            ],
            # UK
            UK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, uk_name)],
            UK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, uk_id)],
            UK_BIRTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, uk_birth)],
            UK_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, uk_address)],
            UK_ACTIVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, uk_active)],
            UK_PHOTO: [MessageHandler(filters.PHOTO, uk_photo)],
            # INDIA
            IN_IDNO: [MessageHandler(filters.TEXT & ~filters.COMMAND, in_idno)],
            IN_CLASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, in_class)],
            IN_DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, in_dob)],
            IN_VALIDITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, in_validity)],
            IN_MOBILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, in_mobile)],
            IN_PHOTO: [MessageHandler(filters.PHOTO, in_photo)],
            # BANGLADESH
            BD_STUDENT_ROLL: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_student_roll)],
            BD_CENTRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_centre)],
            BD_REG_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_reg_date)],
            BD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_name)],
            BD_AMOUNT_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_amount_number)],
            BD_AMOUNT_WORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_amount_words)],
            BD_INSTRUMENT_NO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_instr_no)],
            BD_INSTRUMENT_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_instr_date)],
            BD_PAYMENT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_payment_type)],
            BD_BANK: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_bank)],
            BD_SESSION_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bd_session_text)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)

    # jalanin bot
    app.run_polling()


if __name__ == "__main__":
    main()
