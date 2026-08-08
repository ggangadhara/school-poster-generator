import io
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Sachetana Poster Generator", page_icon="🏫", layout="centered"
)

st.title("🏫 Sachetana Poster Generator")
st.write(
    "Upload your daily school activity photo and update the details to generate an official HD poster."
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


# --- SIDEBAR: EVENT DETAILS & CONTROLS ---
st.sidebar.header("Activity Details")

# Activity Category Chip Selector
CATEGORY_TAGS = {
    "ಪರಿಸರ ಕ್ಲಬ್ (Eco Club)": "• ಪರಿಸರ ಕ್ಲಬ್",
    "ಸ್ವಚ್ಛ ಭಾರತ (Swachh Bharat)": "• ಸ್ವಚ್ಛ ಭಾರತ",
    "ಶೈಕ್ಷಣಿಕ ಚಟುವಟಿಕೆ (Academics)": "• ಶೈಕ್ಷಣಿಕ ಚಟುವಟಿಕೆ",
    "ಸಾಂಸ್ಕೃತಿಕ (Cultural)": "• ಸಾಂಸ್ಕೃತಿಕ",
    "ಕ್ರೀಡೆ ಮತ್ತು ದೈಹಿಕ ಶಿಕ್ಷಣ (Sports)": "• ಕ್ರೀಡೆ",
    "ಸಚೇತನ ವಿಶೇಷ (Sachetana Special)": "• ಸಚೇತನ ವಿಶೇಷ",
}

selected_category_label = st.sidebar.selectbox(
    "Activity Category Tag",
    options=list(CATEGORY_TAGS.keys()),
    index=0,
)
category_tag_text = CATEGORY_TAGS[selected_category_label]

subject_input = st.sidebar.text_input(
    "Activity Title (ವಿಷಯ)", value="ಮಾಲಿನ್ಯ ತಡೆಗಟ್ಟುವುದು."
)

date_input = st.sidebar.text_input("Date (ದಿನಾಂಕ)", value="08-08-2026")

uploaded_file = st.sidebar.file_uploader(
    "Upload School Photo", type=["jpg", "jpeg", "png"]
)

# --- ADVANCED / FIXED SETTINGS (HIDDEN BY DEFAULT) ---
with st.sidebar.expander("⚙️ Advanced: Edit Fixed School Name"):
    default_school_name = "ಸರ್ಕಾರಿ ಹಿರಿಯ ಪ್ರಾಥಮಿಕ ಶಾಲೆ ಹೊಮ್ಮರಗಳ್ಳಿ\nಹೆಚ್ ಡಿ ಕೋಟೆ ತಾಲ್ಲೂಕು ಮೈಸೂರು ಜಿಲ್ಲೆ"
    school_name = st.text_area(
        "School Name (2 Lines)", value=default_school_name, height=90
    )


# --- HELPER FUNCTION TO DRAW HD POSTER ---
def create_poster(image_file, school, category_text, subject_text, date_text):
    # 1. Create 1080x1920 Full HD Canvas (Fixed Warm Parchment Beige #F4F1EA)
    width, height = 1080, 1920
    bg_color = "#F4F1EA"
    poster = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(poster)

    # 2. Draw Top Karnataka Decorative Accent Bars (Red & Yellow)
    draw.rectangle([(0, 0), (width, 14)], fill="#D32F2F")  # Deep Red stripe
    draw.rectangle(
        [(0, 14), (width, 28)], fill="#FFC107"
    )  # Vibrant Gold stripe

    # 3. Download and Load Kannada Font
    font_path = "NotoSansKannada-Bold.ttf"
    font_url = "https://raw.githubusercontent.com/openmaptiles/fonts/master/noto-sans/NotoSansKannada-Bold.ttf"
    download_file(font_url, font_path)

    try:
        font_title = ImageFont.truetype(font_path, 42)
        font_sub = ImageFont.truetype(font_path, 38)
        font_school = ImageFont.truetype(font_path, 38)
        font_badge = ImageFont.truetype(font_path, 52)
        font_category = ImageFont.truetype(font_path, 30)
        font_hero_title = ImageFont.truetype(font_path, 52)
        font_date = ImageFont.truetype(font_path, 36)
    except IOError:
        st.warning(
            "⚠️ Kannada font could not be loaded. Text may not render correctly."
        )
        font_title = font_sub = font_school = font_badge = font_category = (
            font_hero_title
        ) = font_date = ImageFont.load_default()

    # 4. Download and Place Karnataka Government Emblem (500px authorized size)
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

    # 5. Draw Fixed Header Text
    draw.text(
        (width // 2, 190),
        "ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
        font=font_title,
        fill="#900C3F",
        anchor="mm",
    )
    draw.text(
        (width // 2, 245),
        "ಶಾಲಾ ಶಿಕ್ಷಣ ಮತ್ತು ಸಾಕ್ಷರತಾ ಇಲಾಖೆ",
        font=font_sub,
        fill="#1E3A8A",
        anchor="mm",
    )

    # 6. Draw Fixed School Name in 2 Clean Lines
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

    # 7. Draw "ಸಚೇತನ" Executive Pill Badge
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

    # 8. SMART HUMAN-AWARE IMAGE FITTING (Zero padding, zero distortion)
    target_w, target_h = 1000, 960
    paste_x = (width - target_w) // 2
    paste_y = 550

    if image_file:
        img = Image.open(image_file).convert("RGB")
        # Top-weighted aspect fill (0.08): Fills 100% of frame without squashing faces
        img_processed = ImageOps.fit(
            img,
            (target_w, target_h),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.08),
        )
        poster.paste(img_processed, (paste_x, paste_y))

        # Crisp standard border outline around the image
        draw.rectangle(
            [
                (paste_x - 1, paste_y - 1),
                (paste_x + target_w + 1, paste_y + target_h + 1),
            ],
            outline="#CBD5E1",
            width=2,
        )
    else:
        # Placeholder gray canvas if no photo uploaded yet
        draw.rectangle(
            [(paste_x, paste_y), (paste_x + target_w, paste_y + target_h)],
            fill="#E2E8F0",
            outline="#CBD5E1",
            width=2,
        )
        draw.text(
            (width // 2, paste_y + (target_h // 2)),
            "Photo Will Fill This Frame Completely",
            font=font_sub,
            fill="#64748B",
            anchor="mm",
        )

    # 9. PROFESSIONAL FOOTER CARD WITH HIERARCHY
    card_w, card_h = 960, 260
    card_x0 = (width - card_w) // 2
    card_y0 = 1575

    # White elevated info card
    draw.rounded_rectangle(
        [
            (card_x0, card_y0),
            (card_x0 + card_w, card_y0 + card_h),
        ],
        radius=24,
        fill="#FFFFFF",
        outline="#CBD5E1",
        width=3,
    )

    # A. Draw Activity Category Pill Chip (Top Center of Card)
    chip_w, chip_h = 240, 48
    chip_x0 = (width - chip_w) // 2
    chip_y0 = card_y0 + 24
    draw.rounded_rectangle(
        [
            (chip_x0, chip_y0),
            (chip_x0 + chip_w, chip_y0 + chip_h),
        ],
        radius=14,
        fill="#EFF6FF",
        outline="#3B82F6",
        width=2,
    )
    draw.text(
        (width // 2, chip_y0 + 24),
        category_text,
        font=font_category,
        fill="#1D4ED8",
        anchor="mm",
    )

    # B. Draw Hero Activity Title (Large Burgundy text for instant readability)
    draw.text(
        (width // 2, card_y0 + 130),
        subject_text,
        font=font_hero_title,
        fill="#800020",
        anchor="mm",
    )

    # C. Draw Date (Secondary Slate Gray hierarchy at bottom)
    formatted_date = f"ದಿನಾಂಕ : {date_text}"
    draw.text(
        (width // 2, card_y0 + 208),
        formatted_date,
        font=font_date,
        fill="#475569",
        anchor="mm",
    )

    return poster


# --- APP EXECUTION ---
if uploaded_file is not None:
    with st.spinner("Generating Professional High-Resolution Poster..."):
        hd_poster = create_poster(
            uploaded_file,
            school_name,
            category_tag_text,
            subject_input,
            date_input,
        )

        st.image(
            hd_poster,
            caption="HD Professional Poster Preview (Warm Parchment Beige)",
            use_container_width=True,
        )

        buf = io.BytesIO()
        hd_poster.save(buf, format="PNG", quality=100)
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Download HD Poster (PNG)",
            data=byte_im,
            file_name="sachetana_poster_hd.png",
            mime="image/png",
            use_container_width=True,
        )
else:
    st.info(
        "👈 Please upload an image from the sidebar to generate your poster."
    )

# --- WEBPAGE FOOTER CREDIT ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #64748B; font-size: 0.9em; padding-top: 10px;'>
        <b>Design and developed by:</b><br>
        Gangadhar, Statistical Inspector, Taluk Office, Malavalli, Mandya
    </div>
    """,
    unsafe_allow_html=True,
)
