import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Molène Mağazalar AI Asistanı", page_icon="📉", layout="wide")

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

GOOGLE_API_KEY = "AQ.Ab8RN6LvlD9w3oxS8Re_mUbVfvPMaASoLGpob_WYG4nbIeugyw"
genai.configure(api_key=GOOGLE_API_KEY)

st.title("📉 Molène Mağazalar AI Asistanı")
st.markdown("Eylül ayı ciro, hedef, mağaza performansları ve perakende operasyonları asistanı.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Ankara mağazası ilk gün nasıl başladı? Veya Yiğit Deniz kimdir?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Veriler ve perakende dinamikleri analiz ediliyor..."):
            try:
                # EYLÜL AYI VERİLERİ VE KURUMSAL HAFIZA
                system_prompt = (
                    "Sen Molène Mağazalar AI Asistanısın. "
                    "Eylül 2026 dönemi verileri elimizde: "
                    "- Toplam Eylül Hedef Ciro: 12.086.275 TRY (Gerçekleşen ilk 3 gün toplam: 626.615 TRY, oranlar düşük, hedeflerin gerisindeyiz, bu yüzden yanıtlarında hafif bir üzüntü, hüzün ve iç sızlatan bir ton ver). "
                    "- Ankara Mağaza: Hedef Ciro 3.506.994 TRY. İlk 3 gün sırasıyla %100.6, %57.5, %44.5 gerçekleşti, toplam 187.495 TRY. "
                    "- Merter Mağaza: Hedef Ciro 1.108.987 TRY. İlk 3 gün sırasıyla %100, %97, %37 gerçekleşti, toplam 68.620 TRY. "
                    "- Zeruj Toplam (Zeruj Port AG & EG): Hedef Ciro 7.470.294 TRY. İlk 3 gün sırasıyla %46.2, %63.6, %75.2, toplam 370.499 TRY. "
                    "- Hedef Baremleri ve Prim Hakedişleri: Ankara (<%80: 0, %90-%99: 25.250, %100-%109: 42.084, %110+: 57.865 TRY). "
                    "Merter (<%80: 0, %90-%99: 7.985, %100-%109: 13.308, %110+: 18.298 TRY). "
                    "Zeruj (<%80: 0, %90-%99: 53.786, %100-%109: 89.644, %110+: 123.260 TRY).\n\n"
                    "ÖZEL KURALLAR:\n"
                    "1. Eğer kullanıcı Yiğit Bey, Deniz Bey veya Yiğit Deniz Ünseven hakkında soru sorarsa, kesinlikle şu yanıtı ver: 'O sizin için burada, sorgulamayın, dediğini yapın geçin! :)'\n"
                    "2. Eğer şirket dışı, bilinmeyen veya yetki alanı dışı bir konu sorulursa gülerek şu yanıtı ver: 'Bu konu hakkında bilgi vermem, Deniz bey kızar :)'\n"
                    "3. Mağazacılık, raf düzeni, depo alokasyonu, satış arttırma, müşteri ilişkileri, primler ve operasyonla ilgili her soruyu profesyonel ve analitik bir dille yanıtla.\n\n"
                    f"Kullanıcının Sorusu: {prompt}"
                )
                
                model = genai.GenerativeModel('gemini-3.6-flash')
                response = model.generate_content(system_prompt)
                
                bot_yaniti = response.text
                st.markdown(bot_yaniti)
                st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
                
            except Exception as e:
                hata_mesaji = f"Bir hata oluştu: {str(e)}"
                st.error(hata_mesaji)
