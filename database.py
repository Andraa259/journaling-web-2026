import streamlit as st
from supabase import create_client, Client

# Inisialisasi klien Supabase menggunakan secrets
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def login_user(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return res.user
    except Exception as e:
        st.error(f"⚠️ Gagal Masuk: {e}")
        return None

def change_password(new_password):
    try:
        # Fungsi bawaan Supabase untuk memperbarui data user yang sedang login
        supabase.auth.update_user({"password": new_password})
        return True
    except Exception as e:
        st.error(f"⚠️ Gagal mengubah kata sandi: {e}")
        return False

def logout_user():
    supabase.auth.sign_out()

def get_all_journals():
    response = supabase.table("journals").select("*").order("created_at", desc=True).execute()
    return response.data

def insert_journal(user_id, user_email, title, content):
    data = {
        "user_id": user_id,
        "user_email": user_email,
        "title": title,
        "content": content
    }
    response = supabase.table("journals").insert(data).execute()
    return response.data
