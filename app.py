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

school_name = st.sidebar.text_area(
    "School Name",
    value="ಸರ್ಕಾರಿ ಹಿರಿಯ ಪ್ರಾಥಮಿಕ ಶಾಲೆ ಹೊಮ್ಮರಗಳ್ಳಿ ಹೆಚ್ ಡಿ ಕೋಟೆ ತಾಲ್ಲೂಕು ಮೈಸೂರು ಜಿಲ್ಲೆ",
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
    banner_height = 400
    draw.rectangle(
        [(0, height - banner_height), (width, height)], fill="#F5B041"
    )

    # 3. Load Kannada Font (Auto-download from openmaptiles mirror if missing)
    font_path = "NotoSansKannada-Bold.ttf"
    font_url = "https://raw.githubusercontent.com/openmaptiles/fonts/master/noto-sans/NotoSansKannada-Bold.ttf"

    # Automatically fetch the font file if not found locally
    if not os.path.exists(font_path):
        try:
            urllib.request.urlretrieve(font_url, font_path)
        except Exception as e:
            st.warning(f"⚠️ Could not download font automatically: {e}")

    # Use LAYOUT_RAQM to properly shape Kannada conjuncts & vowel signs
    try:
        layout = ImageFont.LAYOUT_RAQM
        font_title = ImageFont.truetype(
            font_path, 45, layout_engine=layout
        )
        font_school = ImageFont.truetype(
            font_path, 42, layout_engine=layout
        )
        font_badge = ImageFont.truetype(
            font_path, 60, layout_engine=layout
        )
        font_footer = ImageFont.truetype(
            font_path, 50, layout_engine=layout
        )
    except (IOError, KeyError, ValueError):
        # Fallback if RaQm is unavailable on the system
        try:
            font_title = ImageFont.truetype(font_path, 45)
            font_school = ImageFont.truetype(font_path, 42)
            font_badge = ImageFont.truetype(font_path, 60)
            font_footer = ImageFont.truetype(font_path, 50)
        except IOError:
            st.warning(
                "⚠️ Kannada font could not be loaded. Text may not render correctly."
            )
            font_title = font_school = font_badge = font_footer = (
                ImageFont.load_default()
            )

    # 4. Draw Header Text
    draw.text(
        (width // 2, 80),
        "ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
        font=font_title,
        fill="#900C3F",
        anchor="mm",
    )
    draw.text(
        (width // 2, 140),
        "ಶಾಲಾ ಶಿಕ್ಷಣ ಮತ್ತು ಸಾಕ್ಷರತಾ ಇಲಾಖೆ",
        font=font_title,
        fill="#1A5276",
        anchor="mm",
    )

    # Multiline School Name
    draw.multiline_text(
        (width // 2, 230),
        school,
        font=font_school,
        fill="#900C3F",
        anchor="mm",
        align="center",
        spacing=15,
    )

    # 5. Draw "ಸಚೇತನ" Pink Badge
    badge_w, badge_h = 360, 100
    badge_x0 = (width - badge_w) // 2
    badge_y0 = 340
    draw.rounded_rectangle(
        [
            (badge_x0, badge_y0),
            (badge_x0 + badge_w, badge_y0 + badge_h),
        ],
        radius=25,
        fill="#F1948A",
    )
    draw.text(
        (width // 2, badge_y0 + 50),
        "ಸಚೇತನ",
        font=font_badge,
        fill="#900C3F",
        anchor="mm",
    )

    # 6. Process and Center Uploaded Image
    if image_file:
        img = Image.open(image_file).convert("RGB")
        # High-quality Lanczos resizing to fit canvas nicely
        target_w, target_h = 900, 950
        img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)

        # Draw a white border frame
        paste_x = (width - img.width) // 2
        paste_y = 480
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

    # 7. Draw Footer Text (Date & Subject)
    footer_text_1 = f"ದಿನಾಂಕ: {date_text}"
    footer_text_2 = f"ವಿಷಯ - {subject_text}"

    draw.text(
        (width // 2, height - 260),
        footer_text_1,
        font=font_footer,
        fill="#1B4F72",
        anchor="mm",
    )
    draw.text(
        (width // 2, height - 150),
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

        # Display preview (scaled down for web viewing)
        st.image(
            hd_poster,
            caption="HD Poster Preview (1080x1920)",
            use_container_width=True,
        )

        # Convert to bytes for download
        buf = io.BytesIO()
        hd_poster.save(buf, format="PNG", quality=100)
        byte_im = buf.getvalue()

        # Download button
        st.download_button(
            label="📥 Download HD Poster (PNG)",
            data=byte_im,
            file_name="school_poster_hd.png",
            mime="image/png",
            use_container_width=True,
        )
else:
    st.info("👈 Please upload an image from the sidebar to generate the poster.")
