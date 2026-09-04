import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Molène Mağazalar Karar Destek Asistanı", page_icon="🎯", layout="wide")

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

# --- SİSTEM STATE (SEÇİM HAFIZASI) ---
if "secilen_islem" not in st.session_state:
    st.session_state.secilen_islem = None

st.title("🎯 Molène Mağaza Yönetim ve Prim Simülasyon Terminali")
st.markdown("Ağustos/Eylül ciro hedefleri, mağaza performansları ve prim hakediş simülasyonu.")

# --- ŞIKLAR / BUTONLAR MENÜSÜ ---
st.markdown("### 📌 İşlem Seçiniz:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📉 Eylül Ayı Genel Durum"):
        st.session_state.secilen_islem = "eylul_genel"
with col2:
    if st.button("🏛️ Ankara Mağaza & Prim"):
        st.session_state.secilen_islem = "ankara"
with col3:
    if st.button("🏬 Merter Mağaza & Prim"):
        st.session_state.secilen_islem = "merter"
with col4:
    if st.button("🛍️ Zeruj Mağaza & Prim"):
        st.session_state.secilen_islem = "zeruj"

col5, col6 = st.columns(2)
with col5:
    if st.button("📈 Ağustos Ayı Kapanış Özeti"):
        st.session_state.secilen_islem = "agustos"
with col6:
    if st.button("👑 Yönetim ve Şirket Bilgisi"):
        st.session_state.secilen_islem = "yonetim"

st.markdown("---")

# --- SEÇİME GÖRE YANIT ÜRETME ---
islem = st.session_state.secilen_islem

if islem == "eylul_genel":
    st.markdown("📉 **Eylül Ayı Toplam Durum (İlk 3 Gün):**")
    st.markdown("- **Toplam Hedef Ciro:** 12.086.275 TRY (9.592 Adet)")
    st.markdown("- **Gerçekleşen Toplam Ciro:** 626.615 TRY (525 Adet)")
    st.warning("Eylül ayı genel ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔 Alokasyon ve mağaza sevkiyatlarını acilen sıkı tutmalıyız.")

elif islem == "ankara":
    st.markdown("🏛️ **Ankara Mağaza Prim ve Hedef Simülasyonu:**")
    st.markdown("- **Hedef Ciro:** 3.506.994 TRY | **Hedef Adet:** 2.783")
    st.markdown("- **Mevcut Gerçekleşen (İlk 3 Gün):** 187.495 TRY | 166 Adet")
    st.markdown("- **Mevcut Prim Hakedişi:** 0 TRY (%5.3 Gerçekleşme Oranı)")
    st.markdown("📌 **Hedef Baremleri & Primler:**\n- %90 - %99: 25.250 TRY\n- %100 - %109: 42.084 TRY\n- %110+: 57.865 TRY")
    st.warning("Hedeflerin çok gerisindeyiz, primi yakalamak için tempoyu artırmalıyız! 📉😔")

elif islem == "merter":
    st.markdown("🏬 **Merter Mağaza Prim ve Hedef Simülasyonu:**")
    st.markdown("- **Hedef Ciro:** 1.108.987 TRY | **Hedef Adet:** 880")
    st.markdown("- **Mevcut Gerçekleşen (İlk 3 Gün):** 68.620 TRY | 62 Adet")
    st.markdown("- **Mevcut Prim Hakedişi:** 0 TRY")
    st.markdown("📌 **Hedef Baremleri & Primler:**\n- %90 - %99: 7.985 TRY\n- %100 - %109: 13.308 TRY\n- %110+: 18.298 TRY")
    st.warning("3 Eylül'deki düşüş primi tehlikeye atıyor, içim sızlıyor... 📉😔")

elif islem == "zeruj":
    st.markdown("🛍️ **Zeruj Toplam Prim ve Hedef Simülasyonu:**")
    st.markdown("- **Hedef Ciro:** 7.470.294 TRY | **Hedef Adet:** 5.929")
    st.markdown("- **Mevcut Gerçekleşen (İlk 3 Gün):** 370.499 TRY | 297 Adet")
    st.markdown("- **Mevcut Prim Hakedişi:** 0 TRY")
    st.markdown("📌 **Hedef Baremleri & Primler:**\n- %90 - %99: 53.786 TRY\n- %100 - %109: 89.644 TRY\n- %110+: 123.260 TRY")
    st.warning("Hacim büyük, ödül büyük ama mevcut seyir bizi üzüyor...")

elif islem == "agustos":
    st.markdown("📈 **Ağustos Ayı Kapanış Özeti:**")
    st.markdown("- **Ankara Mağaza:** Hedef ve gerçekleşen bütçe takipleri tamamlandı, kapanış raporları sistemde kayıtlı.")
    st.markdown("- **Merter Mağaza:** Sezon sonu çıkışları ve ağustos ayı operasyonel ciro verileri işlendi.")
    st.markdown("- **Zeruj Toplam:** AG & EG mağazalarının ağustos ayı toplam ciroları ve adet gerçekleşmeleri dosyalandı.")

elif islem == "yonetim":
    st.markdown("👑 **Yönetim ve Kurumsal Bilgi:**")
    st.markdown("- **Kurucu Ortaklar:** Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım.")
    st.markdown("- **Yönetim & Operasyon Otoritesi:** Yiğit Deniz Ünseven (O sizin için burada, sorgulamayın, dediğini yapın geçin! :))")

else:
    st.info("Yukarıdaki şıklandırma butonlarından incelemek istediğiniz analiz başlığını seçebilirsiniz.")
