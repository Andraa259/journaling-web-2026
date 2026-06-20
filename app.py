import streamlit as st
import database as db
from streamlit_cookies_controller import CookieController

# 1. Inisialisasi Cookie Controller
controller = CookieController()

st.set_page_config(page_title="Our Shared Space", page_icon="💖", layout="centered")

# --- PREMIUM COLORFUL & ROMANTIC JOURNALING CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;700&family=Poppins:wght@400;600;800&display=swap');
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #FFEBEB 0%, #FFF0E5 50%, #FFE4E4 100%) !important;
    }
    .main-title { font-family: 'Comfortaa', cursive; color: #D14343; text-align: center; font-weight: 800; font-size: 3.5rem; margin-bottom: 0px; }
    .sub-title { text-align: center; color: #E07A5F; font-style: italic; font-family: 'Comfortaa', cursive; margin-bottom: 40px; }
    .journal-card { background: rgba(255, 255, 255, 0.85); border-radius: 20px; padding: 22px; margin-bottom: 20px; border-left: 6px solid #FF6B6B; backdrop-filter: blur(10px); }
    .journal-card-partner { background: rgba(255, 255, 255, 0.85); border-radius: 20px; padding: 22px; margin-bottom: 20px; border-left: 6px solid #1E90FF; backdrop-filter: blur(10px); }
    .stButton > button { border-radius: 12px; font-weight: 600; }
    .avatar-img { border-radius: 50%; border: 3px solid white; object-fit: cover; }
    .profile-badge { background: rgba(255,255,255,0.8); padding: 20px; border-radius: 20px; text-align: center; backdrop-filter: blur(5px); }
    div[data-testid="stPopover"] > button { border: none !important; background: transparent !important; font-size: 1.3rem !important; color: #888 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Cek apakah ada cookie login yang tersimpan dari kunjungan sebelumnya
saved_user_id = controller.get("user_id")

if "user" not in st.session_state:
    st.session_state.user = None

# Jika session kosong tapi cookie ada, otomatis pulihkan session login
if st.session_state.user is None and saved_user_id:
    # Buat objek tiruan user dengan ID dari cookie agar aplikasi mengenali
    class UserMock:
        def __init__(self, id):
            self.id = id
    st.session_state.user = UserMock(saved_user_id)

if "current_page" not in st.session_state:
    st.session_state.current_page = "📖 Baca Timeline"

# ========================================================
# 🔒 GERBANG MASUK (LOGIN)
# ========================================================
if st.session_state.user is None:
    st.markdown("<p class='main-title'>💖 Shared Space</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Ruang rahasia memori kita berdua ✨</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("<h3 style='text-align: center; color: #D14343;'>Selamat Datang Kembali 💕</h3>", unsafe_allow_html=True)
        identifier = st.text_input("Username atau Email", placeholder="rian123 / amelia@email.com")
        pass_login = st.text_input("Kata Sandi", type="password", placeholder="******")
        submit_login = st.form_submit_button("Buka Pintu Jurnal 🔑", use_container_width=True)
        
        if submit_login:
            if identifier and pass_login:
                user_data = db.login_user_flexible(identifier, pass_login)
                if user_data:
                    st.session_state.user = user_data
                    
                    # 3. SIMPAN COOKIE SELAMA 30 MENIT (1800 detik)
                    # Cookie ini akan otomatis dihapus oleh browser setelah 30 menit
                    controller.set("user_id", user_data.id, max_age=1800)
                    
                    st.toast("Pintu kamar kenangan berhasil dibuka! 🥰", icon="❤️")
                    st.rerun()
            else:
                st.warning("Kolom masuk dan kata sandi wajib diisi!")

# ========================================================
# 🏡 HALAMAN UTAMA (SETELAH LOGIN)
# ========================================================
else:
    # Validasi proteksi ganda jika data profil gagal ditarik
    try:
        profile = db.get_user_profile(st.session_state.user.id)
    except Exception:
        # Jika session rusak/cookie kedaluwarsa di sisi Supabase, paksa logout
        controller.remove("user_id")
        st.session_state.user = None
        st.rerun()
        
    # Header Atas
    col_header, col_logout = st.columns([4, 1])
    with col_header:
        st.markdown("<h1 style='color: #D14343; font-family:\"Comfortaa\"; margin:0;'>Shared Journal</h1>", unsafe_allow_html=True)
        st.caption(f"✨ Ruang rajutan memori milik **{profile['nickname']}** (@{profile['username']})")
    with col_logout:
        st.write("")
        if st.button("Keluar 🚪", use_container_width=True):
            db.logout_user()
            # 4. HAPUS COOKIE SAAT KLIK LOGOUT SECARA MANUAL
            controller.remove("user_id")
            st.session_state.user = None
            st.rerun()
            
    st.write("")

    # --- NAVIGASI ELEGAN ---
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    with col_nav1:
        if st.button("📖\n\nBaca Timeline", use_container_width=True, key="nav_t1"):
            st.session_state.current_page = "📖 Baca Timeline"
    with col_nav2:
        if st.button("✍️\n\nTulis Cerita Baru", use_container_width=True, key="nav_t2"):
            st.session_state.current_page = "✍️ Tulis Cerita Baru"
    with col_nav3:
        if st.button("👤\n\nProfil & Keamanan", use_container_width=True, key="nav_t3"):
            st.session_state.current_page = "👤 Profil & Keamanan"

    st.divider()

    # --- KODE UNTUK MENU 1, 2, DAN 3 TETAP SAMA SEPERTI SEBELUMNYA ---
    if st.session_state.current_page == "📖 Baca Timeline":
        st.markdown("<h3 style='color:#D14343; font-family:\"Comfortaa\";'>⏳ Menyusuri Lorong Waktu</h3>", unsafe_allow_html=True)
        journals = db.get_all_journals_with_profiles()
        
        if not journals:
            st.info("Belum ada lembaran cerita hari ini. Yuk tulis momen pertamamu! 🦄")
        else:
            for journal in journals:
                is_self = journal["user_id"] == profile["id"]
                p_info = journal["profiles"]
                p_nickname = p_info["nickname"] if p_info else "Seseorang"
                p_avatar = p_info["avatar_url"] if p_info else ""
                penulis = f"Kamu ({p_nickname})" if is_self else p_nickname
                card_style = "journal-card" if is_self else "journal-card-partner"
                
                with st.container():
                    col_card_left, col_card_right = st.columns([15, 1])
                    with col_card_left:
                        st.markdown(f"""
                            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                                <img src="{p_avatar}" width="45" height="45" class="avatar-img" style="margin-right: 15px;"/>
                                <div>
                                    <h4 style="margin: 0; color: #333; font-size:1.2rem;">{journal['title']}</h4>
                                    <p style="margin: 0; font-size: 0.8rem; color: #777;">✍️ Oleh <b>{penulis}</b> • 📅 {journal['created_at'][:10]}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_card_right:
                        if is_self:
                            with st.popover("⋮", help="Opsi Jurnal"):
                                st.markdown("<p style='font-size:0.85rem; font-weight:bold; margin:0;'>Aksi Cerita</p>", unsafe_allow_html=True)
                                with st.expander(label="✏️ Edit Cerita", expanded=False):
                                    edit_title = st.text_input("Judul Baru", value=journal["title"], key=f"et_{journal['id']}")
                                    edit_content = st.text_area("Konten Baru", value=journal["content"], key=f"ec_{journal['id']}")
                                    if st.button("Simpan Perubahan", key=f"es_{journal['id']}", use_container_width=True):
                                        if db.update_journal(journal["id"], edit_title, edit_content):
                                            st.success("Jurnal diperbarui!")
                                            st.rerun()
                                if st.button("🗑️ Hapus Permanen", key=f"del_{journal['id']}", use_container_width=True):
                                    if db.delete_journal(journal["id"]):
                                        st.toast("Satu kenangan telah dihapus.", icon="🗑️")
                                        st.rerun()
                    st.markdown(f"""
                        <div class="{card_style}" style="margin-top:-25px;">
                            <p style="margin: 0; color: #444; line-height: 1.6; white-space: pre-line;">{journal['content']}</p>
                        </div>
                    """, unsafe_allow_html=True)

    elif st.session_state.current_page == "✍️ Tulis Cerita Baru":
        st.markdown("<h3 style='color:#D14343; font-family:\"Comfortaa\";'>✍️ Ukir Kisah Hari Ini</h3>", unsafe_allow_html=True)
        with st.form("journal_entry_form", clear_on_submit=True):
            title = st.text_input("Judul Momen Indah", placeholder="Misal: Saling bertukar kado kejutan!")
            content = st.text_area("Tumpahkan seluruh isi pikiran dan perasaanmu di sini...", placeholder="Hari ini sangat berkesan karena...", height=250)
            submit_journal = st.form_submit_button("Simpan ke Kapsul Waktu 💖", use_container_width=True)
            if submit_journal:
                if title and content:
                    db.insert_journal(profile["id"], title, content)
                    st.balloons()
                    st.success("Ceritamu berhasil mendarat dengan aman!")
                else:
                    st.warning("Judul dan ceritanya diisi dengan lengkap dulu ya.")

    elif st.session_state.current_page == "👤 Profil & Keamanan":
        st.markdown("<h3 style='color:#444; font-family:\"Comfortaa\";'>👥 Ruang Identitas Kita</h3>", unsafe_allow_html=True)
        partner_profile = db.get_partner_profile(profile["id"])
        col_my_p, col_partner_p = st.columns(2)
        with col_my_p:
            st.markdown("<div class='profile-badge'>", unsafe_allow_html=True)
            st.markdown("<h4>👑 Profil Kamu</h4>", unsafe_allow_html=True)
            st.image(profile["avatar_url"], width=100)
            st.markdown(f"**{profile['nickname']}**<br><span style='color:#777;'>@{profile['username']}</span>", unsafe_allow_html=True)
            st.caption(f"✉️ {profile['email']}")
            st.markdown("</div>", unsafe_allow_html=True)
        with col_partner_p:
            st.markdown("<div class='profile-badge'>", unsafe_allow_html=True)
            st.markdown("<h4>❤️ Profil Pasangan</h4>", unsafe_allow_html=True)
            if partner_profile:
                st.image(partner_profile["avatar_url"], width=100)
                st.markdown(f"**{partner_profile['nickname']}**<br><span style='color:#777;'>@{partner_profile['username']}</span>", unsafe_allow_html=True)
                st.caption(f"✉️ {partner_profile['email']}")
            else:
                st.info("Pasangan belum bergabung.")
            st.markdown("</div>", unsafe_allow_html=True)
        st.divider()
        with st.form("edit_profile_form"):
            edit_nickname = st.text_input("Nama Panggilan Baru", value=profile["nickname"])
            edit_username = st.text_input("Username Baru", value=profile["username"])
            uploaded_file = st.file_uploader("Pilih Foto Profil Baru (PNG/JPG)", type=["png", "jpg", "jpeg"])
            submit_profile = st.form_submit_button("Simpan Perubahan Profil ✨", use_container_width=True)
            if submit_profile:
                final_avatar_url = profile["avatar_url"]
                if uploaded_file is not None:
                    file_bytes = uploaded_file.read()
                    file_name = uploaded_file.name
                    with st.spinner("Sedang mengunggah foto profil..."):
                        uploaded_url = db.upload_avatar(profile["id"], file_bytes, file_name)
                        if uploaded_url:
                            final_avatar_url = uploaded_url
                if edit_nickname and edit_username:
                    if db.update_user_profile_data(profile["id"], edit_nickname, edit_username, final_avatar_url):
                        st.success("Data profil dan foto berhasil diperbarui! 🪄")
                        st.rerun()
        st.divider()
        with st.form("change_password_form", clear_on_submit=True):
            new_pass = st.text_input("Kata Sandi Baru", type="password", placeholder="Minimal 6 karakter")
            confirm_new_pass = st.text_input("Konfirmasi Kata Sandi Baru", type="password", placeholder="Ulangi kata sandi")
            submit_change_pass = st.form_submit_button("Perbarui Kata Sandi Akun 🛠️", use_container_width=True)
            if submit_change_pass:
                if len(new_pass) < 6:
                    st.warning("Kata sandi baru minimal harus 6 karakter ya!")
                elif new_pass != confirm_new_pass:
                    st.error("Konfirmasi kata sandi tidak cocok.")
                else:
                    if db.change_password(new_pass):
                        st.success("Kata sandi akunmu berhasil diubah dengan aman! 🔑")
