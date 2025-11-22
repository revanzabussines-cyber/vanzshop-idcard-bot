from PIL import Image, ImageDraw, ImageFont


# ============================
#  FONT LOADER
# ============================
FONT_BOLD = "Arial-bold.ttf"
FONT_NORMAL = "Verdana.ttf"


# ============================
#  UK CARD
# ============================
def generate_uk_card(name: str, out_path: str):

    img = Image.open("template_uk.png").convert("RGBA")
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype(FONT_BOLD, 60)
    font_med = ImageFont.truetype(FONT_BOLD, 48)

    # Nama
    draw.text((140, 330), name, font=font_big, fill="black")

    # ID, Birth, Address default (template statis)
    draw.text((230, 480), "1201-0732", font=font_med, fill="black")
    draw.text((230, 560), "10/10/2005", font=font_med, fill="black")
    draw.text((380, 640), "London, UK", font=font_med, fill="black")

    img.save(out_path)


# ============================
#  INDIA CARD
# ============================
def generate_india_card(name: str, out_path: str):

    img = Image.open("template_india.png").convert("RGBA")
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype(FONT_BOLD, 60)
    font_med = ImageFont.truetype(FONT_BOLD, 46)

    # Nama (besar di atas foto)
    draw.text((300, 300), name, font=font_big, fill="black")

    # Detail default (template statis)
    draw.text((300, 400), "ECE", font=font_med, fill="black")
    draw.text((300, 470), "15/01/2000", font=font_med, fill="black")
    draw.text((300, 540), "11/25 - 11/26", font=font_med, fill="black")
    draw.text((300, 610), "+917546728719", font=font_med, fill="black")

    img.save(out_path)


# ============================
#  BANGLADESH RECEIPT
# ============================
def generate_bangladesh_card(header_text: str, out_path: str):

    img = Image.open("template_bd.png").convert("RGBA")
    draw = ImageDraw.Draw(img)

    font_header = ImageFont.truetype(FONT_NORMAL, 40)

    # Header miring (posisi sesuai template kamu)
    draw.text((300, 250), header_text, font=font_header, fill="black")

    img.save(out_path)
