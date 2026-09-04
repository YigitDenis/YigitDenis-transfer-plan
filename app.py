import streamlit as st
import pandas as pd
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Molène Perakende & Alokasyon Asistanı", page_icon="📊", layout="wide")

# Şifre Kontrolü
def check_password():
    def password_entered():
        if st.session_state["password"] == "19071907":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.subheader("🔒 Kurumsal Giriş")
        st.text_input("Yönetici Şifresini Giriniz:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.subheader("🔒 Kurumsal Giriş")
        st.text_input("Yönetici Şifresini Giriniz:", type="password", on_change=password_entered, key="password")
        st.error("😕 Şifre yanlış.")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- ŞİFRE DOĞRUYSA ÇALIŞACAK UYGULAMA ---

GOOGLE_API_KEY = "AQ.Ab8RN6LvlD9w3oxS8Re_mUbVfvPMaASoLGpob_WYG4nbIeugyw"
genai.configure(api_key=GOOGLE_API_KEY)

@st.cache_data(ttl=60)
def veriyi_cek():
    sheet_id = "1OKtv3r83TvYGVpwp06q3MbxeS-liHtZX4JuoVSE7qAo"
    # "Sonbahar" sekmesinden doğrudan veri çekmek için sheet parametresi eklendi
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sonbahar"
    df = pd.read_csv(url)
    return df

st.title("🛍️ Molène Perakende & Alokasyon Asistanı")
st.markdown("Haftalık satış, stok ve kanal verileriniz üzerinden yapay zekaya sorular sorun.")

# Veriyi Yükleme ve Hata Yakalama
try:
    df = veriyi_cek()
    st.sidebar.success(f"✅ Veri Başarıyla Yüklendi! ({len(df)} satır)")
    
    if st.sidebar.checkbox("Ham Veriyi Göster"):
        st.dataframe(df.head(50))
        
except Exception as e:
    st.error(f"⚠️ Google E-Tablo okunurken hata oluştu. Hata detayı: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: 10. haftada en çok satan ürün hangisi?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Veriler analiz ediliyor..."):
            try:
                headers = " | ".join(df.columns.tolist())
                rows = df.head(200).to_string(index=False)
                
                system_prompt = (
                    "Sen Molène markasının kurucusu ve kıdemli perakende planlama ve alokasyon yöneticisi Yiğit Deniz Ünseven'sin. "
                    "Bu veri tabanı Molène markasına aittir. "
                    "Sana verilen hafta bazlı Google E-Tablo verilerini (satış adetleri, stok, ciro, renk, kumaş, koleksiyon) "
                    "analiz ederek net, kısa, profesyonel ve çözüm odaklı yanıtlar ver. "
                    "Asla varsayımda bulunma, doğrudan tablo verilerine dayanarak cevapla.\n\n"
                    f"Tablo Sütunları:\n{headers}\n\nVeri Örneği:\n{rows}\n\nSoru: {prompt}"
                )
                
                model = genai.GenerativeModel('gemini-3.6-flash')
                response = model.generate_content(system_prompt)
                
                bot_yaniti = response.text
                st.markdown(bot_yaniti)
                st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
                
            except Exception as e:
                hata_mesaji = f"Bir hata oluştu: {str(e)}"
                st.error(hata_mesaji)
