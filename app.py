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

# --- ŞİFRE DOĞRUYSA ÇALIŞACAK UYGULAMA ---

st.title("🎯 Molène Tüm Mağazalar Hedef ve Performans Takip Asistanı")
st.markdown("Tüm mağazalar, bütçe takipleri, ciro hedefleri ve perakende operasyonları asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Hava nasıl? Veya mağazaların durumu nedir?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        soru_kucuk = prompt.lower()
        
        # 1. Günlük Selamlaşma ve Hal Hatır
        if any(kelime in soru_kucuk for kelime in ["selam", "merhaba", "mrb", "günaydın", "iyi akşamlar", "nasılsın", "ne naber"]):
            bot_yaniti = "Aleykümselam! Çok iyiyim, Molène ekibiyle birlikte tempoyu düşürmeden çalışıyoruz. Sen nasılsın, bugün hangi konulara bakıyoruz? 😊"
        
        # 2. Havadan Sudan / Hava Durumu
        elif any(kelime in soru_kucuk for kelime in ["hava", "yağmur", "sıcak", "güneş", "nasıldır", "dışarı"]):
            bot_yaniti = "Bugün dışarısı oldukça dinamik, tam e-ticaret kargolarını paketleyip mağazalara sevkiyat yapmalık bir hava var! 🌤️ Sen dışarı çıkma fırsatı buldun mu yoksa ofiste yoğun tempoda mısın?"
        
        # 3. Yiğit Deniz / Deniz Bey Kuralı
        elif "yiğit" in soru_kucuk or "deniz" in soru_kucuk:
            bot_yaniti = "O sizin için burada, sorgulamayın, dediğini yapın geçin! :)"
        
        # 4. Şirket ve Mağaza Bilgileri (Bilal Bey ve Semih Bey Güncellemeli)
        elif any(kelime in soru_kucuk for kelime in ["molène", "molene", "kim", "kurucu", "ortak", "bilal", "semih", "mağaza", "zeruj", "ankara", "merter", "depo"]):
            bot_yaniti = (
                "Molène, kadın giyim sektöründe faaliyet gösteren öncü bir markadır. "
                "Kurucu ortaklarımız Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "Mağazalarımız: Zeruj Port (AG & EG), Ankara ATG, Merter mağazası ve güçlü E-ticaret kanalımızdır. "
                "Depomuz kendi bünyemizde in-house olarak çalışmakta; mağazalara haftada 3 gün, e-ticarete ise her gün sevkiyat yapılmaktadır."
            )
        
        # 5. Hedefler ve Ciro Durumu
        elif any(kelime in soru_kucuk for kelime in ["hedef", "ciro", "eylül", "bütçe", "prim"]):
            bot_yaniti = (
                "Eylül ayı genel ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔 "
                "Ankara, Merter ve Zeruj mağazalarımızda ilk günlerdeki dalgalanmaları toparlamak için satış ve alokasyon stratejilerini sıkı tutmalıyız."
            )
        
        # 6. Operasyon / Perakende Süreçleri
        elif any(kelime in soru_kucuk for kelime in ["raf", "alokasyon", "müşteri", "satış", "stok", "nebim", "iotegra"]):
            bot_yaniti = (
                "Perakende operasyonlarımız Nebim V3 (ERP) ve Iontegra WMS (Depo) entegrasyonuyla yönetilmektedir. "
                "Doğru ürünün doğru mağazada ve rafta olması, depo sevkiyatlarının aksamaması ve müşteri ilişkilerinin en üst düzeyde tutulması temel önceliğimizdir."
            )
        
        # 7. Yetki Dışı / Bilinmeyen Konular
        else:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
