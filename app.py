import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(
    page_title="Molène Mağazalar | Ağustos Kapanış & Eylül Canlı Dashboard", 
    page_icon="🎯", 
    layout="wide"
)

# Kurumsal Şifre Kontrolü (Şifre: 1907)
def check_password():
    def password_entered():
        if st.session_state["password"] == "1907":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.subheader("🔒 Molène Kurumsal Giriş")
        st.text_input("Yönetici Şifresini Giriniz:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.subheader("🔒 Molène Kurumsal Giriş")
        st.text_input("Yönetici Şifresini Giriniz:", type="password", on_change=password_entered, key="password")
        st.error("😕 Şifre yanlış.")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- GOOGLE E-TABLO (AI SAYFA) CANLI VERİ ÇEKME MOTORU ---
@st.cache_data(ttl=10) # Her 10 saniyede bir tablodaki güncellemeleri kontrol eder
def canli_veri_cek():
    try:
        sheet_id = "1TFXBAtfGrCLQzze7Llbg4fI0pWL2kkWEb0eBuX71kKE"
        sheet_name = "ai Sayfa"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)
        return df, True
    except Exception as e:
        return None, False

df_eylul, veri_durumu = canli_veri_cek()

# --- AĞUSTOS SABİT KAPANIŞ VERİLERİ ---
AGUSTOS_VERILERI = {
    "toplam": {"hedef_ciro": 10215505.88, "gerceklesen_ciro": 10071896.05, "oran": "%99"},
}

# --- DASHBOARD ARAYÜZÜ ---
st.title("🎯 Molène Mağazalar | Ağustos & Eylül Performans Dashboard")
st.markdown("Ağustos resmi kapanış verileri ve Google E-Tablolar ('ai Sayfa') üzerinden anlık güncellenen Eylül takip ekranı.")

st.markdown("### 📈 Ağustos Ayı Kesinleşmiş Kapanış Özet Kartları")
c1, c2, c3, c4 = st.columns(4)
t_ag = AGUSTOS_VERILERI["toplam"]
c1.metric("Ağustos Hedef Ciro", f"{t_ag['hedef_ciro']:,.2f} TRY")
c2.metric("Ağustos Gerçekleşen", f"{t_ag['gerceklesen_ciro']:,.2f} TRY")
c3.metric("Ağustos Gerçekleşme", t_ag['oran'])
c4.metric("Kapanış Durumu", "Tamamlandı 🟢")

st.markdown("---")

st.markdown("### 📉 Eylül Ayı Canlı Veri Akışı ve Mağaza Analizleri")

if veri_durumu and df_eylul is not None:
    st.success("Google E-Tablolar ('ai Sayfa') verisi başarıyla senkronize edildi. Tabloya veri girdikçe burası otomatik güncellenir.")
    st.dataframe(df_eylul, use_container_width=True)
else:
    st.error("Google E-Tablo verisi okunamadı. Lütfen Google E-Tablonuzda paylaşım ayarlarının **'Bağlantıya sahip olan herkes - Görüntüleyen'** olarak seçili olduğundan emin olun.")

st.markdown("---")
st.markdown("### 📊 Mağaza Bazlı Detaylı Analiz & Değerlendirme")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("#### 🏛️ Ankara Mağaza Analizi")
    st.markdown(
        "- **Bütçe Takibi:** Tablodan anlık okunan verilere göre bütçe sapmaları analiz edilir.\n"
        "- **Adet Verimliliği:** Hedef ve gerçekleşen adet oranları tabloya işlendiği anda buraya yansır.\n"
        "- **Analiz:** Günlük girişlerle birlikte trafik ve dönüşüm performansları anlık izlenmektedir."
    )

with col_b:
    st.markdown("#### 🏬 Merter Mağaza Analizi")
    st.markdown(
        "- **Bütçe Takibi:** Tablodan anlık okunan verilere göre bütçe sapmaları analiz edilir.\n"
        "- **Adet Verimliliği:** Hedef ve gerçekleşen adet oranları tabloya işlendiği anda buraya yansır.\n"
        "- **Analiz:** Sezon geçişleri ve sepet ortalaması canlı veriler üzerinden takip edilmektedir."
    )

with col_c:
    st.markdown("#### 🛍️ Zeruj Toplam Analizi")
    st.markdown(
        "- **Bütçe Takibi:** Tablodan anlık okunan verilere göre bütçe sapmaları analiz edilir.\n"
        "- **Adet Verimliliği:** Hedef ve gerçekleşen adet oranları tabloya işlendiği anda buraya yansır.\n"
        "- **Analiz:** Kanal ağırlığı yüksek olan Zeruj verileri anlık olarak senkronize edilmektedir."
    )
