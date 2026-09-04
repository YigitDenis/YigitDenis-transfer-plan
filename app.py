import streamlit as st
import datetime

# Sayfa Ayarları
st.set_page_config(
    page_title="Molène Mağazalar | Yönetim Paneli & Dashboard", 
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

# --- AĞUSTOS SABİT VERİLERİ ---
AGUSTOS_VERILERI = {
    "toplam": {"hedef_ciro": 10215505.88, "gerceklesen_ciro": 10071896.05, "oran": "%99"},
}

# --- EYLÜL VERİLERİ İÇİN STATE (HAFIZA) YÖNETİMİ ---
if "veri_tarihi" not in st.session_state:
    st.session_state.veri_tarihi = datetime.date(2026, 9, 4)
if "eylul_ankara_ciro" not in st.session_state:
    st.session_state.eylul_ankara_ciro = 187495.0
    st.session_state.eylul_ankara_adet = 166
    st.session_state.eylul_merter_ciro = 68620.0
    st.session_state.eylul_merter_adet = 62
    st.session_state.eylul_zeruj_ciro = 370499.0
    st.session_state.eylul_zeruj_adet = 297

# --- YAN MENÜ: VERİ GİRİŞ VE DÜZENLEME PANELİ ---
st.sidebar.header("⚙️ Eylül Veri Giriş Paneli")
st.sidebar.markdown("Yanlış veri girersen kutucukları düzeltip tekrar güncelle diyebilir veya sıfırlayabilirsin.")

with st.sidebar.form("veri_formu"):
    secilen_tarih = st.date_input("Veri Tarihi", value=st.session_state.veri_tarihi)
    
    st.subheader("🏛️ Ankara Mağaza")
    ankara_c = st.number_input("Ankara Ciro (TRY)", value=st.session_state.eylul_ankara_ciro)
    ankara_a = st.number_input("Ankara Adet", value=st.session_state.eylul_ankara_adet, step=1)
    
    st.subheader("🏬 Merter Mağaza")
    merter_c = st.number_input("Merter Ciro (TRY)", value=st.session_state.eylul_merter_ciro)
    merter_a = st.number_input("Merter Adet", value=st.session_state.eylul_merter_adet, step=1)
    
    st.subheader("🛍️ Zeruj Mağaza")
    zeruj_c = st.number_input("Zeruj Ciro (TRY)", value=st.session_state.eylul_zeruj_ciro)
    zeruj_a = st.number_input("Zeruj Adet", value=st.session_state.eylul_zeruj_adet, step=1)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        submit_btn = st.form_submit_button("🔄 Güncelle")
    with col_f2:
        reset_btn = st.form_submit_button("🗑️ Sıfırla")
    
    if submit_btn:
        st.session_state.veri_tarihi = secilen_tarih
        st.session_state.eylul_ankara_ciro = ankara_c
        st.session_state.eylul_ankara_adet = ankara_a
        st.session_state.eylul_merter_ciro = merter_c
        st.session_state.eylul_merter_adet = merter_a
        st.session_state.eylul_zeruj_ciro = zeruj_c
        st.session_state.eylul_zeruj_adet = zeruj_a
        st.success("Veriler güncellendi!")

    if reset_btn:
        st.session_state.eylul_ankara_ciro = 0.0
        st.session_state.eylul_ankara_adet = 0
        st.session_state.eylul_merter_ciro = 0.0
        st.session_state.eylul_merter_adet = 0
        st.session_state.eylul_zeruj_ciro = 0.0
        st.session_state.eylul_zeruj_adet = 0
        st.warning("Veriler sıfırlandı!")

# --- HESAPLAMALAR ---
hedef_ankara, hedef_merter, hedef_zeruj = 3506994.0, 1108987.0, 7470294.0
hedef_toplam_ciro = hedef_ankara + hedef_merter + hedef_zeruj
hedef_toplam_adet = 2783 + 880 + 5929

gerc_toplam_ciro = st.session_state.eylul_ankara_ciro + st.session_state.eylul_merter_ciro + st.session_state.eylul_zeruj_ciro
gerc_toplam_adet = st.session_state.eylul_ankara_adet + st.session_state.eylul_merter_adet + st.session_state.eylul_zeruj_adet
genel_oran = (gerc_toplam_ciro / hedef_toplam_ciro) * 100 if hedef_toplam_ciro > 0 else 0

# --- ANA DASHBOARD EKRANI ---
st.title("🎯 Molène Mağazalar | Ağustos & Eylül Performans Dashboard")
st.markdown(f"Ağustos resmi kapanış verileri ve **{st.session_state.veri_tarihi.strftime('%d.%m.%Y')}** tarihli güncel Eylül takip ekranı.")

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
e1.metric("Eylül Hedef Ciro", f"{hedef_toplam_ciro:,.2f} TRY")
e2.metric("Eylül Gerçekleşen", f"{gerc_toplam_ciro:,.2f} TRY")
e3.metric("Hedef / Gerç. Adet", f"{hedef_toplam_adet} / {gerc_toplam_adet}")
e4.metric("Eylül Gerçekleşme", f"%{genel_oran:.1f}")

st.markdown("### 📌 Mağaza Bazlı Eylül Tablosu")

ank_oran = (st.session_state.eylul_ankara_ciro / hedef_ankara) * 100
mer_oran = (st.session_state.eylul_merter_ciro / hedef_merter) * 100
zer_oran = (st.session_state.eylul_zeruj_ciro / hedef_zeruj) * 100

eylül_tablo = [
    {"Mağaza": "Ankara", "Hedef Ciro": f"{hedef_ankara:,.0f} TRY", "Gerçekleşen Ciro": f"{st.session_state.eylul_ankara_ciro:,.0f} TRY", "Hedef Adet": 2783, "Gerç. Adet": st.session_state.eylul_ankara_adet, "Gerçekleşme": f"%{ank_oran:.1f}", "Durum": "Kritik 🔴"},
    {"Mağaza": "Merter", "Hedef Ciro": f"{hedef_merter:,.0f} TRY", "Gerçekleşen Ciro": f"{st.session_state.eylul_merter_ciro:,.0f} TRY", "Hedef Adet": 880, "Gerç. Adet": st.session_state.eylul_merter_adet, "Gerçekleşme": f"%{mer_oran:.1f}", "Durum": "Kritik 🔴"},
    {"Mağaza": "Zeruj Toplam", "Hedef Ciro": f"{hedef_zeruj:,.0f} TRY", "Gerçekleşen Ciro": f"{st.session_state.eylul_zeruj_ciro:,.0f} TRY", "Hedef Adet": 5929, "Gerç. Adet": st.session_state.eylul_zeruj_adet, "Gerçekleşme": f"%{zer_oran:.1f}", "Durum": "Kritik 🔴"},
]
st.table(eylül_tablo)

st.markdown("---")
st.markdown("### 📊 Mağaza Bazlı Detaylı Analiz & Değerlendirme")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("#### 🏛️ Ankara Mağaza Analizi")
    st.markdown(
        f"- **Bütçe Durumu:** {hedef_ankara:,.0f} TRY hedef karşısında {st.session_state.eylul_ankara_ciro:,.0f} TRY gerçekleşme.\n"
        f"- **Adet Verimliliği:** 2.783 hedef adete karşılık {st.session_state.eylul_ankara_adet} adet çıkış.\n"
        "- **Analiz:** Yan panelden girilen verilere göre bütçe sapmaları ve performans anlık olarak hesaplanmaktadır."
    )

with col_b:
    st.markdown("#### 🏬 Merter Mağaza Analizi")
    st.markdown(
        f"- **Bütçe Durumu:** {hedef_merter:,.0f} TRY hedef karşısında {st.session_state.eylul_merter_ciro:,.0f} TRY gerçekleşme.\n"
        f"- **Adet Verimliliği:** 880 hedef adete karşılık {st.session_state.eylul_merter_adet} adet çıkış.\n"
        "- **Analiz:** Günlük ciro girişleriyle birlikte sepet ortalaması ve realize oranları takip edilmektedir."
    )

with col_c:
    st.markdown("#### 🛍️ Zeruj Toplam Analizi")
    st.markdown(
        f"- **Bütçe Durumu:** {hedef_zeruj:,.0f} TRY hedef karşısında {st.session_state.eylul_zeruj_ciro:,.0f} TRY gerçekleşme.\n"
        f"- **Adet Verimliliği:** 5.929 hedef adete karşılık {st.session_state.eylul_zeruj_adet} adet çıkış.\n"
        "- **Analiz:** Kanal ağırlığı yüksek olan Zeruj verileri güncellendikçe yansımaktadır."
    )
