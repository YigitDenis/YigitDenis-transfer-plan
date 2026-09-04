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

# --- MÜKEMMEL ÇALIŞAN AKILLI YERLEŞİK MOTOR ---

st.title("🎯 Molène Tüm Mağazalar Hedef ve Performans Takip Asistanı")
st.markdown("Tüm mağazalar, bütçe takipleri, ciro hedefleri ve perakende operasyonları asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Karl Marks kimdir? Veya Ankara mağazası eylül ayı durumu ne?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        soru = prompt.lower()
        
        # 1. Yiğit Deniz Kuralı
        if "yiğit" in soru or "deniz" in soru:
            bot_yaniti = "O sizin için burada, sorgulamayın, dediğini yapın geçin! :)"
        
        # 2. Selamlaşma ve Hal Hatır
        elif any(k in soru for k in ["selam", "merhaba", "mrb", "günaydın", "iyi akşamlar", "nasılsın", "ne naber"]):
            bot_yaniti = "Aleykümselam! Çok iyiyim, Molène ekibiyle birlikte tempoyu düşürmeden çalışıyoruz. Sen nasılsın, bugün hangi departman konularına bakıyoruz? 😊"
        
        # 3. Genel Kültür (Örn: Karl Marks vb.)
        elif "karl marks" in soru or "marx" in soru:
            bot_yaniti = "Karl Marks, 19. yüzyılda yaşamış Alman filozof, ekonomist ve politik teorisyendir. Özellikle Kapital ve Komünist Manifesto eserleriyle tanınır; kapitalist ekonomi sistemini eleştiren teorileriyle bilinir."
        elif "tarih" in soru or "felsefe" in soru or "bilim" in soru:
            bot_yaniti = f" '{prompt}' konusu oldukça derin ve analitik bir konu. Molène ekibi olarak her alanda olduğu gibi bilgiye de stratejik yaklaşıyoruz!"
        
        # 4. Şirket, Kurucular ve Mağazalar (Bilal Bey ve Semih Bey)
        elif any(k in soru for k in ["molène", "molene", "kurucu", "ortak", "bilal", "semih", "mağaza", "zeruj", "ankara", "merter", "depo", "e-ticaret"]):
            bot_yaniti = (
                "Molène, kadın giyim sektöründe faaliyet gösteren öncü bir markadır. "
                "Kurucu ortaklarımız Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "Mağazalarımız: Zeruj Port (AG & EG), Ankara ATG, Merter mağazası ve güçlü E-ticaret kanalımızdır. "
                "Depomuz in-house çalışmakta; mağazalara haftada 3 gün, e-ticarete her gün sevkiyat yapılmaktadır."
            )
        
        # 5. Eylül / Ağustos Ayı Hedef ve Ciro Durumu (Hüzünlü Ton)
        elif any(k in soru for k in ["hedef", "ciro", "eylül", "ağustos", "bütçe", "prim", "satış"]):
            bot_yaniti = (
                "Eylül ayı genel ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔 "
                "Ankara, Merter ve Zeruj mağazalarımızda ilk günlerdeki dalgalanmaları toparlamak için Nebim V3 ve Iontegra WMS verileri üzerinden alokasyon ve satış stratejilerini acilen sıkı tutmalıyız."
            )
        
        # 6. Yetki Dışı / Güvenlik Duvarı
        elif "sır" in soru in soru or "şifre" in soru or "maaş" in soru:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"
        
        # 7. Diğer Tüm Genel Sorular İçin Akıllı Esneklik
        else:
            bot_yaniti = f" '{prompt}' konusunu ve perakende dinamiklerimizi Nebim V3 ve Iontegra WMS altyapımızla harmanlayıp en doğru analizi çıkarabiliriz. Başka hangi detayla devam edelim?"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
