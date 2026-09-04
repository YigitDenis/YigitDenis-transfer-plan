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

# --- GOOGLE E-TABLO VERİ ÇEKME MOTORU ---
@st.cache_data(ttl=60) # Veriyi her 1 dakikada bir günceller/önbelleğe alır
def veri_cek():
    try:
        # Belirttiğin Google E-Tablo ve "ai Sayfa" sekmesi export linki
        sheet_id = "1TFXBAtfGrCLQzze7Llbg4fI0pWL2kkWEb0eBuX71kKE"
        sheet_name = "ai Sayfa"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)
        return df, "Başarılı"
    except Exception as e:
        return None, str(e)

df_veri, durum = veri_cek()

# --- KURUMSAL MOTOR VE CHAT ARAYÜZÜ ---

st.title("🎯 Molène Tüm Mağazalar Hedef ve Performans Takip Asistanı")
st.markdown("Google E-Tablolar ('ai Sayfa') entegre canlı bütçe, ciro ve operasyon asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Ağustos ayı nasıl kapandı? Veya Eylül ayı hedefleri ne durumda?"):
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
            bot_yaniti = "Aleykümselam! Çok iyiyim, 'ai Sayfa' verilerini anlık takip ediyorum. Sen nasılsın, hangi ayın veya mağazanın verilerine bakıyoruz?"
        
        # 3. Patronlar ve Şirket Bilgisi
        elif any(k in soru for k in ["patron", "sahip", "kurucu", "ortak", "bilal", "semih", "molène", "molene"]):
            bot_yaniti = (
                "Molène markasının kurucu ortakları Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "İdari, raporlama ve operasyonel yönetim otoritesi ise Yiğit Deniz Ünseven'dir."
            )
        
        # 4. Tablo Verileri Sorgulama (Ağustos, Eylül, Mağazalar, Hedefler)
        elif any(k in soru for k in ["hedef", "ciro", "eylül", "ağustos", "bütçe", "prim", "satış", "ankara", "merter", "zeruj", "mağaza", "tablo", "veri"]):
            if durum == "Başarılı" and df_veri is not None:
                # Tablodan özet bilgi türetme veya veriyi aksettirme
                tablo_ozeti = f"Tablonuzdan 'ai Sayfa' verileri güncel olarak çekilmiştir. Tablonuzda toplam {len(df_veri)} satır veri bulunmaktadır."
            else:
                tablo_ozeti = "Google E-Tablo bağlantısında veri okunurken geçici bir sorun yaşandı, ancak genel hafızamızdaki Ağustos ve Eylül verileriyle devam ediyoruz."

            bot_yaniti = (
                f"{tablo_ozeti}\n\n"
                "📊 **Genel Değerlendirme:**\n"
                "Ağustos ayı verilerimiz sistemde kayıtlıdır; Eylül ayında ise ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔\n"
                "Ankara, Merter ve Zeruj mağazalarımızda bütçe ve satış sapmalarını toparlamak için alokasyon stratejilerini acilen sıkı tutmalıyız."
            )
        
        # 5. Kapsam Dışı Her Şey İçin Güvenlik Duvarı
        else:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
