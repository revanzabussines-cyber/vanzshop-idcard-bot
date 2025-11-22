import os
from PIL import Image, ImageDraw, ImageFont

# =====================================================
# ================  CONFIG (EDIT DI SINI)  ============
# =====================================================

# Nama file template & font (satu folder sama all.py)
TEMPLATE_UK = "template_uk.png"
TEMPLATE_INDIA = "template_india.png"   # rename dari template_india (1).png
TEMPLATE_BD = "template_bd.png"         # rename gambar Bangladesh jadi ini

FONT_ARIAL = "arial.ttf"                # UK & India
FONT_VERDANA = "verdana.ttf"            # Bangladesh (boleh kosong, nanti fallback)

# ---------- UK CARD (LSE STYLE) ----------

# kotak foto (x1, y1, x2, y2)
UK_PHOTO_BOX = (700, 190, 950, 530)

# posisi & ukuran font teks (edit sesuka lo)
UK_NAME_POS = (260, 260)
UK_NAME_SIZE = 40

UK_ID_POS = (260, 310)
UK_ID_SIZE = 36

UK_BIRTH_POS = (260, 360)
UK_BIRTH_SIZE = 36

UK_ADDRESS_POS = (260, 410)
UK_ADDRESS_SIZE = 34

UK_ACTIVE_POS = (630, 520)   # "ACTIVE UNTIL ..."
UK_ACTIVE_SIZE = 36


# ---------- INDIA CARD (UNIV OF MUMBAI) ----------

# foto bulat di tengah
INDIA_PHOTO_CENTER = (440, 560)   # (x, y) tengah lingkaran
INDIA_PHOTO_RADIUS = 220

# posisi teks (tengah semua di bawah foto)
INDIA_LINE_START_Y = 950   # y baris pertama
INDIA_LINE_GAP = 70        # jarak antar baris
INDIA_FONT_SIZE = 46

# ---------- BANGLADESH FEE RECEIPT ----------

# semua pakai Verdana
BD_TOP_LEFT_POS = (260, 520)   # Student Roll, Name (kolom kiri)
BD_TOP_RIGHT_X = 1020          # Centre, Registration Date (kolom kanan)
BD_TOP_Y1 = 520
BD_TOP_Y2 = 580
BD_TOP_FONT_SIZE = 34

# paragraf “Received the sum of…”
BD_PARA_POS = (260, 660)       # titik mulai paragraf
BD_PARA_WIDTH = 1000           # max lebar paragraf (buat wrapping)
BD_PARA_FONT_SIZE = 30
BD_PARA_LINE_GAP = 8

# baris tabel payment detail
BD_TABLE_Y = 900
BD_TABLE_FONT_SIZE = 30
BD_COL_INSTRUMENT_NO_X = 260
BD_COL_DATE_X = 520
BD_COL_PAYTYPE_X = 780
BD_COL_BANK_X = 1000
BD_COL_AMOUNT_X = 1260

# teks session (1 baris di bawah tabel)
BD_SESSION_POS = (260, 980)
BD_SESSION_FONT_SIZE = 30


# =====================================================
# ==============  HELPER (JARANG DIUBAH)  =============
# =====================================================

def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _paste_photo_rect(base: Image.Image, photo_path: str, box):
    x1, y1, x2, y2 = box
    target_w = x2 - x1
    target_h = y2 - y1

    photo = Image.open(photo_path).convert("RGB")
    pw, ph = photo.size
    target_ratio = target_w / target_h
    src_ratio = pw / ph

    # crop biar rasio mirip kotak
    if src_ratio > target_ratio:
        new_w = int(ph * target_ratio)
        left = (pw - new_w) // 2
        photo = photo.crop((left, 0, left + new_w, ph))
    else:
        new_h = int(pw / target_ratio)
        top = (ph - new_h) // 2
        photo = photo.crop((0, top, pw, top + new_h))

    photo = photo.resize((target_w, target_h), Image.LANCZOS)
    base.paste(photo, (x1, y1))


