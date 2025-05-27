import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# SETUP STREAMLIT 
st.markdown("""
    <div style="
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 50%, #fdbb2d 100%);
        padding: 2rem 3rem;
        border-radius: 15px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        color: white;
        margin-bottom: 2rem;
    ">
        <div style="flex: 3; text-align: left;">
            <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem;"> AI Color Palette Extractor</h1>
            <p style="font-size: 1.2rem; margin: 0;">
                TUGAS 6 AI PRAKTIKUM : Mengubah gambar menjadi palet warna dominan dengan K-Means.
            </p>
        </div>
        <div style="flex: 1; text-align: right; font-size: 1rem;">
            <p style="margin: 0;">👨‍💻 David Christian Nathaniel</p>
            <p style="margin: 0;">140810230027</p>
        </div>
    </div>
""", unsafe_allow_html=True)


# FILE UPLOADER 
uploaded_file = st.file_uploader("📂 Unggah gambar di sini", type=["jpg", "jpeg", "png"])

#  WARNA DOMINAN 
def get_palette(image, k=5):
    image = image.resize((150, 150))  # kecilkan untuk efisiensi
    img_array = np.array(image)
    img_array = img_array.reshape((-1, 3))  # ubah jadi array 2D (RGB)

    kmeans = KMeans(n_clusters=k, n_init=10)
    labels = kmeans.fit_predict(img_array)
    centers = np.round(kmeans.cluster_centers_).astype(int)
    counts = np.bincount(labels)

    return centers, counts

#  JIKA GAMBAR ADA 
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Gambar yang diunggah", use_column_width=True)

    with st.spinner("🔍 Menganalisis warna dominan..."):
        centers, counts = get_palette(image)

    hex_colors = ['#%02x%02x%02x' % tuple(c) for c in centers]
    total_pixels = sum(counts)
    proportions = [round((count / total_pixels) * 100, 2) for count in counts]

    #  TAMPILKAN PALET WARNA 
    st.markdown("### 🎯 Palet Warna Dominan")
    color_cols = st.columns(len(centers))
    for idx, col in enumerate(color_cols):
        with col:
            st.markdown(f"<div style='background-color:{hex_colors[idx]}; padding:30px; border-radius:10px'></div>", unsafe_allow_html=True)
            st.text(f"{hex_colors[idx]}")
            st.caption(f"RGB: {tuple(centers[idx])}\n{proportions[idx]}%")

    #  PIE CHART 
    st.markdown("### 📊 Proporsi Warna (Pie Chart)")
    fig, ax = plt.subplots()
    ax.pie(proportions, labels=hex_colors, colors=hex_colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

#  FOOTER IDENTITAS 
st.markdown("---")
st.markdown("<p style='text-align: center;'>Dibuat oleh <strong>David Christian Nathaniel</strong> | NPM: 140810230027</p>", unsafe_allow_html=True)
