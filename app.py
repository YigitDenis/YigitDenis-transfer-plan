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

# --- NET VE ODAKLI KURUMSAL MOTOR ---

st.title("🎯 Molène Tüm Mağazalar Hedef ve Performans Takip Asistanı")
st.markdown("Tüm mağazalar, bütçe takipleri, ciro hedefleri ve perakende operasyonları asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Eylül ayı hedefleri nasıl? Veya Yiğit Deniz Ünseven kimdir?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        soru = prompt.lower()
        
        # 1. Yiğit Deniz / Deniz Bey Kuralı
        if any(k in soru for k in ["yiğit", "deniz", "ünseven"]):
            bot_yaniti = "O sizin için burada, sorgulamayın, dediğini yapın geçin! :)"
        
        # 2. Selamlaşma, Hal Hatır ve Naber
        elif any(k in soru for k in ["selam", "merhaba", "mrb", "günaydın", "iyi akşamlar", "nasılsın", "ne naber", "naber", "selamın aleyküm"]):
            bot_yaniti = "Aleykümselam! Çok iyiyim, Molène verileriyle çalışmaya devam ediyorum. Sen nasılsın, hangi mağazanın hedeflerine bakıyoruz?"
        
        # 3. Patronlar ve Şirket Bilgisi
        elif any(k in soru for k in ["patron", "sahip", "kurucu", "ortak", "bilal", "semih", "molène", "molene"]):
            bot_yaniti = (
                "Molène markasının kurucu ortakları Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "İdari ve operasyonel süreçlerin merkezi ise Yiğit Deniz Ünseven'dir."
            )
        
        # 4. Mağazalar, Hedefler ve Ciro Verileri (Eylül Ayı İlk 3 Gün Özeti)
        elif any(k in soru for k in ["hedef", "ciro", "eylül", "bütçe", "prim", "satış", "ankara", "merter", "zeruj", "mağaza"]):
            bot_yaniti = (
                "Eylül ayı genel ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔\n\n"
                "📊 **Eylül Ayı İlk 3 Gün Özeti:**\n"
                "- **Toplam Hedef Ciro:** 12.086.275 TRY | **Gerçekleşen:** 626.615 TRY\n"
                "- **Ankara Mağaza:** Hedef 3.506.994 TRY | İlk 3 gün toplam: 187.495 TRY (%100.6, %57.5, %44.5)\n"
                "- **Merter Mağaza:** Hedef 1.108.987 TRY | İlk 3 gün toplam: 68.620 TRY (%100, %97, %37)\n"
                "- **Zeruj Toplam:** Hedef 7.470.294 TRY | İlk 3 gün toplam: 370.499 TRY (%46.2, %63.6, %75.2)"
            )
        
        # 5. Kapsam Dışı Her Şey İçin Güvenlik Duvarı
        else:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
