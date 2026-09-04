import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Molène Mağazalar AI Asistanı", page_icon="🎯", layout="wide")

# Şifre Kontrolü (Şifre: 1907)
def check_password():
    def password_entered():
        if st.session_state["password"] == "1907":
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

# Standart API Anahtar Yapılandırması
GOOGLE_API_KEY = "AIzaSy..." # Kendi geçerli AI Studio API anahtarını buraya yazabilirsin
genai.configure(api_key=GOOGLE_API_KEY)

st.title("🎯 Molène Tüm Mağazalar Hedef ve Performans Takip Asistanı")
st.markdown("Tüm mağazalar, bütçe takipleri, ciro hedefleri ve perakende operasyonları asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Mağazaların genel hedef durumu nedir? Veya Yiğit Deniz kimdir?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Tüm mağaza verileri ve perakende dinamikleri analiz ediliyor..."):
            try:
                # TÜM MAĞAZALAR GENEL HEDEF VE PERFORMANS HAFIZASI
                system_prompt = (
                    "Sen Molène Mağazalar AI Asistanısın. "
                    "Tüm mağazaların (Ankara, Merter, Zeruj Port AG & EG ve E-ticaret) genel hedef ve performans takip sistemisin. "
                    "Mevcut verilerimizde genel ciro ve hedefler geride kaldığı için, hedeflerin altında olunan durumlarda yanıtlarında hafif bir üzüntü, hüzün ve iç sızlatan bir ton ver. "
                    "ÖZEL KURALLAR:\n"
                    "1. Eğer kullanıcı Yiğit Bey, Deniz Bey veya Yiğit Deniz Ünseven hakkında soru sorarsa, kesinlikle şu yanıtı ver: 'O sizin için burada, sorgulamayın, dediğini yapın geçin! :)'\n"
                    "2. Eğer şirket dışı, bilinmeyen veya yetki alanı dışı bir konu sorulursa gülerek şu yanıtı ver: 'Bu konu hakkında bilgi vermem, Deniz bey kızar :)'\n"
                    "3. Mağazacılık, raf düzeni, depo alokasyonu, satış arttırma, müşteri ilişkileri, primler ve tüm mağaza operasyonlarıyla ilgili her soruyu profesyonel ve analitik bir dille yanıtla.\n\n"
                    f"Kullanıcının Sorusu: {prompt}"
                )
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(system_prompt)
                
                bot_yaniti = response.text
                st.markdown(bot_yaniti)
                st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
                
            except Exception as e:
                hata_mesaji = f"Bir hata oluştu: {str(e)}"
                st.error(hata_mesaji)
