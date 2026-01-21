import streamlit as st
import re
import string

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Kriptografi Keyboard Dvorak",
    layout="centered"
)

# =============================
# CUSTOM STYLE (HIDUP & NATURAL)
# =============================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #f6dce3 0%, #fffafc 70%);
}

.block-container {
    padding-top: 2.5rem;
    max-width: 820px;
}

h1 {
    color: #3b1f2b;
    font-weight: 700;
}

h2 {
    color: #5a2a3a;
}

p {
    color: #3d3d3d;
}

.card {
    background: white;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 10px 28px rgba(0,0,0,0.08);
}

label {
    font-weight: 600;
    color: #5a2a3a;
}

textarea, input {
    background-color: #ffffff !important;
    color: #1f1f1f !important;
    border-radius: 10px !important;
    border: 1px solid #e0b7c5 !important;
}

.stButton button {
    background-color: #b94a6a;
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    border: none;
}

.stButton button:hover {
    background-color: #983c57;
}

.footer {
    text-align: center;
    color: #6b4a56;
    margin-top: 2rem;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# =============================
# DATA
# =============================
ALPHABET = string.ascii_uppercase

# =============================
# ENCRYPT
# =============================
def encrypt(plaintext):
    plaintext = plaintext.upper()
    prev_index = ALPHABET.index("I")
    result = []

    for ch in plaintext:
        if ch in ALPHABET:
            curr = ALPHABET.index(ch)
            diff = curr - prev_index

            arrow = "↑" if diff >= 0 else "↓"
            step = abs(diff) * 10
            tweak = "+1" if diff >= 0 else "-1"

            result.append(f"{arrow}{step}{tweak}")
            prev_index = curr
        else:
            result.append(ch)

    return "".join(result)

# =============================
# DECRYPT
# =============================
def decrypt(ciphertext, start_char):
    start_char = start_char.upper()

    if start_char not in ALPHABET:
        return "Huruf acuan tidak valid"

    tokens = re.findall(r"[↑↓]\d+[+-]1", ciphertext)
    prev = ALPHABET.index(start_char)
    result = []

    for t in tokens:
        arrow = t[0]
        number = int(t[1:-2])
        shift = number // 10
        direction = 1 if arrow == "↑" else -1

        curr = (prev + direction * shift) % 26
        result.append(ALPHABET[curr])
        prev = curr

    return "".join(result)

# =============================
# UI CONTENT
# =============================
st.title("Kriptografi Keyboard Dvorak")
st.write("Aplikasi enkripsi dan dekripsi berbasis pergerakan relatif keyboard Dvorak.")

# ---------- CARD 1 ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Plaintext → Ciphertext")
pt = st.text_area("Masukkan Plaintext", height=120)

if st.button("Enkripsi"):
    if pt.strip():
        ct = encrypt(pt)
        st.text_area("Hasil Ciphertext", ct, height=140)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- CARD 2 ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Ciphertext → Plaintext")
ct_input = st.text_area("Masukkan Ciphertext", height=140)
acuan = st.text_input("Huruf acuan awal", value="I")

if st.button("Dekripsi"):
    if ct_input.strip():
        hasil = decrypt(ct_input, acuan)
        st.text_area("Hasil Plaintext", hasil, height=120)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(
    "<div class='footer'>Dina Ayu Safitri — Kriptografi Keyboard Dvorak</div>",
    unsafe_allow_html=True
)
