import io
import streamlit as st
from PIL import Image
from rembg import remove

# ── Language state (English by default) ──────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "en"

lang = st.session_state.lang

# ── Translations ─────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "page_title": "Remove Background",
        "title":      "Background<br>Removal",
        "subtitle":   "Upload an image and receive a clean, transparent result instantly.",
        "upload":     "Upload Image",
        "uploader":   "Upload an image to remove its background",
        "browse":     "Upload",
        "hint":       "200MB per file • JPG, PNG, WEBP",
        "processing": "Processing",
        "original":   "Original",
        "removed":    "Background Removed",
        "download":   "Download PNG",
        "note":       "Transparent PNG &nbsp;·&nbsp; Ready to use",
        "footer":     "Powered by Andrés Pérez &nbsp;·&nbsp; rembg",
    },
    "es": {
        "page_title": "Quitar Fondo",
        "title":      "Quitar<br>Fondo",
        "subtitle":   "Sube una imagen y obtén un resultado limpio y transparente al instante.",
        "upload":     "Subir Imagen",
        "uploader":   "Sube una imagen para quitar su fondo",
        "browse":     "Subir",
        "hint":       "200MB por archivo • JPG, PNG, WEBP",
        "processing": "Procesando",
        "original":   "Original",
        "removed":    "Fondo Eliminado",
        "download":   "Descargar PNG",
        "note":       "PNG transparente &nbsp;·&nbsp; Listo para usar",
        "footer":     "Desarrollado por Andrés Pérez &nbsp;·&nbsp; rembg",
    },
}
t = TRANSLATIONS[lang]

st.set_page_config(
    page_title=t["page_title"],
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Theme state (dark by default) ────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# ── Color tokens ─────────────────────────────────────────────────────────────
if dark:
    BG          = "#0F0F0E"
    BG2         = "#181816"
    BG_UPLOAD   = "#131210"
    TEXT        = "#E8E4DC"
    TEXT_MUTED  = "#8C8C80"
    TEXT_SUBTLE = "#5A584F"
    BORDER      = "#252420"
    BORDER_DASH = "#302E28"
    BTN_BG      = "#E8E4DC"
    BTN_FG      = "#0F0F0E"
    ICON        = "☾"   # moon = currently dark mode
else:
    BG          = "#FFFFFF"
    BG2         = "#F4F3F0"
    BG_UPLOAD   = "#FAFAF8"
    TEXT        = "#1C1C1C"
    TEXT_MUTED  = "#6B6B6B"
    TEXT_SUBTLE = "#9A9A9A"
    BORDER      = "#E8E5E0"
    BORDER_DASH = "#C8C4BE"
    BTN_BG      = "#1C1C1C"
    BTN_FG      = "#FFFFFF"
    ICON        = "☀"   # sun = currently light mode

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif !important;
}}

/* Background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {{
    background-color: {BG} !important;
}}
[data-testid="stHeader"] {{
    background: transparent !important;
    border-bottom: none !important;
}}

/* Hide Streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"] {{
    display: none !important;
    visibility: hidden !important;
}}

/* Page layout */
.block-container {{
    padding-top: 5rem;
    padding-bottom: 5rem;
    max-width: 860px;
}}

/* Default text colour */
p, span, label, div, h1, h2, h3 {{
    color: {TEXT};
}}

/* ── Top-right control buttons (theme + language) — fixed, targeted via stable st-key class ── */
.st-key-theme_toggle button,
.st-key-lang_toggle button {{
    position: fixed !important;
    top: 1.1rem !important;
    z-index: 1000000 !important;   /* above Streamlit header (z-index 999990) so clicks register */
    width: 2.3rem !important;
    height: 2.3rem !important;
    min-height: unset !important;
    padding: 0 !important;
    border-radius: 50% !important;
    background: transparent !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT_MUTED} !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, color 0.2s ease !important;
    line-height: 1 !important;
}}
.st-key-theme_toggle button {{
    right: 1.4rem !important;
    font-size: 0.88rem !important;
}}
.st-key-lang_toggle button {{
    right: 4.3rem !important;
    font-size: 0.58rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
}}
.st-key-theme_toggle button:hover,
.st-key-lang_toggle button:hover {{
    border-color: {TEXT} !important;
    color: {TEXT} !important;
    background: transparent !important;
    box-shadow: none !important;
}}
.st-key-theme_toggle button:focus,
.st-key-theme_toggle button:focus-visible,
.st-key-theme_toggle button:active,
.st-key-lang_toggle button:focus,
.st-key-lang_toggle button:focus-visible,
.st-key-lang_toggle button:active {{
    border-color: {TEXT} !important;
    color: {TEXT} !important;
    box-shadow: none !important;
    outline: none !important;
    background: transparent !important;
}}

