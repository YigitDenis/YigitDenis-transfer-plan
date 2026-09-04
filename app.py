import streamlit as st

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
        # API bağlantısı bekletmeden anında yanıt üretme mantığı
        soru_kucuk = prompt.lower()
        
        if "yiğit" in soru_kucuk or "deniz" in soru_kucuk:
            bot_yaniti = "O sizin için burada, sorgulamayın, dediğini yapın geçin! :)"
        elif any(kelime in soru_kucuk forkelime in ["hedef", "ciro", "eylül", "ankara", "merter", "zeruj"]):
            bot_yaniti = (
                "Eylül ayı genel ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔 "
                "Ankara, Merter ve Zeruj mağazalarımızda ilk günlerdeki dalgalanmaları toparlamak için alokasyon ve satış stratejilerini acilen gözden geçirmeliyiz."
            )
        elif any(kelime in soru_kucuk for kelime in ["raf", "depo", "alokasyon", "müşteri", "satış", "prim"]):
            bot_yaniti = (
                "Perakende operasyonlarında kritik kuralımız nettir: Doğru ürünü doğru mağazaya zamanında sevk etmek. "
                "Haftada 3 gün mağaza sevkiyatlarımızı ve günlük e-ticaret akışımızı Nebim V3 ve Iontegra WMS üzerinden sıkı takip ediyoruz. "
                "Personel motivasyonu ve prim hakedişleri için hedef baremlerine odaklanmalıyız."
            )
        else:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
