from pathlib import Path
import logging
import streamlit as st

logger = logging.getLogger(__name__)


# Read and cache raw CSS text from disk to optimize Streamlit reruns
@st.cache_data(show_spinner=False)
def _read_css_file(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to read CSS file at {file_path}: {e}")
        return ""


# Resolves, reads, and injects global styling into the Streamlit DOM
def inject_global_css(css_relative_path: str = "assets/style.css") -> None:
    # Absolute path anchor based on project root
    project_root = Path(__file__).resolve().parent.parent
    full_path = project_root / css_relative_path

    if not full_path.is_file():
        logger.warning(f"Stylesheet target does not exist: {full_path}")
        return

    css_content = _read_css_file(full_path)
    if css_content:
        logger.info("Located & Loaded css file!")
        print("Located & Loaded css file!")
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)