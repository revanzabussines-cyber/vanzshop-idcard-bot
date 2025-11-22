import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================
# PATH TEMPLATE & FONT
# =========================
TEMPLATE_UK = os.path.join(BASE_DIR, "template_uk.png")
TEMPLATE_INDIA = os.path.join(BASE_DIR, "template_india.png")
TEMPLATE_BD = os.path.join(BASE_DIR, "template_bd.png")  # simpan template BD dengan nama ini

ARIAL_FONT = os.path.join(BASE_DIR, "arial.ttf")      # UK & India
VERDANA_FONT = os.path.join(BASE_DIR, "verdana.ttf")  # Bangladesh (fallback ke Arial kalau tidak ada)

# =========================
# POSISI & SIZE NAMA (EDIT DI SINI AJA)
# =========================

# UK card (template_uk.png)
UK_NAME_POS = (260, 260)  # (x, y) posisi text nama
UK_NAME_SIZE = 40

# India card (template_india.png)
INDIA_NAME_POS = (120, 950)  # (x, y)
INDIA_NAME_SIZE = 46

# Bangladesh receipt (template_bd.png)
BD_NAME_POS = (260, 580)   # posisi setelah "Name:"
BD_NAME_SIZE = 32

# =========================
# HELPER
# =========================

def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Load TTF, kalau gagal fallback ke font default."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# =========================
# GENERATOR NAME-ONLY
# =========================

def generate_uk_card(name: str, out_path: str) -> str:
    """
    Generate 1 UK card hanya dengan nama.
    Template sudah fixed, kita cuma tulis nama di posisi UK_NAME_POS.
    """
    img = Image.open(TEMPLATE_UK).convert("RGB")
    draw = ImageDraw.Draw(img)

    font = _load_font(ARIAL_FONT, UK_NAME_SIZE)
    draw.text(UK_NAME_POS, name, font=font, fill="black")

    img.save(out_path, format="PNG")
    return out_path


def generate_india_card(name: str, out_path: str) -> str:
    """
    Generate 1 India card hanya dengan nama.
    Nama ditulis di posisi INDIA_NAME_POS.
    """
    img = Image.open(TEMPLATE_INDIA).convert("RGB")
    draw = ImageDraw.Draw(img)

    font = _load_font(ARIAL_FONT, INDIA_NAME_SIZE)
    draw.text(INDIA_NAME_POS, name, font=font, fill="black")

    img.save(out_path, format="PNG")
    return out_path


def generate_bangladesh_card(name: str, out_path: str) -> str:
    """
    Generate 1 Bangladesh fee receipt hanya dengan nama.
    Field lain (roll, centre, amount, dll) dibiarkan seperti di template.
    Nama akan ditulis di posisi BD_NAME_POS.
    """
    img = Image.open(TEMPLATE_BD).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_path = VERDANA_FONT if os.path.exists(VERDANA_FONT) else ARIAL_FONT
    font = _load_font(font_path, BD_NAME_SIZE)
    draw.text(BD_NAME_POS, name, font=font, fill="black")

    img.save(out_path, format="PNG")
    return out_path
