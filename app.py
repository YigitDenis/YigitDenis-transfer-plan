import streamlit as st

# Sayfa Ayarları
st.set_page_config(
    page_title="Molène Mağazalar | Ağustos & Eylül KPI Dashboard", 
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

# --- VERİ TABANI ---
AGUSTOS_VERILERI = {
    "toplam": {"hedef_ciro": 10215505.88, "gerceklesen_ciro": 10071896.05, "oran": "%99"},
    "ankara": {"hedef_ciro": 2760000.00, "gerceklesen_ciro": 2922495.00, "oran": "%108"},
    "merter": {"hedef_ciro": 884006.00, "gerceklesen_ciro": 924156.00, "oran": "%105"},
    "zeruj_ag": {"hedef_ciro": 4401000.00, "gerceklesen_ciro": 4322265.00, "oran": "%98"},
    "zeruj_eg": {"hedef_ciro": 2170500.00, "gerceklesen_ciro": 1902980.00, "oran": "%88"}
}

EYLUL_VERILERI = {
    "toplam": {"hedef_ciro": 12086275.00, "gerceklesen_ciro": 626615.00, "hedef_adet": 9592, "gerceklesen_adet": 525, "oran": "%5.2"}
}

# --- DASHBOARD ARAYÜZÜ ---
st.title("🎯 Molène Mağazalar | Ağustos & Eylül Performans Dashboard")
st.markdown("Ağustos resmi kapanış verileri ve Eylül ayı performans takip ekranı.")

st.markdown("### 📈 Ağustos Ayı Kesinleşmiş Kapanış Özet Kartları")
c1, c2, c3, c4 = st.columns(4)
t_ag = AGUSTOS_VERILERI["toplam"]
c1.metric("Ağustos Hedef Ciro", f"{t_ag['hedef_ciro']:,.2f} TRY")
c2.metric("Ağustos Gerçekleşen", f"{t_ag['gerceklesen_ciro']:,.2f} TRY")
c3.metric("Ağustos Gerçekleşme", t_ag['oran'])
c4.metric("Kapanış Durumu", "Tamamlandı 🟢")

st.markdown("---")

st.markdown("### 📉 Eylül Ayı Performans Özeti")
e1, e2, e3, e4 = st.columns(4)
t_ey = EYLUL_VERILERI["toplam"]
e1.metric("Eylül Hedef Ciro", f"{t_ey['hedef_ciro']:,.2f} TRY")
e2.metric("Eylül Gerçekleşen", f"{t_ey['gerceklesen_ciro']:,.2f} TRY")
e3.metric("Hedef / Gerç. Adet", f"{t_ey['hedef_adet']} / {t_ey['gerceklesen_adet']}")
e4.metric("Eylül Gerçekleşme", t_ey['oran'])

st.markdown("### 📌 Mağaza Bazlı Eylül Tablosu")
eylül_tablo = [
    {"Mağaza": "Ankara", "Hedef Ciro": "3.506.994 TRY", "Gerçekleşen Ciro": "187.495 TRY", "Hedef Adet": 2783, "Gerç. Adet": 166, "Durum": "Kritik 🔴"},
    {"Mağaza": "Merter", "Hedef Ciro": "1.108.987 TRY", "Gerçekleşen Ciro": "68.620 TRY", "Hedef Adet": 880, "Gerç. Adet": 62, "Durum": "Kritik 🔴"},
    {"Mağaza": "Zeruj Toplam", "Hedef Ciro": "7.470.294 TRY", "Gerçekleşen Ciro": "370.499 TRY", "Hedef Adet": 5929, "Gerç. Adet": 297, "Durum": "Kritik 🔴"},
]
st.table(eylül_tablo)
