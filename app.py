import streamlit as st

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

# --- VERİ TABANI (AĞUSTOS KAPANIŞ & EYLÜL İLK 3 GÜN) ---
AGUSTOS_VERILERI = {
    "toplam": {"hedef_ciro": 10215505.88, "gerceklesen_ciro": 10071896.05, "oran": "%99"},
    "ankara": {"hedef_ciro": 2760000.00, "gerceklesen_ciro": 2922495.00, "oran": "%108"},
    "merter": {"hedef_ciro": 884006.00, "gerceklesen_ciro": 924156.00, "oran": "%105"},
    "zeruj_ag": {"hedef_ciro": 4401000.00, "gerceklesen_ciro": 4322265.00, "oran": "%98"},
    "zeruj_eg": {"hedef_ciro": 2170500.00, "gerceklesen_ciro": 1902980.00, "oran": "%88"}
}

EYLUL_VERILERI = {
    "toplam": {"hedef_ciro": 12086275.00, "gerceklesen_ciro": 626615.00, "hedef_adet": 9592, "gerceklesen_adet": 525, "oran": "%5.2"},
    "ankara": {"hedef_ciro": 3506994.00, "gerceklesen_ciro": 187495.00, "hedef_adet": 2783, "gerceklesen_adet": 166},
    "merter": {"hedef_ciro": 1108987.00, "gerceklesen_ciro": 68620.00, "hedef_adet": 880, "gerceklesen_adet": 62},
    "zeruj": {"hedef_ciro": 7470294.00, "gerceklesen_ciro": 370499.00, "hedef_adet": 5929, "gerceklesen_adet": 297}
}

# --- DASHBOARD ARAYÜZÜ ---
st.title("🎯 Molène Mağazalar | Ağustos Kapanış & Eylül Performans Dashboard")
st.markdown("Ağustos resmi kapanış verileri ve Eylül ayı ilk 3 gün performans takip ekranı.")

# Sekmeler (Dashboard vs Asistan)
tab_dash, tab_asistan = st.tabs(["📊 KPI Dashboard", "💬 Kurumsal Asistan Terminali"])

with tab_dash:
    st.markdown("### 📈 Ağustos Ayı Kesinleşmiş Kapanış Özet Kartları")
    c1, c2, c3, c4 = st.columns(4)
    t_ag = AGUSTOS_VERILERI["toplam"]
    c1.metric("Ağustos Hedef Ciro", f"{t_ag['hedef_ciro']:,.2f} TRY")
    c2.metric("Ağustos Gerçekleşen", f"{t_ag['gerceklesen_ciro']:,.2f} TRY")
    c3.metric("Ağustos Gerçekleşme", t_ag['oran'])
    c4.metric("Kapanış Durumu", "Tamamlandı 🟢")

    st.markdown("---")
    st.markdown("### 📉 Eylül Ayı İlk 3 Gün Performans Özeti")
    
    e1, e2, e3, e4 = st.columns(4)
    t_ey = EYLUL_VERILERI["toplam"]
    e1.metric("Eylül Hedef Ciro", f"{t_ey['hedef_ciro']:,.2f} TRY")
    e2.metric("Eylül Gerçekleşen", f"{t_ey['gerceklesen_ciro']:,.2f} TRY", delta="-11.4M TRY")
    e3.metric("Hedef / Gerç. Adet", f"{t_ey['hedef_adet']} / {t_ey['gerceklesen_adet']}")
    e4.metric("Eylül Gerçekleşme", t_ey['oran'])
    
    st.warning("Eylül ayı genel ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔 Ankara, Merter ve Zeruj mağazalarımızda alokasyon ve sevkiyat stratejilerini acilen sıkı tutmalıyız.")

    st.markdown("### 📌 Mağaza Bazlı Eylül İlk 3 Gün Tablosu")
    eylül_tablo = [
        {"Mağaza": "Ankara", "Hedef Ciro": "3.506.994 TRY", "Gerçekleşen Ciro": "187.495 TRY", "Hedef Adet": 2783, "Gerç. Adet": 166, "Durum": "Kritik 🔴"},
        {"Mağaza": "Merter", "Hedef Ciro": "1.108.987 TRY", "Gerçekleşen Ciro": "68.620 TRY", "Hedef Adet": 880, "Gerç. Adet": 62, "Durum": "Kritik 🔴"},
        {"Mağaza": "Zeruj Toplam", "Hedef Ciro": "7.470.294 TRY", "Gerçekleşen Ciro": "370.499 TRY", "Hedef Adet": 5929, "Gerç. Adet": 297, "Durum": "Kritik 🔴"},
    ]
    st.table(eylül_tablo)

with tab_asistan:
    st.subheader("💬 Kurumsal Akıllı Asistan Terminali")
    st.markdown("Ağustos kapanışları, Eylül verileri, mağazalar ve yönetim hakkında soru sorabilirsiniz.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Örn: Ağustos nasıl kapandı? Veya Eylül ayı Ankara mağazası durumu nedir?"):
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
            elif any(k in soru for k in ["selam", "merhaba", "mrb", "günaydın", "iyi akşamlar", "nasılsın", "naber"]):
                bot_yaniti = "Aleykümselam! Ağustos kesinleşmiş verileri ve Eylül ayı ilk 3 gün performansı hazır. Hangi analize bakıyoruz?"
            
            # 3. Patronlar ve Şirket Bilgisi
            elif any(k in soru for k in ["patron", "sahip", "kurucu", "ortak", "bilal", "semih", "molène", "molene"]):
                bot_yaniti = (
                    "Molène markasının kurucu ortakları Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                    "İdari, raporlama ve operasyonel yönetim otoritesi ise Yiğit Deniz Ünseven'dir."
                )
            
            # 4. Ağustos Kapanış Detayları
            elif "ağustos" in soru:
                bot_yaniti = (
                    "📊 **Ağustos Ayı Kapanış Özeti:**\n"
                    f"- **Toplam Hedef Ciro:** {t_ag['hedef_ciro']:,.2f} TRY\n"
                    f"- **Toplam Gerçekleşen:** {t_ag['gerceklesen_ciro']:,.2f} TRY ({t_ag['oran']})\n"
                    "- Ankara (%108) ve Merter (%105) hedeflerini aşarken; Zeruj Ag (%98) ve Zeruj Eg (%88) ile dönemi tamamlamıştır."
                )
            
            # 5. Eylül Canlı Veri Soruları
            elif "eylül" in soru:
                bot_yaniti = (
                    "📉 **Eylül Ayı İlk 3 Gün Özeti:**\n"
                    f"- **Toplam Hedef Ciro:** {EYLUL_VERILERI['toplam']['hedef_ciro']:,.2f} TRY\n"
                    f"- **Toplam Gerçekleşen:** {EYLUL_VERILERI['toplam']['gerceklesen_ciro']:,.2f} TRY ({EYLUL_VERILERI['toplam']['oran']})\n"
                    "Ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔 "
                    "Ankara, Merter ve Zeruj mağazalarımızdaki detayları yukarıdaki KPI Dashboard sekmesinden inceleyebilirsin."
                )
            
            # 6. Kapsam Dışı Güvenlik Duvarı
            else:
                bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

            st.markdown(bot_yaniti)
            st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
