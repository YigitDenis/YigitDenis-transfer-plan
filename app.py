import streamlit as st
import pandas as pd
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Perakende AI Asistanı", page_icon="📊", layout="wide")

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

# Gemini API Yapılandırması
GOOGLE_API_KEY = "AQ.Ab8RN6IrttZSm48twAcllBpiho2z5amf3tJLmmPvyns8Wcl8yQ"
genai.configure(api_key=GOOGLE_API_KEY)

# Google Sheets Verisini Çekme Fonksiyonu
@st.cache_data(ttl=600)
def veriyi_cek():
    sheet_id = "1OKtv3r83TvYGVpwp06q3MbxeS-liHtZX4JuoVSE7qAo"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    df = pd.read_csv(url)
    return df

# Arayüz Tasarımı
st.title("🛍️ Molène Perakende & Alokasyon Asistanı")
st.markdown("Günlük satış, stok ve kanal verileriniz üzerinden yapay zekaya sorular sorun.")

# Veriyi Yükleme
try:
    df = veriyi_cek()
    st.sidebar.success(f"✅ Veri Başarıyla Yüklendi! ({len(df)} satır)")
    
    if st.sidebar.checkbox("Ham Veriyi Göster"):
        st.dataframe(df.head(50))
        
except Exception as e:
    st.error(f"Veri okunurken hata oluştu: {e}")
    st.stop()

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan Soru Alma
if prompt := st.chat_input("Örn: Hangi ürünün stoğu az kalmış?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Veriler analiz ediliyor..."):
            try:
                headers = " | ".join(df.columns.tolist())
                rows = df.head(200).to_string(index=False)
                
                system_prompt = (
                    "Sen kıdemli bir perakende planlama ve alokasyon yöneticisisin. "
                    "Sana verilen Google E-Tablo verilerini analiz ederek net, kısa, profesyonel ve çözüm odaklı yanıtlar ver. "
                    "Asla varsayımda bulunma, doğrudan tablo verilerine dayanarak cevapla.\n\n"
                    f"Tablo Sütunları:\n{headers}\n\nVeri Örneği:\n{rows}\n\nSoru: {prompt}"
                )
                
                # Güncel Gemini model çağrısı
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(system_prompt)
                
                bot_yaniti = response.text
                st.markdown(bot_yaniti)
                st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
                
            except Exception as e:
                hata_mesaji = f"Bir hata oluştu: {str(e)}"
                st.error(hata_mesaji)
