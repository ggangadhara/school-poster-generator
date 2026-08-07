import io
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="School HD Poster Generator", page_icon="🏫", layout="centered"
)

st.title("🏫 School Poster Generator (HD)")
st.write(
    "Upload an event photo and update the details to generate an HD poster."
)

# --- SIDEBAR / INPUT CONTROLS ---
st.sidebar.header("Poster Settings")

# Default 2-line school name and address
default_school_name = (
    "ಸರ್ಕಾರಿ ಹಿರಿಯ ಪ್ರಾಥಮಿಕ ಶಾಲೆ ಹೊಮ್ಮರಗಳ್ಳಿ\nಹೆಚ್ ಡಿ ಕೋಟೆ ತಾಲ್ಲೂಕು ಮೈಸೂರು ಜಿಲ್ಲೆ"
)

school_name = st.sidebar.text_area(
    "School Name (2 Lines Recommended)",
    value=default_school_name,
    height=100,
)

date_input = st.sidebar.text_input("Date (ದಿನಾಂಕ)", value="05-08-2026")
subject_input = st.sidebar.text_input(
    "Subject (ವಿಷಯ)", value="ಮಾಲಿನ್ಯ ತಡೆಗಟ್ಟುವುದು."
)

uploaded_file = st.sidebar.file_uploader(
    "Upload School Photo", type=["jpg", "jpeg", "png"]
)


# --- HELPER FUNCTION TO DRAW HD POSTER ---
def create_poster(image_file, school, date_text, subject_text):
    # 1. Create 1080x1920 Full HD Canvas (Vertical Poster Ratio)
    width, height = 1080, 1920
    poster = Image.new("RGB", (width, height), color="#D5F5E3")  # Light green
    draw = ImageDraw.Draw(poster)

    # 2. Draw Bottom Orange Banner
    banner_height = 390
    draw.rectangle(
        [(0, height - banner_height), (width, height)], fill="#F5B041"
    )

    # 3. Load Kannada Font (Auto-download from openmaptiles mirror if missing)
    font_path = "NotoSansKannada-Bold.ttf"
    font_url = "https://raw.githubusercontent.com/openmaptiles/fonts/master/noto-sans/NotoSansKannada-Bold.ttf"

    if not os.path.exists(font_path):
        try:
            urllib.request.urlretrieve(font_url, font_path)
        except Exception as e:
            st.warning(f"⚠️ Could not download font automatically: {e}")

    # Load fonts
    try:
        font_title = ImageFont.truetype(font_path, 44)
        font_school = ImageFont.truetype(font_path, 40)
        font_badge = ImageFont.truetype(font_path, 56)
        font_footer = ImageFont.truetype(font_path, 48)
    except IOError:
        st.warning(
            "⚠️ Kannada font could not be loaded. Text may not render correctly."
        )
        font_title = font_school = font_badge = font_footer = (
            ImageFont.load_default()
        )

    # 4. Add Karnataka Government Emblem at the Top Center
    emblem_path = "karnataka_emblem.png"
    emblem_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Seal_of_Karnataka.svg/300px-Seal_of_Karnataka.svg.png"

    if not os.path.exists(emblem_path):
        try:
            urllib.request.urlretrieve(emblem_url, emblem_path)
        except Exception:
            pass  # Fail silently if offline; text will still render

    if os.path.exists(emblem_path):
        try:
            emblem = Image.open(emblem_path).convert("RGBA")
            emblem = emblem.resize((120, 120), Image.Resampling.LANCZOS)
            emblem_x = (width - emblem.width) // 2
            emblem_y = 25
            poster.paste(emblem, (emblem_x, emblem_y), emblem)
        except Exception:
            pass

    # 5. Draw Header Text (Karnataka Govt & Department)
    draw.text(
        (width // 2, 180),
        "ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
        font=font_title,
        fill="#900C3F",
        anchor="mm",
    )
    draw.text(
        (width // 2, 240),
        "ಶಾಲಾ ಶಿಕ್ಷಣ ಮತ್ತು ಸಾಕ್ಷರತಾ ಇಲಾಖೆ",
        font=font_title,
        fill="#1A5276",
        anchor="mm",
    )

    # 6. Draw School Name in exactly 2 lines with proper spacing
    lines = [line.strip() for line in school.split("\n") if line.strip()]

    if len(lines) >= 1:
        # Line 1: ಸರ್ಕಾರಿ ಹಿರಿಯ ಪ್ರಾಥಮಿಕ ಶಾಲೆ ಹೊಮ್ಮರಗಳ್ಳಿ
        draw.text(
            (width // 2, 310),
            lines[0],
            font=font_school,
            fill="#900C3F",
            anchor="mm",
        )
    if len(lines) >= 2:
        # Line 2: ಹೆಚ್ ಡಿ ಕೋಟೆ ತಾಲ್ಲೂಕು ಮೈಸೂರು ಜಿಲ್ಲೆ (with 65px line spacing)
        draw.text(
            (width // 2, 375),
            lines[1],
            font=font_school,
            fill="#900C3F",
            anchor="mm",
        )

    # 7. Draw "ಸಚೇತನ" Pink Badge
    badge_w, badge_h = 340, 90
    badge_x0 = (width - badge_w) // 2
    badge_y0 = 435
    draw.rounded_rectangle(
        [
            (badge_x0, badge_y0),
            (badge_x0 + badge_w, badge_y0 + badge_h),
        ],
        radius=22,
        fill="#F1948A",
    )
    draw.text(
        (width // 2, badge_y0 + 45),
        "ಸಚೇತನ",
        font=font_badge,
        fill="#900C3F",
        anchor="mm",
    )

    # 8. Process, Auto-Fit, and Center Uploaded Image
    if image_file:
        img = Image.open(image_file).convert("RGB")

        # Define maximum available photo canvas area
        max_w, max_h = 940, 940

        # Calculate scale ratio to auto-fit without distorting aspect ratio
        ratio = min(max_w / img.width, max_h / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Center the image horizontally and vertically in the middle canvas area
        paste_x = (width - img.width) // 2
        paste_y = 550 + (max_h - img.height) // 2

        # Draw a clean white border frame
        border = 15
        draw.rectangle(
            [
                (paste_x - border, paste_y - border),
                (paste_x + img.width + border, paste_y + img.height + border),
            ],
            fill="white",
        )

        # Paste uploaded photo
        poster.paste(img, (paste_x, paste_y))

    # 9. Draw Footer Text (Date & Subject)
    footer_text_1 = f"ದಿನಾಂಕ: {date_text}"
    footer_text_2 = f"ವಿಷಯ - {subject_text}"

    draw.text(
        (width // 2, height - 250),
        footer_text_1,
        font=font_footer,
        fill="#1B4F72",
        anchor="mm",
    )
    draw.text(
        (width // 2, height - 140),
        footer_text_2,
        font=font_footer,
        fill="#1B4F72",
        anchor="mm",
    )

    return poster


# --- APP EXECUTION ---
if uploaded_file is not None:
    with st.spinner("Generating High-Resolution Poster..."):
        hd_poster = create_poster(
            uploaded_file, school_name, date_input, subject_input
        )

        st.image(
            hd_poster,
            caption="HD Poster Preview (1080x1920)",
            use_container_width=True,
        )

        buf = io.BytesIO()
        hd_poster.save(buf, format="PNG", quality=100)
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Download HD Poster (PNG)",
            data=byte_im,
            file_name="school_poster_hd.png",
            mime="image/png",
            use_container_width=True,
        )
else:
    st.info("👈 Please upload an image from the sidebar to generate the poster.")
