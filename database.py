import streamlit as st
from supabase import create_client, Client

url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def login_user_flexible(identifier, password):
    try:
        # Jika input tidak mengandung '@', kita asumsikan itu adalah username
        if "@" not in identifier:
            # Cari email asli di tabel profiles berdasarkan username
            profile_res = supabase.table("profiles").select("email").eq("username", identifier).single().execute()
            if profile_res.data:
                email_to_use = profile_res.data["email"]
            else:
                st.error("⚠️ Username tidak ditemukan!")
                return None
        else:
            email_to_use = identifier

        # Eksekusi login resmi menggunakan email ke Supabase Auth
        res = supabase.auth.sign_in_with_password({"email": email_to_use, "password": password})
        return res.user
    except Exception as e:
        st.error(f"⚠️ Gagal Masuk: {e}")
        return None

def get_user_profile(user_id):
    res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    return res.data

def update_user_profile_data(user_id, nickname, username, avatar_url):
    try:
        data = {"nickname": nickname, "username": username, "avatar_url": avatar_url}
        res = supabase.table("profiles").update(data).eq("id", user_id).execute()
        return True
    except Exception as e:
        st.error(f"⚠️ Gagal memperbarui profil: {e}")
        return False

def get_all_journals_with_profiles():
    # Menarik data jurnal beserta informasi profil penulisnya (nickname & avatar)
    res = supabase.table("journals").select("*, profiles(nickname, avatar_url)").order("created_at", desc=True).execute()
    return res.data

def insert_journal(user_id, title, content):
    data = {"user_id": user_id, "title": title, "content": content}
    res = supabase.table("journals").insert(data).execute()
    return res.data

def change_password(new_password):
    try:
        supabase.auth.update_user({"password": new_password})
        return True
    except Exception as e:
        st.error(f"⚠️ Gagal mengubah kata sandi: {e}")
        return False

def logout_user():
    supabase.auth.sign_out()