def _paste_photo_circle(base: Image.Image, photo_path: str, center, radius: int):
    cx, cy = center
    diameter = radius * 2

    photo = Image.open(photo_path).convert("RGB")
    pw, ph = photo.size
    side = min(pw, ph)
    left = (pw - side) // 2
    top = (ph - side) // 2
    photo = photo.crop((left, top, left + side, top + side))
    photo = photo.resize((diameter, diameter), Image.LANCZOS)

    mask = Image.new("L", (diameter, diameter), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((0, 0, diameter, diameter), fill=255)

    base.paste(photo, (cx - radius, cy - radius), mask)


def _draw_paragraph(draw, text, pos, font, max_width, line_gap):
    """Simple word-wrap paragraph. Posisi/ukuran edit di CONFIG aja."""
    x, y = pos
    words = text.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        w, h = draw.textsize(test, font=font)
        if w <= max_width:
            line = test
        else:
            draw.text((x, y), line, font=font, fill="black")
            y += h + line_gap
            line = word
    if line:
        draw.text((x, y), line, font=font, fill="black")


# =====================================================
# ==================  GENERATOR =======================
# =====================================================

def generate_uk_card(
    name: str,
    student_id: str,
    birth: str,
    address: str,
    active_until: str,
    photo_path: str,
    out_path: str = "uk_card_result.png",
) -> str:
    """🇬🇧 Generate UK card (LSE style)."""
    base = Image.open(TEMPLATE_UK).convert("RGB")
    draw = ImageDraw.Draw(base)

    # foto
    _paste_photo_rect(base, photo_path, UK_PHOTO_BOX)

    # font
    font_name = _load_font(FONT_ARIAL, UK_NAME_SIZE)
    font_id = _load_font(FONT_ARIAL, UK_ID_SIZE)
    font_birth = _load_font(FONT_ARIAL, UK_BIRTH_SIZE)
    font_addr = _load_font(FONT_ARIAL, UK_ADDRESS_SIZE)
    font_active = _load_font(FONT_ARIAL, UK_ACTIVE_SIZE)

    # teks
    draw.text(UK_NAME_POS, name, font=font_name, fill="black")
    draw.text(UK_ID_POS, student_id, font=font_id, fill="black")
    draw.text(UK_BIRTH_POS, birth, font=font_birth, fill="black")
    draw.text(UK_ADDRESS_POS, address, font=font_addr, fill="black")
    draw.text(UK_ACTIVE_POS, active_until, font=font_active, fill="black")

    base.save(out_path, format="PNG")
    return out_path


def generate_india_card(
    id_no: str,
    class_name: str,
    dob: str,
    validity: str,
    mobile: str,
    photo_path: str,
    out_path: str = "india_card_result.png",
) -> str:
    """🇮🇳 Generate India card (University of Mumbai style)."""
    base = Image.open(TEMPLATE_INDIA).convert("RGB")
    draw = ImageDraw.Draw(base)

    # foto bulat
    _paste_photo_circle(base, photo_path, INDIA_PHOTO_CENTER, INDIA_PHOTO_RADIUS)

    font = _load_font(FONT_ARIAL, INDIA_FONT_SIZE)

    def draw_centered_line(y, text):
        w, h = draw.textsize(text, font=font)
        x = (base.size[0] - w) // 2
        draw.text((x, y), text, font=font, fill="black")

    y = INDIA_LINE_START_Y
    draw_centered_line(y + 0 * INDIA_LINE_GAP, f"ID No: {id_no}")
    draw_centered_line(y + 1 * INDIA_LINE_GAP, f"Class: {class_name}")
    draw_centered_line(y + 2 * INDIA_LINE_GAP, f"D.O.B: {dob}")
    draw_centered_line(y + 3 * INDIA_LINE_GAP, f"Validity: {validity}")
    draw_centered_line(y + 4 * INDIA_LINE_GAP, f"Mobile: {mobile}")

    base.save(out_path, format="PNG")
    return out_path


def generate_bangladesh_receipt(
    student_roll: str,
    centre: str,
    registration_date: str,
    name: str,
    amount_number: str,
    amount_words: str,
    instrument_no: str,
    instrument_date: str,
    payment_type: str,
    bank: str,
    session_text: str,
    out_path: str = "bd_receipt_result.png",
) -> str:
    """🇧🇩 Generate Bangladesh fee receipt."""
    base = Image.open(TEMPLATE_BD).convert("RGB")
    draw = ImageDraw.Draw(base)

    # pilih font (kalau verdana.ttf nggak ada, pakai arial/default)
    font_path = FONT_VERDANA if os.path.exists(FONT_VERDANA) else FONT_ARIAL

    font_top = _load_font(font_path, BD_TOP_FONT_SIZE)
    font_para = _load_font(font_path, BD_PARA_FONT_SIZE)
    font_table = _load_font(font_path, BD_TABLE_FONT_SIZE)
    font_session = _load_font(font_path, BD_SESSION_FONT_SIZE)

    # ----- TOP BLOCK -----
    # kiri
    draw.text(BD_TOP_LEFT_POS, f"Student Roll no: {student_roll}", font=font_top, fill="black")
    draw.text((BD_TOP_LEFT_POS[0], BD_TOP_Y2), f"Name: {name}", font=font_top, fill="black")

    # kanan
    draw.text((BD_TOP_RIGHT_X, BD_TOP_Y1), f"Centre: {centre}", font=font_top, fill="black")
    draw.text((BD_TOP_RIGHT_X, BD_TOP_Y2), f"Registration Date: {registration_date}", font=font_top, fill="black")

    # ----- PARAGRAPH -----
    paragraph = f"Received the sum of Tk {amount_number} ({amount_words}) towards {session_text}"
    _draw_paragraph(
        draw,
        paragraph,
        BD_PARA_POS,
        font_para,
        BD_PARA_WIDTH,
        BD_PARA_LINE_GAP,
    )

    # ----- PAYMENT ROW -----
    y = BD_TABLE_Y
    draw.text((BD_COL_INSTRUMENT_NO_X, y), instrument_no, font=font_table, fill="black")
    draw.text((BD_COL_DATE_X, y), instrument_date, font=font_table, fill="black")
    draw.text((BD_COL_PAYTYPE_X, y), payment_type, font=font_table, fill="black")
    draw.text((BD_COL_BANK_X, y), bank, font=font_table, fill="black")
    draw.text((BD_COL_AMOUNT_X, y), amount_number, font=font_table, fill="black")

    # ----- SESSION LINE -----
    draw.text(BD_SESSION_POS, session_text, font=font_session, fill="black")

    base.save(out_path, format="PNG")
    return out_path