/* ── Hero ── */
.hero {{
    text-align: center;
    padding: 0 0 3.5rem 0;
}}
.hero-eyebrow {{
    font-size: 0.62rem;
    letter-spacing: 0.26em;
    text-transform: uppercase;
    color: {TEXT_MUTED};
    margin-bottom: 1.2rem;
    display: block;
}}
.hero-title {{
    font-size: 2.4rem;
    font-weight: 300;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: {TEXT};
    margin: 0 0 1rem 0;
    line-height: 1.2;
}}
.hero-subtitle {{
    font-size: 0.82rem;
    font-weight: 300;
    color: {TEXT_MUTED};
    letter-spacing: 0.04em;
    margin: 0;
}}

/* ── Divider ── */
.divider {{
    border: none !important;
    border-top: 1px solid {BORDER} !important;
    margin: 0;
}}

/* ── Section label ── */
.section-label {{
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: {TEXT_MUTED};
    margin-bottom: 0.8rem;
    display: block;
}}

/* ── File uploader ── */
[data-testid="stFileUploader"] {{
    background: {BG_UPLOAD};
    border: 1px solid {BORDER};
    padding: 1.5rem 2rem;
}}
[data-testid="stFileUploader"] label {{ display: none; }}
[data-testid="stFileUploaderDropzone"] {{
    background: transparent !important;
    border: 1px dashed {BORDER_DASH} !important;
    border-radius: 0 !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] p,
[data-testid="stFileUploaderDropzoneInstructions"] span {{
    font-size: 0.75rem !important;
    color: {TEXT_MUTED} !important;
    letter-spacing: 0.06em !important;
}}
/* Localize Streamlit's built-in dropzone hint (its strings aren't translatable) */
[data-testid="stFileUploaderDropzoneInstructions"] span {{ display: none !important; }}
[data-testid="stFileUploaderDropzoneInstructions"] > div::after {{
    content: "{t["hint"]}";
    font-size: 0.75rem;
    color: {TEXT_MUTED};
    letter-spacing: 0.06em;
}}
/* "Browse files" / Upload button inside the dropzone — match the design in both themes */
[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] {{
    background: transparent !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER_DASH} !important;
    border-radius: 0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, color 0.2s ease !important;
}}
[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] svg {{
    fill: {TEXT} !important;
    color: {TEXT} !important;
}}
/* Localize the browse/upload button label (Streamlit's built-in text) */
[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] [data-testid="stMarkdownContainer"] {{
    display: none !important;
}}
[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]::after {{
    content: "{t["browse"]}";
    margin-left: 0.5rem;
}}
[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]:focus,
[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]:focus-visible,
[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]:active {{
    background: transparent !important;
    border-color: {TEXT} !important;
    color: {TEXT} !important;
    box-shadow: none !important;
    outline: none !important;
}}
/* Uploaded-file chip — keep on-theme in both modes (base theme leaves it dark) */
[data-testid="stFileChip"] {{
    background: {BG2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 0 !important;
    color: {TEXT_MUTED} !important;
}}
[data-testid="stFileChipName"] {{
    color: {TEXT} !important;
}}
[data-testid="stFileChip"] svg,
[data-testid="stFileChip"] [data-testid="stIconMaterial"],
[data-testid="stFileChip"] [data-testid="stFileChipDeleteBtn"] {{
    color: {TEXT_MUTED} !important;
    fill: {TEXT_MUTED} !important;
}}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {{
    background: {BTN_BG} !important;
    color: {BTN_FG} !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
    width: 100% !important;
    box-shadow: none !important;
    transition: opacity 0.2s ease !important;
}}
/* Label text lives in a child <p>/<span> that the global "p,span,div" rule recolors to TEXT,
   making it invisible on the contrasting button fill — force it back to BTN_FG. */
[data-testid="stDownloadButton"] > button p,
[data-testid="stDownloadButton"] > button span,
[data-testid="stDownloadButton"] > button div,
[data-testid="stDownloadButton"] > button [data-testid="stIconMaterial"] {{
    color: {BTN_FG} !important;
    fill: {BTN_FG} !important;
}}
[data-testid="stDownloadButton"] > button:hover {{
    opacity: 0.8 !important;
    background: {BTN_BG} !important;
    color: {BTN_FG} !important;
    box-shadow: none !important;
}}

/* ── Image labels ── */
.img-label {{
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: {TEXT_MUTED};
    margin-bottom: 0.5rem;
    margin-top: 1.5rem;
    display: block;
}}

/* ── Image hover toolbar (fullscreen button) — keep on-theme in both modes ── */
[data-testid="stElementToolbar"],
[data-testid="stElementToolbarButtonContainer"] {{
    background: transparent !important;
}}
[data-testid="stElementToolbarButton"] {{
    background: {BG2} !important;
    color: {TEXT_MUTED} !important;
    border: 1px solid {BORDER} !important;
}}
[data-testid="stElementToolbarButton"] svg,
[data-testid="stElementToolbarButton"] [data-testid="stIconMaterial"] {{
    color: {TEXT_MUTED} !important;
    fill: {TEXT_MUTED} !important;
}}
[data-testid="stElementToolbarButton"]:hover {{
    color: {TEXT} !important;
    border-color: {TEXT} !important;
}}

/* ── Spinner ── */
[data-testid="stSpinner"] p {{
    font-size: 0.7rem !important;
    letter-spacing: 0.16em !important;
    color: {TEXT_MUTED} !important;
    text-transform: uppercase !important;
}}

/* ── Notes ── */
.success-note {{
    font-size: 0.62rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: {TEXT_MUTED};
    text-align: center;
    padding: 0.8rem 0 0 0;
}}
.footer-text {{
    text-align: center;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: {TEXT_SUBTLE};
    padding-top: 1.2rem;
}}
</style>
""", unsafe_allow_html=True)

# ── Control buttons (CSS positions them fixed top-right via .st-key-* classes) ──
# Language toggle — shows the currently active language; click switches it.
if st.button("EN" if lang == "en" else "ES", key="lang_toggle"):
    st.session_state.lang = "es" if lang == "en" else "en"
    st.rerun()

# Theme toggle
if st.button(ICON, key="theme_toggle"):
    st.session_state.dark_mode = not dark
    st.rerun()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <h1 class="hero-title">{t["title"]}</h1>
    <p class="hero-subtitle">{t["subtitle"]}</p>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
st.markdown(f'<span class="section-label">{t["upload"]}</span>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    t["uploader"],
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
)

# ── Processing ────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def process(image_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    result = remove(img)
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    return buf.getvalue()

if uploaded_file:
    raw_bytes = uploaded_file.read()

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    with st.spinner(t["processing"]):
        output_bytes = process(raw_bytes)

    col_before, col_gap, col_after = st.columns([1, 0.08, 1])

    with col_before:
        st.markdown(f'<span class="img-label">{t["original"]}</span>', unsafe_allow_html=True)
        st.image(Image.open(io.BytesIO(raw_bytes)), use_container_width=True)

    with col_after:
        st.markdown(f'<span class="img-label">{t["removed"]}</span>', unsafe_allow_html=True)
        st.image(Image.open(io.BytesIO(output_bytes)), use_container_width=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

    stem = uploaded_file.name.rsplit(".", 1)[0]
    st.download_button(
        label=t["download"],
        data=output_bytes,
        file_name=f"{stem}_no_bg.png",
        mime="image/png",
    )
    st.markdown(f'<p class="success-note">{t["note"]}</p>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<br><br>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(f'<p class="footer-text">{t["footer"]}</p>', unsafe_allow_html=True)
