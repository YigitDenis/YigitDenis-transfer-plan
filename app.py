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
@st.cache_data(ttl=30)
def google_sheets_cek():
    try:
        sheet_id = "1TFXBAtfGrCLQzze7Llbg4fI0pWL2kkWEb0eBuX71kKE"
        sheet_name = "ai Sayfa"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)
        return df, "Başarılı"
    except Exception as e:
        return None, str(e)

df_canli, veri_durumu = google_sheets_cek()

# --- AĞUSTOS SABİT KAPANIŞ VERİLERİ ---
AGUSTOS_VERILERI = {
    "toplam": {"hedef_ciro": 10215505.88, "gerceklesen_ciro": 10071896.05, "oran": "%99"},
    "ankara": {"hedef_ciro": 2760000.00, "gerceklesen_ciro": 2922495.00, "oran": "%108"},
    "merter": {"hedef_ciro": 884006.00, "gerceklesen_ciro": 924156.00, "oran": "%105"},
    "zeruj_ag": {"hedef_ciro": 4401000.00, "gerceklesen_ciro": 4322265.00, "oran": "%98"},
    "zeruj_eg": {"hedef_ciro": 2170500.00, "gerceklesen_ciro": 1902980.00, "oran": "%88"}
}

# --- DASHBOARD ARAYÜZÜ ---
st.title("🎯 Molène Mağazalar | Ağustos Kapanış & Eylül Canlı Dashboard")
st.markdown("Ağustos resmi kapanış verileri ile Google E-Tablolar ('ai Sayfa') üzerinden beslenen Eylül canlı performans ekranı.")

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
    st.markdown("### 🔄 Eylül Ayı Canlı Veri Akışı ('ai Sayfa')")
    
    if veri_durumu == "Başarılı" and df_canli is not None:
        st.success("Google E-Tablolar ('ai Sayfa') verisi başarıyla senkronize edildi.")
        st.dataframe(df_canli, use_container_width=True)
    else:
        st.warning("Google E-Tablo verisi okunurken geçici bir bağlantı sorunu oluştu. Lütfen tablonun paylaşımının açık olduğundan emin olun.")
        st.markdown("*(Eylül ayı ilk 3 gün özeti: Toplam Hedef 12.086.275 TRY | Gerçekleşen 626.615 TRY - Hedeflerin gerisindeyiz, içimiz sızlıyor 📉😔)*")

with tab_asistan:
    st.subheader("💬 Kurumsal Akıllı Asistan Terminali")
    st.markdown("Ağustos kapanışları, Eylül canlı verileri, mağazalar ve yönetim hakkında soru sorabilirsiniz.")

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
                bot_yaniti = "Aleykümselam! Ağustos kesinleşmiş verileri ve Google E-Tablo Eylül canlı verileri hazır. Hangi analize bakıyoruz?"
            
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
                    "📉 **Eylül Ayı Canlı Durum:**\n"
                    "Eylül ayı verileri doğrudan Google E-Tablolar ('ai Sayfa') üzerinden çekilmektedir. "
                    "Genel ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔 "
                    "Ankara, Merter ve Zeruj mağazalarımızdaki güncel performansları yukarıdaki KPI Dashboard sekmesinden detaylı inceleyebilirsin."
                )
            
            # 6. Kapsam Dışı Güvenlik Duvarı
            else:
                bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

            st.markdown(bot_yaniti)
            st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
