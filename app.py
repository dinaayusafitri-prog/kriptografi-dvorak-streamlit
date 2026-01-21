import streamlit as st
st.set_page_config(
    page_title="Kriptografi Keyboard Dvorak",
    layout="centered"
)

st.title("🩷 Kriptografi Keyboard Dvorak")
st.write("Aplikasi enkripsi & dekripsi berbasis pergerakan keyboard")


# ================= KEYBOARD DVORAK =================
keyboard = [
    {"row": 1, "keys": list("PYFGCRL")},
    {"row": 0, "keys": list("AOEUIDHTNS")},
    {"row": -1, "keys": list("QJKXBMWVZ")}
]

def get_pos(h):
    for r in keyboard:
        if h in r["keys"]:
            return r["row"], r["keys"].index(h)
    return None, None

def get_key(row, col):
    for r in keyboard:
        if r["row"] == row and 0 <= col < len(r["keys"]):
            return r["keys"][col]
    return "?"

# ================= ENKRIPSI =================
def encrypt(text):
    text = text.upper()
    clean = text.replace(" ", "")
    if not clean:
        return ""

    acuan = clean[-1]
    hasil = ""

    for ch in text:
        if ch == " ":
            continue

        ra, ca = get_pos(acuan)
        rb, cb = get_pos(ch)

        dc = cb - ca
        dr = rb - ra

        part_c = f"↓{dc}" if dc > 0 else f"↑{abs(dc)}" if dc < 0 else "0"
        part_r = f"+{dr}" if dr > 0 else f"{dr}" if dr < 0 else "0"

        hasil += part_c + part_r
        acuan = ch

    return hasil

# ================= DEKRIPSI =================
def decrypt(cipher, acuan):
    tokens = re.findall(r"[↑↓]?\d+[+-]\d+", cipher)
    hasil = ""
    ref = acuan.upper()

    for t in tokens:
        m = re.match(r"([↑↓]?)(\d+)([+-])(\d+)", t)
        if not m:
            continue

        dir_c = 1 if m.group(1) == "↓" else -1 if m.group(1) == "↑" else 0
        val_c = int(m.group(2))
        dir_r = 1 if m.group(3) == "+" else -1
        val_r = int(m.group(4))

        row, col = get_pos(ref)
        row_data = next(r for r in keyboard if r["row"] == row)

        col = (col + dir_c * val_c) % len(row_data["keys"])
        row = max(-1, min(1, row + dir_r * (1 if val_r != 0 else 0)))

        key = get_key(row, col)
        hasil += key
        ref = key

    return hasil

# ================= STREAMLIT UI =================
st.set_page_config(page_title="Kriptografi Dvorak", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(160deg, #ffe4ec, #ffd1dc);
}
textarea, input {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🩷 Kriptografi Keyboard Dvorak")
st.write("Enkripsi & Dekripsi berbasis pergerakan relatif keyboard")

st.subheader("🔐 Plaintext → Ciphertext")
pt = st.text_area("Plaintext")
if st.button("Enkripsi"):
    st.text_area("Ciphertext", encrypt(pt), height=120)

st.divider()

st.subheader("🔓 Ciphertext → Plaintext")
ct = st.text_area("Ciphertext")
ac = st.text_input("Huruf acuan awal")
if st.button("Dekripsi"):
    if ac:
        st.text_area("Hasil Plaintext", decrypt(ct, ac), height=120)
