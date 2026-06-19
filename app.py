import streamlit as st
import database as db

st.set_page_config(page_title="Our Shared Space", page_icon="💖", layout="centered")

# --- CUSTOM CSS UNTUK TAMPILAN COLORFUL & FUN ---
st.markdown("""
    <style>
    .main-title { font-family: 'Poppins', sans-serif; color: #FF4B4B; text-align: center; font-weight: 800; font-size: 3rem; margin-bottom: 0px; }
    .sub-title { text-align: center; color: #FF7A00; font-style: italic; margin-bottom: 30px; }
    .journal-card { background-color: #FFF5F5; border-left: 5px solid #FF4B4B; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .journal-card-partner { background-color: #F0F4FF; border-left: 5px solid #1E90FF; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .avatar-img { border-radius: 50%; border: 3px solid #FF4B4B; background-color: white; }
    </style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

# ========================================================
# 🔒 GERBANG MASUK (LOGIN)
# ========================================================
if st.session_state.user is None:
    st.markdown("<p class='main-title'>🔐 Shared Space</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Tempat rahasia cerita kita berdua ✨</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("### Masuk ke Ruang Cerita 👋")
        identifier = st.text_input("Username atau Email", placeholder="rian123 atau kamu@email.com")
        pass_login = st.text_input("Kata Sandi", type="password", placeholder="******")
        submit_login = st.form_submit_button("Buka Pintu Jurnal 🔑", use_container_width=True)
        
        if submit_login:
            if identifier and pass_login:
                user_data = db.login_user_flexible(identifier, pass_login)
                if user_data:
                    st.session_state.user = user_data
                    st.toast("Yay! Selamat datang kembali 🥰", icon="❤️")
                    st.rerun()
            else:
                st.warning("Kolom masuk dan kata sandi diisi dulu ya!")

# ========================================================
# 🏡 HALAMAN UTAMA (SETELAH LOGIN)
# ========================================================
else:
    # Tarik data profil dinamis dari tabel public.profiles
    profile = db.get_user_profile(st.session_state.user.id)
    
    # Top Bar Header
    col_header, col_logout = st.columns([4, 1])
    with col_header:
        st.markdown("<h2 style='color: #FF4B4B; margin:0;'>📝 Our Shared Journal</h2>", unsafe_allow_html=True)
        st.caption(f"Halo, **{profile['nickname']}** (@{profile['username']})! ✨")
    with col_logout:
        st.write("") 
        if st.button("Keluar 🚪", use_container_width=True):
            db.logout_user()
            st.session_state.user = None
            st.rerun()
            
    st.divider()

    menu = st.radio(
        "Mau melakukan apa hari ini?", 
        ["📖 Baca Timeline", "✍️ Tulis Cerita Baru", "👤 Profil & Keamanan"], 
        horizontal=True
    )
    st.write("")

    # --- MENU 1: TIMELINE BERSAMA ---
    if menu == "📖 Baca Timeline":
        st.markdown("### ⏳ Menyusuri Lorong Waktu")
        journals = db.get_all_journals_with_profiles()
        
        if not journals:
            st.info("Belum ada cerita yang terukir di sini. Yuk, mulai menulis hari ini! 🦄")
        else:
            for journal in journals:
                is_self = journal["user_id"] == profile["id"]
                
                # Mengambil informasi profil penulis hasil relasi database
                p_info = journal["profiles"]
                p_nickname = p_info["nickname"] if p_info else "Seseorang"
                p_avatar = p_info["avatar_url"] if p_info else ""
                
                penulis = f"Kamu ({p_nickname})" if is_self else p_nickname
                card_style = "journal-card" if is_self else "journal-card-partner"
                
                # Render kartu dengan menampilkan Avatar/Profile Picture
                st.markdown(f"""
                    <div class="{card_style}">
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <img src="{p_avatar}" width="40" height="40" class="avatar-img" style="margin-right: 12px;"/>
                            <div>
                                <h3 style="margin: 0; color: #333; font-size:1.2rem;">{journal['title']}</h3>
                                <p style="margin: 0; font-size: 0.8rem; color: #777;">
                                    ✍️ Oleh <b>{penulis}</b> • 📅 {journal['created_at'][:10]}
                                </p>
                            </div>
                        </div>
                        <p style="margin: 5px 0 0 0; color: #444; white-space: pre-line;">{journal['content']}</p>
                    </div>
                """, unsafe_allow_html=True)

    # --- MENU 2: TULIS JURNAL BARU ---
    elif menu == "✍️ Tulis Cerita Baru":
        st.markdown("### Ada cerita seru apa hari ini? 🤔")
        with st.form("journal_entry_form", clear_on_submit=True):
            title = st.text_input("Judul Momen Hari Ini", placeholder="Misal: Cerita hari ini...")
            content = st.text_area("Tumpahkan ceritamu di sini...", placeholder="Hari ini kita...", height=200)
            submit_journal = st.form_submit_button("Simpan Momen Ini ❤️", use_container_width=True)
            
            if submit_journal:
                if title and content:
                    db.insert_journal(profile["id"], title, content)
                    st.balloons() 
                    st.success("Cerita kamu aman tersimpan di kapsul waktu kita! ✨")
                else:
                    st.warning("Judul dan ceritanya diisi dulu ya.")

    # --- MENU 3: PROFIL & KEAMANAN (LENGKAP) ---
    elif menu == "👤 Profil & Keamanan":
        st.markdown("### 👤 Kartu Identitas & Pengaturan Akun")
        
        # Sesi Tampilan Profil (Menampilkan Ava, Username, Email)
        col_ava, col_details = st.columns([1, 3])
        with col_ava:
            st.image(profile["avatar_url"], width=120)
        with col_details:
            st.markdown(f"**Nama Panggilan:** {profile['nickname']}")
            st.markdown(f"**Username Akun:** `@{profile['username']}`")
            st.markdown(f"**Email Terhubung:** `{profile['email']}`")
            
        st.divider()
        
        # Sub-menu Edit Profil Data
        st.markdown("#### ✏️ Perbarui Data Profil")
        with st.form("edit_profile_form"):
            edit_nickname = st.text_input("Nama Panggilan Baru", value=profile["nickname"])
            edit_username = st.text_input("Username Baru", value=profile["username"])
            edit_avatar = st.text_input("URL Foto Profil Baru (Link Gambar/SVG)", value=profile["avatar_url"])
            submit_profile = st.form_submit_button("Simpan Perubahan Data Profil ✨")
            
            if submit_profile:
                if edit_nickname and edit_username:
                    if db.update_user_profile_data(profile["id"], edit_nickname, edit_username, edit_avatar):
                        st.success("Profil kamu berhasil diperbarui! Silakan refresh halaman.")
                        st.rerun()
                else:
                    st.warning("Nama panggilan dan username tidak boleh dikosongkan.")

        st.divider()

        # Sub-menu Ubah Password
        st.markdown("#### 🔑 Ganti Kata Sandi")
        with st.form("change_password_form", clear_on_submit=True):
            new_pass = st.text_input("Kata Sandi Baru", type="password", placeholder="Minimal 6 karakter")
            confirm_new_pass = st.text_input("Konfirmasi Kata Sandi Baru", type="password", placeholder="Ulangi kata sandi")
            submit_change_pass = st.form_submit_button("Perbarui Kata Sandi 🛠️", use_container_width=True)
            
            if submit_change_pass:
                if len(new_pass) < 6:
                    st.warning("Password baru minimal harus 6 karakter ya!")
                elif new_pass != confirm_new_pass:
                    st.error("Konfirmasi password tidak cocok.")
                else:
                    if db.change_password(new_pass):
                        st.success("Hore! Kata sandi kamu berhasil diperbarui! 🔑")
