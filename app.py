import io
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="School HD Poster Generator", page_icon="🏫", layout="centered"
)

st.title("🏫 School Poster Generator (HD - Modern Formal)")
st.write(
    "Upload an event photo and update the details to generate an HD poster."
)


# --- HELPER FUNCTION: DOWNLOAD FILES SAFELY WITH USER-AGENT ---
def download_file(url, filepath):
    if not os.path.exists(filepath):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                },
            )
            with urllib.request.urlopen(req) as response, open(
                filepath, "wb"
            ) as out_file:
                out_file.write(response.read())
        except Exception as e:
            st.warning(f"⚠️ Could not download {filepath}: {e}")


# --- SIDEBAR / INPUT CONTROLS ---
st.sidebar.header("Poster Settings")

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
    # 1. Create 1080x1920 Full HD Canvas with an Executive Off-White/Ivory Base
    width, height = 1080, 1920
    poster = Image.new("RGB", (width, height), color="#F8FAFC")
    draw = ImageDraw.Draw(poster)

    # 2. Draw Top Karnataka Decorative Accent Bars (Red & Yellow)
    draw.rectangle([(0, 0), (width, 14)], fill="#D32F2F")  # Deep Red stripe
    draw.rectangle(
        [(0, 14), (width, 28)], fill="#FFC107"
    )  # Vibrant Gold stripe

    # 3. Draw Modern Dark Navy Footer Banner with a Gold Top Border
    footer_height = 320
    footer_y0 = height - footer_height
    draw.rectangle([(0, footer_y0 - 6), (width, footer_y0)], fill="#FFC107")
    draw.rectangle([(0, footer_y0), (width, height)], fill="#0F172A")

    # 4. Download and Load Kannada Font
    font_path = "NotoSansKannada-Bold.ttf"
    font_url = "https://raw.githubusercontent.com/openmaptiles/fonts/master/noto-sans/NotoSansKannada-Bold.ttf"
    download_file(font_url, font_path)

    try:
        font_title = ImageFont.truetype(font_path, 42)
        font_sub = ImageFont.truetype(font_path, 38)
        font_school = ImageFont.truetype(font_path, 38)
        font_badge = ImageFont.truetype(font_path, 52)
        font_footer_label = ImageFont.truetype(font_path, 42)
        font_footer_value = ImageFont.truetype(font_path, 46)
    except IOError:
        st.warning(
            "⚠️ Kannada font could not be loaded. Text may not render correctly."
        )
        font_title = font_sub = font_school = font_badge = font_footer_label = (
            font_footer_value
        ) = ImageFont.load_default()

    # 5. Download and Place Karnataka Government Emblem (Using 500px authorized size)
    emblem_path = "karnataka_emblem.png"
    emblem_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Seal_of_Karnataka.svg/500px-Seal_of_Karnataka.svg.png"
    download_file(emblem_url, emblem_path)

    if os.path.exists(emblem_path):
        try:
            emblem = Image.open(emblem_path).convert("RGBA")
            emblem = emblem.resize((120, 120), Image.Resampling.LANCZOS)
            emblem_x = (width - emblem.width) // 2
            emblem_y = 45
            poster.paste(emblem, (emblem_x, emblem_y), emblem)
        except Exception as e:
            st.warning(f"⚠️ Could not render emblem image: {e}")

    # 6. Draw Professional Header Text (Distinct Hierarchy)
    draw.text(
        (width // 2, 190),
        "ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
        font=font_title,
        fill="#900C3F",
        anchor="mm",
    )  # Rich Burgundy
    draw.text(
        (width // 2, 245),
        "ಶಾಲಾ ಶಿಕ್ಷಣ ಮತ್ತು ಸಾಕ್ಷರತಾ ಇಲಾಖೆ",
        font=font_sub,
        fill="#1E3A8A",
        anchor="mm",
    )  # Deep Royal Navy

    # 7. Draw School Name in 2 Clean Lines (Slate Charcoal for High Legibility)
    lines = [line.strip() for line in school.split("\n") if line.strip()]
    if len(lines) >= 1:
        draw.text(
            (width // 2, 315),
            lines[0],
            font=font_school,
            fill="#1F2937",
            anchor="mm",
        )
    if len(lines) >= 2:
        draw.text(
            (width // 2, 375),
            lines[1],
            font=font_school,
            fill="#374151",
            anchor="mm",
        )

    # 8. Draw "ಸಚೇತನ" Executive Pill Badge (Burgundy Fill with Crisp White Text)
    badge_w, badge_h = 320, 80
    badge_x0 = (width - badge_w) // 2
    badge_y0 = 430
    draw.rounded_rectangle(
        [
            (badge_x0, badge_y0),
            (badge_x0 + badge_w, badge_y0 + badge_h),
        ],
        radius=40,
        fill="#800020",
    )
    draw.text(
        (width // 2, badge_y0 + 40),
        "ಸಚೇತನ",
        font=font_badge,
        fill="#FFFFFF",
        anchor="mm",
    )

    # 9. Process, Auto-Fit, and Frame Photo with a Realistic Multi-Layer Shadow
    if image_file:
        img = Image.open(image_file).convert("RGB")
        max_w, max_h = 920, 960

        ratio = min(max_w / img.width, max_h / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        paste_x = (width - img.width) // 2
        paste_y = 545 + (max_h - img.height) // 2
        border = 18

        # Outer Shadow (Simulated Drop-Shadow for 3D Depth)
        shadow_offset = 12
        draw.rounded_rectangle(
            [
                (
                    paste_x - border + shadow_offset,
                    paste_y - border + shadow_offset,
                ),
                (
                    paste_x + img.width + border + shadow_offset,
                    paste_y + img.height + border + shadow_offset,
                ),
            ],
            radius=12,
            fill="#CBD5E1",
        )

        # Crisp White Polaroid-Style Card Frame
        draw.rounded_rectangle(
            [
                (paste_x - border, paste_y - border),
                (paste_x + img.width + border, paste_y + img.height + border),
            ],
            radius=12,
            fill="#FFFFFF",
            outline="#E2E8F0",
            width=2,
        )

        # Paste Uploaded Photo
        poster.paste(img, (paste_x, paste_y))

    # 10. Draw Formal Footer Content (Gold & Crisp White Typography on Navy)
    footer_text_1 = f"ದಿನಾಂಕ : {date_text}"
    footer_text_2 = f"ವಿಷಯ : {subject_text}"

    draw.text(
        (width // 2, height - 230),
        footer_text_1,
        font=font_footer_label,
        fill="#F8FAFC",
        anchor="mm",
    )
    draw.text(
        (width // 2, height - 120),
        footer_text_2,
        font=font_footer_value,
        fill="#FFD700",
        anchor="mm",
    )

    return poster


# --- APP EXECUTION ---
if uploaded_file is not None:
    with st.spinner("Generating Professional High-Resolution Poster..."):
        hd_poster = create_poster(
            uploaded_file, school_name, date_input, subject_input
        )

        st.image(
            hd_poster,
            caption="HD Professional Poster Preview (1080x1920)",
            use_container_width=True,
        )

        buf = io.BytesIO()
        hd_poster.save(buf, format="PNG", quality=100)
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Download HD Poster (PNG)",
            data=byte_im,
            file_name="school_poster_professional_hd.png",
            mime="image/png",
            use_container_width=True,
        )
else:
    st.info("👈 Please upload an image from the sidebar to generate the poster.")
