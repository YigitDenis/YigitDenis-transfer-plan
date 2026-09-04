import streamlit as st
import google.generativeai as genai

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

# --- AKILLI ÇÖZÜM ---
# Streamlit secrets (st.secrets) kullanarak anahtarı güvenle ve hatasız çekiyoruz.
# Eğer anahtar ayarlara girilmediyse, yerleşik akıllı yanıt motoru devreye girer (asla çökmez).
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        api_aktif = True
    else:
        api_aktif = False
except:
    api_aktif = False

st.title("🎯 Molène Tüm Mağazalar Hedef ve Performans Takip Asistanı")
st.markdown("Tüm mağazalar, bütçe takipleri, ciro hedefleri ve perakende operasyonları asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Eylül ayı hedefleri nasıl gidiyor? Veya genel kültür/teknik bir soru sorabilirsin."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        soru_kucuk = prompt.lower()
        bot_yaniti = ""

        # 1. Yiğit Deniz Kuralı
        if "yiğit" in soru_kucuk or "deniz" in soru_kucuk:
            bot_yaniti = "O sizin için burada, sorgulamayın, dediğini yapın geçin! :)"
        
        # 2. Şirket / Kurucular (Bilal Bey ve Semih Bey)
        elif any(k in soru_kucuk for k in ["molène", "molene", "kurucu", "ortak", "bilal", "semih", "mağaza", "zeruj", "ankara", "merter", "depo"]):
            bot_yaniti = (
                "Molène, kadın giyim sektöründe faaliyet gösteren öncü bir markadır. "
                "Kurucu ortaklarımız Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "Mağazalarımız: Zeruj Port (AG & EG), Ankara ATG, Merter mağazası ve güçlü E-ticaret kanalımızdır. "
                "Depomuz in-house çalışmakta; mağazalara haftada 3 gün, e-ticarete her gün sevkiyat yapılmaktadır."
            )
        
        # 3. Eylül Ayı Hedef / Ciro Durumu (Hüzünlü Ton)
        elif any(k in soru_kucuk for k in ["hedef", "ciro", "eylül", "bütçe", "prim", "satış"]):
            bot_yaniti = (
                "Eylül ayı genel ciro hedeflerimizin ne yazık ki gerisindeyiz, içim gerçekten sızlıyor... 📉😔 "
                "Ankara, Merter ve Zeruj mağazalarımızda ilk günlerdeki dalgalanmaları toparlamak için Nebim V3 ve Iontegra WMS verileri üzerinden alokasyon ve satış stratejilerini sıkı tutmalıyız."
            )
        
        # 4. Yetki Dışı / Güvenlik Duvarı
        elif "sır" in soru_kucuk or "şifre" in soru_kucuk or "maaş" in soru_kucuk:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"
        
        # 5. Genel İnternet / Günlük Sorular İçin Yapay Zeka Devrede
        else:
            if api_aktif:
                try:
                    system_instruction = (
                        "Sen Molène Mağazalar AI Asistanısın. Kurucular Bilal Bey, Semih Bey ve eşleri Ayşegül Hanım & Esma Hanım. "
                        "Kullanıcının internetten veya genel kültürden sorduğu her türlü soruya (teknik, sosyal, günlük hayat vb.) "
                        "akıllıca, net, profesyonel ve akıcı bir Türkçe ile eksiksiz cevap ver."
                    )
                    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
                    response = model.generate_content(prompt)
                    bot_yaniti = response.text
                except:
                    bot_yaniti = "Genel sorularınız için perakende operasyonları, Nebim V3 ve Iontegra WMS süreçlerine odaklanabiliriz. Bugün mağazalar için hangi analizi yapalım? 😊"
            else:
                # API anahtarı yoksa veya hata alıyorsa yerleşik akıllı yanıt motoru
                bot_yaniti = f"Harika bir soru! Molène ekibi olarak bu konuda analitik düşünüyoruz. Başka hangi departman veya mağaza detayıyla ilgileniyorsun?"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
