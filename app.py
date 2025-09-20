import streamlit as st
import base64
from pathlib import Path
import re

st.set_page_config(page_title="Agrawal Dental And Oral Care Bhopal", layout="wide")

# --- 1️⃣ Load HTML content ---
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()



# --- 2️⃣ Embed images as base64 ---
def encode_file_to_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Background image
bg_base64 = encode_file_to_base64("background.jpg")
html_content = html_content.replace(
    "url('background.jpg')",
    f"url('data:image/jpeg;base64,{bg_base64}')"
)

# Logo
logo_base64 = encode_file_to_base64("logo.png")
html_content = html_content.replace(
    '<img src="logo.png"',
    f'<img src="data:image/png;base64,{logo_base64}"'
)

# --- 3️⃣ Embed reviews.txt into JS ---
with open("reviews.txt", "r", encoding="utf-8") as f:
    reviews = [line.strip() for line in f if line.strip() != ""]

reviews_js_array = str(reviews)

# Replace loadReview function
load_review_js = f"""
function loadReview() {{
    const reviews = {reviews_js_array};
    if(reviews.length === 0) {{
        reviewText.textContent = "No reviews available!";
        return;
    }}
    const randomIndex = Math.floor(Math.random() * reviews.length);
    review = reviews[randomIndex];
    reviewText.textContent = review;
}}
"""
html_content = re.sub(r'function loadReview\(\)\s*{{.*?}}', load_review_js, html_content, flags=re.DOTALL)

# --- 4️⃣ Embed CSS inline ---
css_files = ["./static/css/index.BOl9eq08.css"]  # Add more CSS files if needed
for css_file in css_files:
    path = Path(css_file)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            css_content = f.read()
        # Remove crossorigin and embed
        link_tag_pattern = re.escape(f'<link rel="stylesheet" crossorigin href="{css_file}">')
        html_content = re.sub(link_tag_pattern, f"<style>{css_content}</style>", html_content)

# --- 5️⃣ Embed JS inline ---
js_files = ["./static/js/main.js"]  # Add more JS files if needed
for js_file in js_files:
    path = Path(js_file)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            js_content = f.read()
        # Remove crossorigin and embed
        script_tag_pattern = re.escape(f'<script src="{js_file}" crossorigin></script>')
        html_content = re.sub(script_tag_pattern, f"<script>{js_content}</script>", html_content)

# --- 6️⃣ Display HTML in Streamlit ---
st.components.v1.html(html_content, height=1000, scrolling=True)
