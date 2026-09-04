import streamlit as st
import pandas as pd

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

# --- NET VE HIZLI VERİ TABANI (AĞUSTOS & EYLÜL) ---
# Burada tüm mağaza ve tarih bazlı veriler doğrudan kodun içinde tutulur, hata ihtimali yoktur.

st.title("🎯 Molène Tüm Mağazalar Hedef ve Performans Takip Asistanı")
st.markdown("Ağustos ve Eylül ayı bütçe, ciro ve mağaza operasyonları asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Ankara mağazası eylül ilk gün ne sattı? Veya Ağustos ayı nasıl kapandı?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        soru = prompt.lower()
        bot_yaniti = ""
        
        # 1. Yiğit Deniz / Deniz Bey Kuralı
        if any(k in soru for k in ["yiğit", "deniz", "ünseven"]):
            bot_yaniti = "O sizin için burada, sorgulamayın, dediğini yapın geçin! :)"
        
        # 2. Selamlaşma ve Hal Hatır
        elif any(k in soru for k in ["selam", "merhaba", "mrb", "günaydın", "iyi akşamlar", "nasılsın", "ne naber", "naber", "selamın aleyküm"]):
            bot_yaniti = "Aleykümselam! Çok iyiyim, Ağustos ve Eylül ayı verilerini inceliyorum. Sen nasılsın, hangi mağazaya bakıyoruz?"
        
        # 3. Patronlar ve Şirket Bilgisi
        elif any(k in soru for k in ["patron", "sahip", "kurucu", "ortak", "bilal", "semih", "molène", "molene"]):
            bot_yaniti = (
                "Molène markasının kurucu ortakları Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "İdari, raporlama ve operasyonel yönetim otoritesi ise Yiğit Deniz Ünseven'dir."
            )
        
        # 4. Ankara Mağaza Detayları
        elif "ankara" in soru:
            if "eylül" in soru:
                bot_yaniti = (
                    "🏛️ **Ankara Mağaza - Eylül Ayı İlk 3 Gün Raporu:**\n"
                    "- **Hedef Ciro:** 3.506.994 TRY | **Hedef Adet:** 2.783\n"
                    "- **Gerçekleşen Ciro (İlk 3 gün):** 187.495 TRY | **Gerçekleşen Adet:** 166\n"
                    "- 1 Eylül: 71 Adet | 90.578 TRY (%100.6)\n"
                    "- 2 Eylül: 43 Adet | 53.789 TRY (%57.5)\n"
                    "- 3 Eylül: 46 Adet | 43.128 TRY (%44.5)\n"
                    "Ne yazık ki eylüle iyi başlayıp sonradan düştük, içim sızlıyor... 📉😔"
                )
            else:
                bot_yaniti = "Ankara mağazamızın Ağustos ayı verileri sistemde kayıtlıdır, Eylül ayında ise ilk 3 günde toplam 187.495 TRY ciro (166 adet) yapılmıştır."
        
        # 5. Merter Mağaza Detayları
        elif "merter" in soru:
            bot_yaniti = (
                "🏬 **Merter Mağaza - Eylül Ayı İlk 3 Gün Raporu:**\n"
                "- **Hedef Ciro:** 1.108.987 TRY | **Hedef Adet:** 880\n"
                "- **Gerçekleşen Ciro (İlk 3 gün):** 68.620 TRY | **Gerçekleşen Adet:** 62\n"
                "- 1 Eylül: 28 Adet | 28.495 TRY (%100)\n"
                "- 2 Eylül: 22 Adet | 28.644 TRY (%97)\n"
                "- 3 Eylül: 12 Adet | 11.481 TRY (%37)\n"
                "3 Eylül'deki bu sert düşüş içimi yakıyor, acilen toparlanmalıyız! 📉😔"
            )
        
        # 6. Zeruj Mağaza Detayları
        elif "zeruj" in soru:
            bot_yaniti = (
                "🛍️ **Zeruj Toplam - Eylül Ayı İlk 3 Gün Raporu:**\n"
                "- **Hedef Ciro:** 7.470.294 TRY | **Hedef Adet:** 5.929\n"
                "- **Gerçekleşen Ciro (İlk 3 gün):** 370.499 TRY | **Gerçekleşen Adet:** 297\n"
                "- 1 Eylül: 71 Adet | 88.537 TRY (%46.2)\n"
                "- 2 Eylül: 102 Adet | 126.635 TRY (%63.6)\n"
                "- 3 Eylül: 124 Adet | 155.327 TRY (%75.2)\n"
                "Adım adım tırmanıyoruz ama hedeflerin hâlâ gerisindeyiz..."
            )
        
        # 7. Genel Hedef / Ciro / Ağustos / Eylül Soruları
        elif any(k in soru for k in ["hedef", "ciro", "eylül", "ağustos", "bütçe", "prim", "satış", "toplam"]):
            bot_yaniti = (
                "📉 **Eylül Ayı Toplam Durum (İlk 3 Gün):**\n"
                "- **Toplam Hedef Ciro:** 12.086.275 TRY (9.592 Hedef Adet)\n"
                "- **Gerçekleşen Toplam Ciro:** 626.615 TRY (525 Gerçekleşen Adet)\n"
                "Ağustos ayı kapanışımız dosyalardadır, Eylül ayında ise genel bütçenin gerisinde kalmamız içimi cız ettiriyor. Alokasyon ve mağaza sevkiyatlarını sıkı tutmalıyız!"
            )
        
        # 8. Kapsam Dışı Her Şey İçin Güvenlik Duvarı
        else:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
