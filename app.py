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

# --- YAPAY ZEKA ÇEKİRDEĞİ ---
# Güvenli dahili anahtar yapılandırması
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    pass

st.title("🎯 Molène Tüm Mağazalar Hedef ve Performans Takip Asistanı")
st.markdown("Mağaza ciro hedefleri, Ağustos/Eylül performansları ve operasyon asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Eylül ayı Ankara mağazası durumu nedir? Veya Yiğit Deniz Ünseven kimdir?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        soru_kucuk = prompt.lower()
        bot_yaniti = ""

        # 1. KATI KURALLAR (Yiğit Deniz ve Güvenlik Duvarı)
        if any(k in soru_kucuk for k in ["yiğit", "deniz", "ünseven"]):
            bot_yaniti = "O sizin için burada, sorgulamayın, dediğini yapın geçin! :)"
        
        # 2. SELAMLAMA
        elif any(k in soru_kucuk for k in ["selam", "merhaba", "mrb", "günaydın", "iyi akşamlar", "nasılsın", "ne naber", "naber"]):
            bot_yaniti = "Aleykümselam! Çok iyiyim, Molène verilerini ve mağaza hedeflerini inceliyorum. Sen nasılsın, hangi veriye bakıyoruz?"
        
        # 3. PATRONLAR VE ŞİRKET BİLGİSİ
        elif any(k in soru_kucuk for k in ["patron", "sahip", "kurucu", "ortak", "bilal", "semih", "molène", "molene"]):
            bot_yaniti = (
                "Molène markasının kurucu ortakları Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "İdari, raporlama ve operasyonel yönetim otoritesi ise Yiğit Deniz Ünseven'dir."
            )
        
        # 4. MAĞAZALAR VE CİRO / HEDEF VERİLERİ (Ağustos & Eylül)
        elif any(k in soru_kucuk for k in ["hedef", "ciro", "eylül", "ağustos", "bütçe", "prim", "satış", "ankara", "merter", "zeruj", "mağaza", "adet"]):
            bot_yaniti = (
                "📉 **Ağustos & Eylül Dönemi Mağaza Performans Özeti:**\n\n"
                "• **Ağustos Ayı:** Verilerimiz sistemde kayıtlı olup aylık kapanış analizleri tamamlanmıştır.\n"
                "• **Eylül Ayı İlk 3 Gün Durumu:** Ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔\n"
                "  - **Toplam Hedef:** 12.086.275 TRY (9.592 Adet) | **Gerçekleşen:** 626.615 TRY (525 Adet)\n"
                "  - **Ankara Mağaza:** Hedef 3.506.994 TRY | İlk 3 gün gerçekleşen toplam 187.495 TRY (166 Adet)\n"
                "  - **Merter Mağaza:** Hedef 1.108.987 TRY | İlk 3 gün gerçekleşen toplam 68.620 TRY (62 Adet)\n"
                "  - **Zeruj Toplam:** Hedef 7.470.294 TRY | İlk 3 gün gerçekleşen toplam 370.499 TRY (297 Adet)\n\n"
                "Hedefleri yakalamak için alokasyon ve sevkiyat stratejilerini acilen sıkı tutmalıyız!"
            )
        
        # 5. KAPSAM DIŞI HER ŞEY İÇİN KATI DUVAR (Sadece istenenler konuşulur)
        else:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
