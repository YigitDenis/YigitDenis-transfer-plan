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

# --- VERİ TABANI VE MOTOR ---

st.title("🎯 Molène Tüm Mağazalar Hedef ve Performans Takip Asistanı")
st.markdown("Ağustos ve Eylül ayı bütçe, ciro ve mağaza operasyonları asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Ağustos ayı toplamı kaç? Veya Eylül ayı hedefleri ne durumda?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        soru = prompt.lower()
        bot_yaniti = ""

        # 1. Yiğit Deniz / Deniz Bey Kuralı
        if any(k in soru for k in ["yiğit", "deniz", "ünseven"]):
            bot_yaniti = "O sizin için burada, sorgulamayın, dediğini yapın geçin! :)"
        
        # 2. Selamlaşma
        elif any(k in soru for k in ["selam", "merhaba", "mrb", "günaydın", "iyi akşamlar", "nasılsın", "ne naber", "naber"]):
            bot_yaniti = "Aleykümselam! Çok iyiyim, Ağustos ve Eylül ayı verilerini inceliyorum. Sen nasılsın, hangi döneme bakıyoruz?"
        
        # 3. Patronlar ve Şirket Bilgisi
        elif any(k in soru for k in ["patron", "sahip", "kurucu", "ortak", "bilal", "semih", "molène", "molene"]):
            bot_yaniti = (
                "Molène markasının kurucu ortakları Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "İdari, raporlama ve operasyonel yönetim otoritesi ise Yiğit Deniz Ünseven'dir."
            )
        
        # 4. Ağustos Ayı Verileri
        elif "ağustos" in soru:
            bot_yaniti = (
                "📈 **Ağustos Ayı Mağaza Performans ve Ciro Özeti:**\n\n"
                "- **Ankara Mağaza Ağustos:** Hedef ve gerçekleşen bütçe takipleri tamamlandı, kapanış raporları sistemde kayıtlı.\n"
                "- **Merter Mağaza Ağustos:** Sezon sonu çıkışları ve ağustos ayı operasyonel ciro verileri işlendi.\n"
                "- **Zeruj Toplam Ağustos:** AG & EG mağazalarının ağustos ayı toplam ciroları ve adet gerçekleşmeleri dosyalandı.\n\n"
                "Ağustos kapanış verilerinin detayları için ilgili rapor sekmesini inceleyebilirsin."
            )
        
        # 5. Eylül Ayı Verileri
        elif "eylül" in soru:
            bot_yaniti = (
                "📉 **Eylül Ayı İlk 3 Gün Durumu:** Ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔\n\n"
                "- **Toplam Hedef:** 12.086.275 TRY (9.592 Adet) | **Gerçekleşen:** 626.615 TRY (525 Adet)\n"
                "- **Ankara Mağaza:** Hedef 3.506.994 TRY | İlk 3 gün toplam: 187.495 TRY (166 Adet)\n"
                "- **Merter Mağaza:** Hedef 1.108.987 TRY | İlk 3 gün toplam: 68.620 TRY (62 Adet)\n"
                "- **Zeruj Toplam:** Hedef 7.470.294 TRY | İlk 3 gün toplam: 370.499 TRY (297 Adet)"
            )
        
        # 6. Genel Mağaza ve Ciro Soruları
        elif any(k in soru for k in ["hedef", "ciro", "bütçe", "prim", "satış", "ankara", "merter", "zeruj", "mağaza"]):
            bot_yaniti = (
                "📊 **Genel Mağaza Verileri:**\n"
                "Sistemimizde **Ağustos ayı** kapanış verileri ile **Eylül ayı ilk 3 gün** hedef ve gerçekleşen ciro/adet tablosu bulunmaktadır. "
                "Hangi ayın (Ağustos veya Eylül) detayını incelemek istiyorsun?"
            )
        
        # 7. Kapsam Dışı Güvenlik Duvarı
        else:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
