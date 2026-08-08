import io
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Sachetana Poster Generator", page_icon="🏫", layout="centered"
)

st.title("🏫 Sachetana Poster Generator")
st.write(
    "Upload your event photo and update the Date & Subject to generate an HD poster."
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


# --- SIDEBAR: EVENT DETAILS ---
st.sidebar.header("Event Details")

date_input = st.sidebar.text_input("Date (ದಿನಾಂಕ)", value="08-08-2026")
subject_input = st.sidebar.text_input(
    "Subject (ವಿಷಯ)", value="ಮಾಲಿನ್ಯ ತಡೆಗಟ್ಟುವುದು."
)

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
def create_poster(image_file, school, date_text, subject_text):
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
        font_footer_label = ImageFont.truetype(font_path, 38)  # Smaller secondary Date
        font_footer_value = ImageFont.truetype(font_path, 54)  # Larger hero Subject
    except IOError:
        st.warning(
            "⚠️ Kannada font could not be loaded. Text may not render correctly."
        )
        font_title = font_sub = font_school = font_badge = font_footer_label = (
            font_footer_value
        ) = ImageFont.load_default()

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

    # 8. STANDARD FRAME WITH FULL-FRAME STRETCH (No background card, no shadows)
    target_w, target_h = 1000, 960
    paste_x = (width - target_w) // 2
    paste_y = 550

    if image_file:
        img = Image.open(image_file).convert("RGB")
        # Full Frame Stretch: Exact resize to fill 100% of target area without cropping or padding
        img_processed = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        poster.paste(img_processed, (paste_x, paste_y))

        # Standard clean thin border outline around the image
        draw.rectangle(
            [(paste_x - 1, paste_y - 1), (paste_x + target_w + 1, paste_y + target_h + 1)],
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

    # 9. UNIFORM FOOTER CARD WITH HERO SUBJECT HIGHLIGHT
    card_w, card_h = 960, 260
    card_x0 = (width - card_w) // 2
    card_y0 = 1575

    # A. Outer White Elevated Card
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

    # B. Draw Secondary Date Text at Top of Card
    footer_text_1 = f"ದಿನಾಂಕ : {date_text}"
    draw.text(
        (width // 2, card_y0 + 60),
        footer_text_1,
        font=font_footer_label,
        fill="#1E3A8A",  # Royal Navy
        anchor="mm",
    )

    # C. Highlight Pill Container Behind the Subject (Makes it pop instantly!)
    pill_x0 = card_x0 + 35
    pill_x1 = card_x0 + card_w - 35
    pill_y0 = card_y0 + 110
    pill_y1 = card_y0 + 225
    draw.rounded_rectangle(
        [
            (pill_x0, pill_y0),
            (pill_x1, pill_y1),
        ],
        radius=20,
        fill="#FDEDEC",      # Soft blush-pink highlight tint
        outline="#E6B0AA",   # Warm rose border
        width=2,
    )

    # D. Draw Hero Subject Text inside Highlight Pill
    footer_text_2 = f"ವಿಷಯ - {subject_text}"
    draw.text(
        (width // 2, pill_y0 + 58),
        footer_text_2,
        font=font_footer_value,
        fill="#800020",  # Rich Burgundy
        anchor="mm",
    )

    return poster


# --- APP EXECUTION ---
if uploaded_file is not None:
    with st.spinner("Generating Professional High-Resolution Poster..."):
        hd_poster = create_poster(
            uploaded_file,
            school_name,
            date_input,
            subject_input,
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
