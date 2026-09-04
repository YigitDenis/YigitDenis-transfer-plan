import streamlit as st

# Sayfa Ayarları (Geniş Ekran ve Profesyonel Konsept)
st.set_page_config(
    page_title="Molène Mağazalar | Ağustos Kapanış & KPI Dashboard", 
    page_icon="📊", 
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

# --- AĞUSTOS KAPANIŞ KESİN VERİ TABANI ---
AGUSTOS_VERILERI = {
    "toplam": {
        "hedef_ciro": 10215505.88, "gerceklesen_ciro": 10071896.05,
        "hedef_adet": 6810, "gerceklesen_adet": 7520, "gerceklesme_oran": "%99"
    },
    "ankara": {
        "hedef_ciro": 2760000.00, "gerceklesen_ciro": 2922495.00,
        "hedef_adet": 1840, "gerceklesen_adet": 2379, "gerceklesme_oran": "%108"
    },
    "merter": {
        "hedef_ciro": 884006.00, "gerceklesen_ciro": 924156.00,
        "hedef_adet": 589, "gerceklesen_adet": 738, "gerceklesme_oran": "%105"
    },
    "zeruj_ag": {
        "hedef_ciro": 4401000.00, "gerceklesen_ciro": 4322265.00,
        "hedef_adet": 2934, "gerceklesen_adet": 3171, "gerceklesme_oran": "%98"
    },
    "zeruj_eg": {
        "hedef_ciro": 2170500.00, "gerceklesen_ciro": 1902980.00,
        "hedef_adet": 1447, "gerceklesen_adet": 1232, "gerceklesme_oran": "%88"
    }
}

# --- DASHBOARD BAŞLIĞI VE ÖZET KARTLARI (KPI METRİKLERİ) ---
st.title("📊 Molène | Ağustos Ayı Kapanış ve Performans Dashboard")
st.markdown("Ağustos ayı resmi kapanış verileri, mağaza bazlı ciro/adet gerçekleşmeleri ve operasyonel özet.")

st.markdown("### 🏆 Ağustos Genel Performans Özet Kartları")
col1, col2, col3, col4 = st.columns(4)

t_veri = AGUSTOS_VERILERI["toplam"]
col1.metric("Toplam Hedef Ciro", f"{t_veri['hedef_ciro']:,.2f} TRY")
col2.metric("Gerçekleşen Ciro", f"{t_veri['gerceklesen_ciro']:,.2f} TRY", delta="-143k TRY (%99)")
col3.metric("Hedef Adet / Gerç. Adet", f"{t_veri['hedef_adet']} / {t_veri['gerceklesen_adet']}")
col4.metric("Genel Gerçekleşme", t_veri['gerceklesme_oran'])

st.markdown("---")

# --- MAĞAZA BAZLI DETAYLI KARŞILAŞTIRMA TABLOSU ---
st.subheader("📌 Mağaza Bazlı Ağustos Kapanış Tablosu")

tablo_verisi = [
    {"Mağaza": "Ankara", "Hedef Ciro": "2.760.000 TRY", "Gerçekleşen Ciro": "2.922.495 TRY", "Hedef Adet": 1840, "Gerç. Adet": 2379, "Performans": "%108 🟢"},
    {"Mağaza": "Merter", "Hedef Ciro": "884.006 TRY", "Gerçekleşen Ciro": "924.156 TRY", "Hedef Adet": 589, "Gerç. Adet": 738, "Performans": "%105 🟢"},
    {"Mağaza": "Zeruj Ag", "Hedef Ciro": "4.401.000 TRY", "Gerçekleşen Ciro": "4.322.265 TRY", "Hedef Adet": 2934, "Gerç. Adet": 3171, "Performans": "%98 🔴"},
    {"Mağaza": "Zeruj Eg", "Hedef Ciro": "2.170.500 TRY", "Gerçekleşen Ciro": "1.902.980 TRY", "Hedef Adet": 1447, "Gerç. Adet": 1232, "Performans": "%88 🔴"},
]

st.table(tablo_verisi)

st.markdown("---")

# --- YÖNETİCİ SOHBET VE ASİSTAN TERMİNALİ ---
st.subheader("💬 Kurumsal Akıllı Asistan Terminali")
st.markdown("Ağustos kapanışları, mağaza detayları veya yöneticiler hakkında sorularınızı yazabilirsiniz.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Ankara ağustos ayı nasıl kapandı? Veya Zeruj Eg durumu nedir?"):
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
            bot_yaniti = "Aleykümselam! Molène Ağustos kapanış dashboardu ve verileri aktif. Hangi mağazanın detayını incelemek istiyorsun?"
        
        # 3. Patronlar ve Şirket Bilgisi
        elif any(k in soru for k in ["patron", "sahip", "kurucu", "ortak", "bilal", "semih", "molène", "molene"]):
            bot_yaniti = (
                "Molène markasının kurucu ortakları Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "İdari, raporlama ve operasyonel yönetim otoritesi ise Yiğit Deniz Ünseven'dir."
            )
        
        # 4. Ankara Ağustos Kapanış
        elif "ankara" in soru:
            d = AGUSTOS_VERILERI["ankara"]
            bot_yaniti = (
                "🏛️ **Ankara Mağaza - Ağustos Kapanış Raporu:**\n"
                f"- **Ciro Hedef:** {d['hedef_ciro']:,.2f} TRY | **Gerçekleşen Ciro:** {d['gerceklesen_ciro']:,.2f} TRY\n"
                f"- **Adet Hedef:** {d['hedef_adet']} | **Gerçekleşen Adet:** {d['gerceklesen_adet']}\n"
                f"- **Hedef Gerçekleşme:** {d['gerceklesme_oran']} 🟢\n"
                "Ankara mağazamız Ağustos ayını başarıyla ve hedefini aşarak kapatmıştır."
            )
        
        # 5. Merter Ağustos Kapanış
        elif "merter" in soru:
            d = AGUSTOS_VERILERI["merter"]
            bot_yaniti = (
                "🏬 **Merter Mağaza - Ağustos Kapanış Raporu:**\n"
                f"- **Ciro Hedef:** {d['hedef_ciro']:,.2f} TRY | **Gerçekleşen Ciro:** {d['gerceklesen_ciro']:,.2f} TRY\n"
                f"- **Adet Hedef:** {d['hedef_adet']} | **Gerçekleşen Adet:** {d['gerceklesen_adet']}\n"
                f"- **Hedef Gerçekleşme:** {d['gerceklesme_oran']} 🟢\n"
                "Merter mağazamız Ağustos ayında bütçesini tutturmuş ve üstü bir performans sergilemiştir."
            )
        
        # 6. Zeruj Ag Ağustos Kapanış
        elif "zeruj ag" in soru or ("zeruj" in soru and "ag" in soru):
            d = AGUSTOS_VERILERI["zeruj_ag"]
            bot_yaniti = (
                "🛍️ **Zeruj Ag Mağaza - Ağustos Kapanış Raporu:**\n"
                f"- **Ciro Hedef:** {d['hedef_ciro']:,.2f} TRY | **Gerçekleşen Ciro:** {d['gerceklesen_ciro']:,.2f} TRY\n"
                f"- **Adet Hedef:** {d['hedef_adet']} | **Gerçekleşen Adet:** {d['gerceklesen_adet']}\n"
                f"- **Hedef Gerçekleşme:** {d['gerceklesme_oran']} 🔴\n"
                "Zeruj Ag küçük bir sapmayla hedefin hemen altında (%98) Ağustos'u tamamlamıştır."
            )

        # 7. Zeruj Eg Ağustos Kapanış
        elif "zeruj eg" in soru or ("zeruj" in soru and "eg" in soru):
            d = AGUSTOS_VERILERI["zeruj_eg"]
            bot_yaniti = (
                "🛍️ **Zeruj Eg Mağaza - Ağustos Kapanış Raporu:**\n"
                f"- **Ciro Hedef:** {d['hedef_ciro']:,.2f} TRY | **Gerçekleşen Ciro:** {d['gerceklesen_ciro']:,.2f} TRY\n"
                f"- **Adet Hedef:** {d['hedef_adet']} | **Gerçekleşen Adet:** {d['gerceklesen_adet']}\n"
                f"- **Hedef Gerçekleşme:** {d['gerceklesme_oran']} 🔴\n"
                "Zeruj Eg ağustos ayında bütçenin bir miktar gerisinde kalmış (%88), operasyonel takibe alınmıştır."
            )

        # 8. Ağustos Genel Toplam
        elif "ağustos" in soru or "toplam" in soru:
            d = AGUSTOS_VERILERI["toplam"]
            bot_yaniti = (
                "📊 **Ağustos Ayı Genel Kapanış Özeti:**\n"
                f"- **Toplam Hedef Ciro:** {d['hedef_ciro']:,.2f} TRY\n"
                f"- **Toplam Gerçekleşen Ciro:** {d['gerceklesen_ciro']:,.2f} TRY\n"
                f"- **Toplam Adet:** {d['gerceklesen_adet']} (Hedef: {d['hedef_adet']})\n"
                f"- **Genel Gerçekleşme:** {d['gerceklesme_oran']}\n"
                "Ağustos ayı resmi kapanışı yüzde 99 oranla tamamlanmıştır."
            )
        
        # 9. Kapsam Dışı Güvenlik Duvarı
        else:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
