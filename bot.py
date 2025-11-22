import os
from uuid import uuid4

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
)

# 🔥 Ambil token dari ENV (Railway Variable: BOT_TOKEN)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Import generator dari all.py
from all import (
    generate_uk_card,
    generate_india_card,
    generate_bangladesh_receipt,
)

# ================== KONFIGURASI ==================

CHANNEL_URL = "https://t.me/VanzDisscusion"
GROUP_URL = "https://t.me/VANZSHOPGROUP"

# ================== STATE ==================

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

def start(update: Update, context: CallbackContext):
    text = (
        "👋 Selamat datang di *VanzShop ID Card Bot!*\n\n"
        "Pilih kartu yang mau dibuat:\n"
        "• /card → Pilih template & buat 1 kartu\n"
    )

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 Card UK", callback_data="single_uk"),
            InlineKeyboardButton("🇮🇳 Card India", callback_data="single_india"),
        ],
        [
            InlineKeyboardButton("🇧🇩 Receipt BD", callback_data="single_bd"),
        ],
        [
            InlineKeyboardButton("📢 Channel", url=CHANNEL_URL),
            InlineKeyboardButton("👥 Group", url=GROUP_URL),
        ],
    ]

    update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ================== /card: pilih template ==================

def card_cmd(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 UK", callback_data="TPL_UK"),
            InlineKeyboardButton("🇮🇳 India", callback_data="TPL_IN"),
            InlineKeyboardButton("🇧🇩 Bangladesh", callback_data="TPL_BD"),
        ]
    ]
    update.message.reply_text(
        "Pilih template kartu:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return CHOOSING_TEMPLATE


def card_from_start_button(update: Update, context: CallbackContext):
    """Masuk flow dari tombol di /start."""
    query = update.callback_query
    query.answer()

    data = query.data
    if data == "single_uk":
        context.user_data["template"] = "UK"
        query.message.reply_text("🇬🇧 *Kartu UK*\n\nMasukkan *Nama lengkap*:", parse_mode="Markdown")
        return UK_NAME

    if data == "single_india":
        context.user_data["template"] = "INDIA"
        query.message.reply_text("🇮🇳 *Kartu India*\n\nMasukkan *ID No*:", parse_mode="Markdown")
        return IN_IDNO

    if data == "single_bd":
        context.user_data["template"] = "BD"
        query.message.reply_text("🇧🇩 *Fee Receipt Bangladesh*\n\nMasukkan *Student Roll no*:", parse_mode="Markdown")
        return BD_STUDENT_ROLL

    query.message.reply_text("Pilihan tidak dikenal.")
    return ConversationHandler.END


def template_chosen(update: Update, context: CallbackContext):
    """Dipanggil kalau user pilih template lewat /card."""
    query = update.callback_query
    query.answer()

    tpl = query.data
    if tpl == "TPL_UK":
        context.user_data["template"] = "UK"
        query.message.reply_text("🇬🇧 *Kartu UK*\n\nMasukkan *Nama lengkap*:", parse_mode="Markdown")
        return UK_NAME

    if tpl == "TPL_IN":
        context.user_data["template"] = "INDIA"
        query.message.reply_text("🇮🇳 *Kartu India*\n\nMasukkan *ID No*:", parse_mode="Markdown")
        return IN_IDNO

    if tpl == "TPL_BD":
        context.user_data["template"] = "BD"
        query.message.reply_text("🇧🇩 *Fee Receipt Bangladesh*\n\nMasukkan *Student Roll no*:", parse_mode="Markdown")
        return BD_STUDENT_ROLL

    query.message.reply_text("Pilihan tidak dikenal.")
    return ConversationHandler.END


# ================== FLOW KARTU UK ==================

def uk_name(update: Update, context: CallbackContext):
    context.user_data["uk_name"] = update.message.text
    update.message.reply_text("Masukkan *Student ID*:", parse_mode="Markdown")
    return UK_ID


def uk_id(update: Update, context: CallbackContext):
    context.user_data["uk_id"] = update.message.text
    update.message.reply_text("Masukkan *Tanggal lahir* (contoh: 10/10/2005):", parse_mode="Markdown")
    return UK_BIRTH


def uk_birth(update: Update, context: CallbackContext):
    context.user_data["uk_birth"] = update.message.text
    update.message.reply_text("Masukkan *Alamat* (contoh: London, UK):", parse_mode="Markdown")
    return UK_ADDRESS


def uk_address(update: Update, context: CallbackContext):
    context.user_data["uk_address"] = update.message.text
    update.message.reply_text("Masukkan *Active until* (contoh: 06/2028):", parse_mode="Markdown")
    return UK_ACTIVE


def uk_active(update: Update, context: CallbackContext):
    context.user_data["uk_active"] = update.message.text
    update.message.reply_text("Kirim *foto* untuk dimasukin ke kartu (kirim sebagai foto, bukan file).",
                              parse_mode="Markdown")
    return UK_PHOTO


def uk_photo(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]
    file = photo.get_file()

    tmp_photo = f"uk_photo_{uuid4().hex}.jpg"
    file.download(tmp_photo)

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
            update.message.reply_photo(
                img,
                caption="✅ Kartu UK berhasil dibuat.",
            )
    except Exception as e:
        update.message.reply_text(f"❌ Gagal generate kartu UK.\nError: {e}")
    finally:
        if os.path.exists(tmp_photo):
            os.remove(tmp_photo)
        if os.path.exists(out_path):
            os.remove(out_path)
        context.user_data.clear()

    return ConversationHandler.END


# ================== FLOW KARTU INDIA ==================

def in_idno(update: Update, context: CallbackContext):
    context.user_data["in_idno"] = update.message.text
    update.message.reply_text("Masukkan *Class* (contoh: ECE):", parse_mode="Markdown")
    return IN_CLASS


def in_class(update: Update, context: CallbackContext):
    context.user_data["in_class"] = update.message.text
    update.message.reply_text("Masukkan *D.O.B* (contoh: 15/01/2000):", parse_mode="Markdown")
    return IN_DOB


def in_dob(update: Update, context: CallbackContext):
    context.user_data["in_dob"] = update.message.text
    update.message.reply_text("Masukkan *Validity* (contoh: 11/25 - 11/26):", parse_mode="Markdown")
    return IN_VALIDITY


def in_validity(update: Update, context: CallbackContext):
    context.user_data["in_validity"] = update.message.text
    update.message.reply_text("Masukkan *Mobile* (contoh: +917546728719):", parse_mode="Markdown")
    return IN_MOBILE


def in_mobile(update: Update, context: CallbackContext):
    context.user_data["in_mobile"] = update.message.text
    update.message.reply_text("Kirim *foto* untuk dimasukin ke kartu (kirim sebagai foto, bukan file).",
                              parse_mode="Markdown")
    return IN_PHOTO


def in_photo(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]
    file = photo.get_file()

    tmp_photo = f"in_photo_{uuid4().hex}.jpg"
    file.download(tmp_photo)

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
            update.message.reply_photo(
                img,
                caption="✅ Kartu India berhasil dibuat.",
            )
    except Exception as e:
        update.message.reply_text(f"❌ Gagal generate kartu India.\nError: {e}")
    finally:
        if os.path.exists(tmp_photo):
            os.remove(tmp_photo)
        if os.path.exists(out_path):
            os.remove(out_path)
        context.user_data.clear()

    return ConversationHandler.END


# ================== FLOW BANGLADESH RECEIPT ==================

def bd_student_roll(update: Update, context: CallbackContext):
    context.user_data["bd_student_roll"] = update.message.text
    update.message.reply_text("Masukkan *Centre*:", parse_mode="Markdown")
    return BD_CENTRE


def bd_centre(update: Update, context: CallbackContext):
    context.user_data["bd_centre"] = update.message.text
    update.message.reply_text("Masukkan *Registration Date* (contoh: 14.10.25):", parse_mode="Markdown")
    return BD_REG_DATE


def bd_reg_date(update: Update, context: CallbackContext):
    context.user_data["bd_reg_date"] = update.message.text
    update.message.reply_text("Masukkan *Name*:", parse_mode="Markdown")
    return BD_NAME


def bd_name(update: Update, context: CallbackContext):
    context.user_data["bd_name"] = update.message.text
    update.message.reply_text("Masukkan *Amount angka* (contoh: 18500):", parse_mode="Markdown")
    return BD_AMOUNT_NUMBER


def bd_amount_number(update: Update, context: CallbackContext):
    context.user_data["bd_amount_number"] = update.message.text
    update.message.reply_text("Masukkan *Amount dalam kata* (contoh: Eighteen thousand ...):",
                              parse_mode="Markdown")
    return BD_AMOUNT_WORDS


def bd_amount_words(update: Update, context: CallbackContext):
    context.user_data["bd_amount_words"] = update.message.text
    update.message.reply_text("Masukkan *Instrument No*:", parse_mode="Markdown")
    return BD_INSTRUMENT_NO


def bd_instr_no(update: Update, context: CallbackContext):
    context.user_data["bd_instr_no"] = update.message.text
    update.message.reply_text("Masukkan *Instrument Date* (contoh: 14.10.25):", parse_mode="Markdown")
    return BD_INSTRUMENT_DATE


def bd_instr_date(update: Update, context: CallbackContext):
    context.user_data["bd_instr_date"] = update.message.text
    update.message.reply_text("Masukkan *Payment Type* (contoh: BDT):", parse_mode="Markdown")
    return BD_PAYMENT_TYPE


def bd_payment_type(update: Update, context: CallbackContext):
    context.user_data["bd_payment_type"] = update.message.text
    update.message.reply_text("Masukkan *Bank* (contoh: Islami Bank):", parse_mode="Markdown")
    return BD_BANK


def bd_bank(update: Update, context: CallbackContext):
    context.user_data["bd_bank"] = update.message.text
    update.message.reply_text("Masukkan *teks session* (contoh: tuition fees of 1st semester ...):",
                              parse_mode="Markdown")
    return BD_SESSION_TEXT


def bd_session_text(update: Update, context: CallbackContext):
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
            update.message.reply_photo(
                img,
                caption="✅ Fee receipt Bangladesh berhasil dibuat.",
            )
    except Exception as e:
        update.message.reply_text(f"❌ Gagal generate receipt BD.\nError: {e}")
    finally:
        if os.path.exists(out_path):
            os.remove(out_path)
        context.user_data.clear()

    return ConversationHandler.END


# ================== /cancel ==================

def cancel(update: Update, context: CallbackContext):
    context.user_data.clear()
    update.message.reply_text("❌ Proses dibatalkan.")
    return ConversationHandler.END


# ================== MAIN ==================

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable belum di-set.")

    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # /start
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("card", card_cmd))

    # Conversation untuk semua flow
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
            UK_NAME: [MessageHandler(Filters.text & ~Filters.command, uk_name)],
            UK_ID: [MessageHandler(Filters.text & ~Filters.command, uk_id)],
            UK_BIRTH: [MessageHandler(Filters.text & ~Filters.command, uk_birth)],
            UK_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, uk_address)],
            UK_ACTIVE: [MessageHandler(Filters.text & ~Filters.command, uk_active)],
            UK_PHOTO: [MessageHandler(Filters.photo, uk_photo)],
            # INDIA
            IN_IDNO: [MessageHandler(Filters.text & ~Filters.command, in_idno)],
            IN_CLASS: [MessageHandler(Filters.text & ~Filters.command, in_class)],
            IN_DOB: [MessageHandler(Filters.text & ~Filters.command, in_dob)],
            IN_VALIDITY: [MessageHandler(Filters.text & ~Filters.command, in_validity)],
            IN_MOBILE: [MessageHandler(Filters.text & ~Filters.command, in_mobile)],
            IN_PHOTO: [MessageHandler(Filters.photo, in_photo)],
            # BANGLADESH
            BD_STUDENT_ROLL: [MessageHandler(Filters.text & ~Filters.command, bd_student_roll)],
            BD_CENTRE: [MessageHandler(Filters.text & ~Filters.command, bd_centre)],
            BD_REG_DATE: [MessageHandler(Filters.text & ~Filters.command, bd_reg_date)],
            BD_NAME: [MessageHandler(Filters.text & ~Filters.command, bd_name)],
            BD_AMOUNT_NUMBER: [MessageHandler(Filters.text & ~Filters.command, bd_amount_number)],
            BD_AMOUNT_WORDS: [MessageHandler(Filters.text & ~Filters.command, bd_amount_words)],
            BD_INSTRUMENT_NO: [MessageHandler(Filters.text & ~Filters.command, bd_instr_no)],
            BD_INSTRUMENT_DATE: [MessageHandler(Filters.text & ~Filters.command, bd_instr_date)],
            BD_PAYMENT_TYPE: [MessageHandler(Filters.text & ~Filters.command, bd_payment_type)],
            BD_BANK: [MessageHandler(Filters.text & ~Filters.command, bd_bank)],
            BD_SESSION_TEXT: [MessageHandler(Filters.text & ~Filters.command, bd_session_text)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv)

    # Jalanin bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
