import streamlit as st
import database as db

# Konfigurasi halaman dasar dengan icon yang lucu
st.set_page_config(page_title="Our Shared Space", page_icon="💖", layout="centered")

# --- CUSTOM CSS UNTUK TAMPILAN COLORFUL & FUN ---
st.markdown("""
    <style>
    /* Mengubah font header utama agar lebih estetik */
    .main-title {
        font-family: 'Poppins', sans-serif;
        color: #FF4B4B;
        text-align: center;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #FF7A00;
        font-style: italic;
        margin-bottom: 30px;
    }
    /* Mengubah gaya container jurnal di timeline */
    .journal-card {
        background-color: #FFF5F5;
        border-left: 5px solid #FF4B4B;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .journal-card-partner {
        background-color: #F0F4FF;
        border-left: 5px solid #1E90FF;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi session state untuk status login
if "user" not in st.session_state:
    st.session_state.user = None

# ========================================================
# 🔒 HALAMAN AKSES (LOGIN & REGISTER SEBELUM MASUK UTAMA)
# ========================================================
if st.session_state.user is None:
    st.markdown("<p class='main-title'>🔐 Shared Space</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Tempat rahasia cerita kita berdua ✨</p>", unsafe_allow_html=True)
    
    # Membuat Tab yang colorful untuk memisahkan Login dan Register
    tab_login, tab_register = st.tabs(["✨ Masuk (Login)", "🌱 Daftar Baru (Sign Up)"])
    
    # --- FORM LOGIN ---
    with tab_login:
        st.write("") # Spacer
        with st.form("login_form"):
            st.markdown("### Selamat Datang Kembali! 👋")
            email_login = st.text_input("Email Terdaftar", placeholder="kamu@email.com")
            pass_login = st.text_input("Kata Sandi", type="password", placeholder="******")
            
            submit_login = st.form_submit_with_button("Buka Pintu Jurnal 🔑", use_container_width=True)
            
            if submit_login:
                if email_login and pass_login:
                    user_data = db.login_user(email_login, pass_login)
                    if user_data:
                        st.session_state.user = user_data
                        st.toast("Yay! Selamat datang kembali 🥰", icon="❤️")
                        st.rerun()
                else:
                    st.warning("Eits, isi email dan password kamu dulu ya!")

    # --- FORM REGISTRASI ---
    with tab_register:
        st.write("") # Spacer
        with st.form("register_form"):
            st.markdown("### Mulai Perjalanan Bersama 🚀")
            email_reg = st.text_input("Email Baru", placeholder="pasanganmu@email.com")
            pass_reg = st.text_input("Buat Kata Sandi", type="password", placeholder="Minimal 6 karakter")
            pass_confirm = st.text_input("Ulangi Kata Sandi", type="password", placeholder="Pastikan sama ya")
            
            submit_reg = st.form_submit_with_button("Buat Akun Kita 🎉", use_container_width=True)
            
            if submit_reg:
                if pass_reg != pass_confirm:
                    st.error("Waduh, kata sandinya nggak cocok nih. Coba dicek lagi.")
                elif len(pass_reg) < 6:
                    st.warning("Biar aman, kata sandi minimal 6 karakter ya!")
                elif email_reg and pass_reg:
                    new_user = db.register_user(email_reg, pass_reg)
                    if new_user:
                        st.success("Hore! Akun berhasil dibuat. Sekarang kamu bisa langsung klik tab 'Masuk' di atas!")
                else:
                    st.warning("Semua kolom wajib diisi ya!")

# ========================================================
# 🏡 HALAMAN UTAMA (SETELAH BERHASIL LOGIN)
# ========================================================
else:
    current_user = st.session_state.user
    
    # Top Bar: Judul & Tombol Keluar yang Rapi
    col_header, col_logout = st.columns([4, 1])
    with col_header:
        st.markdown("<h2 style='color: #FF4B4B; margin:0;'>📝 Our Shared Journal</h2>", unsafe_allow_html=True)
        st.caption(f"Menjaga kenangan bersama: **{current_user.email}** 💫")
    with col_logout:
        st.write("") # Penyelaras posisi vertical
        if st.button("Keluar 🚪", use_container_width=True):
            db.logout_user()
            st.session_state.user = None
            st.rerun()
            
    st.divider()

    # Navigasi Menu Utama dengan Gaya Tombol Radio Horizontal
    menu = st.radio(
        "Mau melakukan apa hari ini?", 
        ["📖 Baca Timeline Cerita", "✍️ Tulis Cerita Baru"], 
        horizontal=True
    )
    st.write("")

    # --- MENU 1: TULIS JURNAL BARU ---
    if menu == "✍️ Tulis Cerita Baru":
        st.markdown("### Ada cerita seru apa hari ini? 🤔")
        
        with st.form("journal_entry_form", clear_on_submit=True):
            title = st.text_input("Judul Momen Hari Ini", placeholder="Misal: Kencan mendadak yang seru!")
            content = st.text_area("Tumpahkan ceritamu di sini...", placeholder="Hari ini kita pergi ke...", height=200)
            
            # Menggunakan warna tombol bawaan streamlit yang mencolok
            submit_journal = st.form_submit_with_button("Simpan Momen Ini ❤️", use_container_width=True)
            
            if submit_journal:
                if title and content:
                    db.insert_journal(current_user.id, current_user.email, title, content)
                    st.balloons() # Efek balon terbang biar seru!
                    st.success("Cerita kamu aman tersimpan di kapsul waktu kita! ✨")
                else:
                    st.warning("Judul dan ceritanya diisi dulu ya, jangan dikosongkan.")

    # --- MENU 2: TIMELINE BERSAMA ---
    elif menu == "📖 Baca Timeline Cerita":
        st.markdown("### ⏳ Menyusuri Lorong Waktu")
        journals = db.get_all_journals()
        
        if not journals:
            st.info("Belum ada cerita yang terukir di sini. Yuk, jadi yang pertama menulis hari ini! 🦄")
        else:
            for journal in journals:
                # Cek apakah ini tulisan sendiri atau pasangan
                is_self = journal["user_email"] == current_user.email
                penulis = "Kamu" if is_self else journal["user_email"]
                
                # Gunakan CSS Box khusus yang colorful berdasarkan siapa yang menulis
                card_style = "journal-card" if is_self else "journal-card-partner"
                
                st.markdown(f"""
                    <div class="{card_style}">
                        <h3 style="margin: 0 0 5px 0; color: #333;">{journal['title']}</h3>
                        <p style="margin: 0 0 10px 0; font-size: 0.85rem; color: #777;">
                            ✍️ Ditulis oleh <b>{penulis}</b> • 📅 {journal['created_at'][:10]}
                        </p>
                        <p style="margin: 0; color: #444; white-space: pre-line;">{journal['content']}</p>
                    </div>
                """, unsafe_allow_html=True)
