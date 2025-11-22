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

# 🔥 AMBIL BOT TOKEN DARI RAILWAY ENV
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Generator dari all.py
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
    UK_NAME, UK_ID, UK_BIRTH, UK_ADDRESS, UK_ACTIVE, UK_PHOTO,
    IN_IDNO, IN_CLASS, IN_DOB, IN_VALIDITY, IN_MOBILE, IN_PHOTO,
    BD_STUDENT_ROLL, BD_CENTRE, BD_REG_DATE, BD_NAME,
    BD_AMOUNT_NUMBER, BD_AMOUNT_WORDS, BD_INSTRUMENT_NO,
    BD_INSTRUMENT_DATE, BD_PAYMENT_TYPE, BD_BANK, BD_SESSION_TEXT,
) = range(24)


# ================== /start ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Selamat datang di *VanzShop ID Card Bot!*\n\n"
        "Pilih kartu yang mau dibuat:"
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

    await update.message.reply_text(
        text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ================== /card ==================

async def card_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 UK", callback_data="TPL_UK"),
            InlineKeyboardButton("🇮🇳 India", callback_data="TPL_IN"),
            InlineKeyboardButton("🇧🇩 Bangladesh", callback_data="TPL_BD"),
        ]
    ]
    await update.message.reply_text(
        "Pilih template kartu:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return CHOOSING_TEMPLATE


async def card_from_start_button(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "single_uk":
        context.user_data["template"] = "UK"
        await query.message.reply_text("Masukkan *Nama Lengkap*:", parse_mode="Markdown")
        return UK_NAME

    if query.data == "single_india":
        context.user_data["template"] = "INDIA"
        await query.message.reply_text("Masukkan *ID No*:", parse_mode="Markdown")
        return IN_IDNO

    if query.data == "single_bd":
        context.user_data["template"] = "BD"
        await query.message.reply_text("Masukkan *Student Roll*:", parse_mode="Markdown")
        return BD_STUDENT_ROLL


async def template_chosen(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "TPL_UK":
        context.user_data["template"] = "UK"
        await query.message.reply_text("Masukkan *Nama*:", parse_mode="Markdown")
        return UK_NAME

    if query.data == "TPL_IN":
        context.user_data["template"] = "INDIA"
        await query.message.reply_text("Masukkan *ID No*:", parse_mode="Markdown")
        return IN_IDNO

    if query.data == "TPL_BD":
        context.user_data["template"] = "BD"
        await query.message.reply_text("Masukkan *Student Roll*:", parse_mode="Markdown")
        return BD_STUDENT_ROLL


# ================== FLOW UK ==================

async def uk_name(update, context):
    context.user_data["uk_name"] = update.message.text
    await update.message.reply_text("Masukkan *Student ID*:", parse_mode="Markdown")
    return UK_ID

async def uk_id(update, context):
    context.user_data["uk_id"] = update.message.text
    await update.message.reply_text("Masukkan *Tanggal Lahir*:", parse_mode="Markdown")
    return UK_BIRTH

async def uk_birth(update, context):
    context.user_data["uk_birth"] = update.message.text
    await update.message.reply_text("Masukkan *Alamat*:", parse_mode="Markdown")
    return UK_ADDRESS

async def uk_address(update, context):
    context.user_data["uk_address"] = update.message.text
    await update.message.reply_text("Masukkan *Active Until*:", parse_mode="Markdown")
    return UK_ACTIVE

async def uk_active(update, context):
    context.user_data["uk_active"] = update.message.text
    await update.message.reply_text("Kirim *foto* (bukan file):", parse_mode="Markdown")
    return UK_PHOTO

async def uk_photo(update, context):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    tmp = f"uk_{uuid4().hex}.jpg"
    await file.download_to_drive(tmp)

    data = context.user_data
    out = f"uk_card_{uuid4().hex}.png"

    try:
        generate_uk_card(
            name=data["uk_name"],
            student_id=data["uk_id"],
            birth=data["uk_birth"],
            address=data["uk_address"],
            active_until=data["uk_active"],
            photo_path=tmp,
            out_path=out
        )
        with open(out, "rb") as img:
            await update.message.reply_photo(img, caption="✅ Kartu UK jadi gan!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
    finally:
        for f in (tmp, out):
            if os.path.exists(f):
                os.remove(f)
        context.user_data.clear()

    return ConversationHandler.END


# ================== FLOW INDIA ==================

async def in_idno(update, context):
    context.user_data["in_idno"] = update.message.text
    await update.message.reply_text("Masukkan *Class*:", parse_mode="Markdown")
    return IN_CLASS

async def in_class(update, context):
    context.user_data["in_class"] = update.message.text
    await update.message.reply_text("Masukkan *D.O.B*:", parse_mode="Markdown")
    return IN_DOB

async def in_dob(update, context):
    context.user_data["in_dob"] = update.message.text
    await update.message.reply_text("Masukkan *Validity*:", parse_mode="Markdown")
    return IN_VALIDITY

async def in_validity(update, context):
    context.user_data["in_validity"] = update.message.text
    await update.message.reply_text("Masukkan *Mobile*:", parse_mode="Markdown")
    return IN_MOBILE

async def in_mobile(update, context):
    context.user_data["in_mobile"] = update.message.text
    await update.message.reply_text("Kirim *foto* (bukan file):", parse_mode="Markdown")
    return IN_PHOTO

async def in_photo(update, context):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    tmp = f"in_{uuid4().hex}.jpg"
    await file.download_to_drive(tmp)

    data = context.user_data
    out = f"india_{uuid4().hex}.png"

    try:
        generate_india_card(
            id_no=data["in_idno"],
            class_name=data["in_class"],
            dob=data["in_dob"],
            validity=data["in_validity"],
            mobile=data["in_mobile"],
            photo_path=tmp,
            out_path=out
        )
        with open(out, "rb") as img:
            await update.message.reply_photo(img, caption="✅ Kartu India jadi!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
    finally:
        for f in (tmp, out):
            if os.path.exists(f):
                os.remove(f)
        context.user_data.clear()

    return ConversationHandler.END


# ================== FLOW BANGLADESH ==================

async def bd_student_roll(update, context):
    context.user_data["bd_student_roll"] = update.message.text
    await update.message.reply_text("Masukkan *Centre*:")
    return BD_CENTRE

async def bd_centre(update, context):
    context.user_data["bd_centre"] = update.message.text
    await update.message.reply_text("Masukkan *Registration Date*:")
    return BD_REG_DATE

async def bd_reg_date(update, context):
    context.user_data["bd_reg_date"] = update.message.text
    await update.message.reply_text("Masukkan *Name*:")
    return BD_NAME

async def bd_name(update, context):
    context.user_data["bd_name"] = update.message.text
    await update.message.reply_text("Masukkan *Amount Number*:")
    return BD_AMOUNT_NUMBER

async def bd_amount_number(update, context):
    context.user_data["bd_amount_number"] = update.message.text
    await update.message.reply_text("Masukkan *Amount Words*:")
    return BD_AMOUNT_WORDS

async def bd_amount_words(update, context):
    context.user_data["bd_amount_words"] = update.message.text
    await update.message.reply_text("Masukkan *Instrument No*:")
    return BD_INSTRUMENT_NO

async def bd_instr_no(update, context):
    context.user_data["bd_instr_no"] = update.message.text
    await update.message.reply_text("Masukkan *Instrument Date*:")
    return BD_INSTRUMENT_DATE

async def bd_instr_date(update, context):
    context.user_data["bd_instr_date"] = update.message.text
    await update.message.reply_text("Masukkan *Payment Type*:")
    return BD_PAYMENT_TYPE

async def bd_payment(update, context):
    context.user_data["bd_payment_type"] = update.message.text
    await update.message.reply_text("Masukkan *Bank*:")
    return BD_BANK

async def bd_bank(update, context):
    context.user_data["bd_bank"] = update.message.text
    await update.message.reply_text("Masukkan *Session Text*:")
    return BD_SESSION_TEXT

async def bd_session_text(update, context):
    data = context.user_data
    data["bd_session_text"] = update.message.text

    out = f"bd_{uuid4().hex}.png"

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
            out_path=out,
        )
        with open(out, "rb") as img:
            await update.message.reply_photo(img, caption="✅ Receipt Bangladesh jadi!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
    finally:
        if os.path.exists(out):
            os.remove(out)
        context.user_data.clear()

    return ConversationHandler.END


# ================== MAIN ==================

def main():
    if not BOT_TOKEN:
        raise RuntimeError("❌ BOT_TOKEN belum di-set di Railway Variables!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("card", card_cmd))

    conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(card_from_start_button, pattern="^single_"),
            CommandHandler("card", card_cmd),
        ],
        states={
            CHOOSING_TEMPLATE: [CallbackQueryHandler(template_chosen, pattern="^TPL_")],

            UK_NAME: [MessageHandler(filters.TEXT, uk_name)],
            UK_ID: [MessageHandler(filters.TEXT, uk_id)],
            UK_BIRTH: [MessageHandler(filters.TEXT, uk_birth)],
            UK_ADDRESS: [MessageHandler(filters.TEXT, uk_address)],
            UK_ACTIVE: [MessageHandler(filters.TEXT, uk_active)],
            UK_PHOTO: [MessageHandler(filters.PHOTO, uk_photo)],

            IN_IDNO: [MessageHandler(filters.TEXT, in_idno)],
            IN_CLASS: [MessageHandler(filters.TEXT, in_class)],
            IN_DOB: [MessageHandler(filters.TEXT, in_dob)],
            IN_VALIDITY: [MessageHandler(filters.TEXT, in_validity)],
            IN_MOBILE: [MessageHandler(filters.TEXT, in_mobile)],
            IN_PHOTO: [MessageHandler(filters.PHOTO, in_photo)],

            BD_STUDENT_ROLL: [MessageHandler(filters.TEXT, bd_student_roll)],
            BD_CENTRE: [MessageHandler(filters.TEXT, bd_centre)],
            BD_REG_DATE: [MessageHandler(filters.TEXT, bd_reg_date)],
            BD_NAME: [MessageHandler(filters.TEXT, bd_name)],
            BD_AMOUNT_NUMBER: [MessageHandler(filters.TEXT, bd_amount_number)],
            BD_AMOUNT_WORDS: [MessageHandler(filters.TEXT, bd_amount_words)],
            BD_INSTRUMENT_NO: [MessageHandler(filters.TEXT, bd_instr_no)],
            BD_INSTRUMENT_DATE: [MessageHandler(filters.TEXT, bd_instr_date)],
            BD_PAYMENT_TYPE: [MessageHandler(filters.TEXT, bd_payment)],
            BD_BANK: [MessageHandler(filters.TEXT, bd_bank)],
            BD_SESSION_TEXT: [MessageHandler(filters.TEXT, bd_session_text)],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )

    app.add_handler(conv)

    app.run_polling()


if __name__ == "__main__":
    main()
