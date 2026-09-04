import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Molène Mağazalar Prim ve Hedef Simülasyonu", page_icon="🎯", layout="wide")

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

# --- PRİM HESAPLAMA MOTORU ---
def prim_hesapla(magaza, gerceklesen_ciro, hedef_ciro):
    oran = (gerceklesen_ciro / hedef_ciro) * 100 if hedef_ciro > 0 else 0
    
    if magaza == "ankara":
        if oran >= 110: prim = 57865
        elif oran >= 100: prim = 42084
        elif oran >= 90: prim = 25250
        else: prim = 0
    elif magaza == "merter":
        if oran >= 110: prim = 18298
        elif oran >= 100: prim = 13308
        elif oran >= 90: prim = 7985
        else: prim = 0
    elif magaza == "zeruj":
        if oran >= 110: prim = 123260
        elif oran >= 100: prim = 89644
        elif oran >= 90: prim = 53786
        else: prim = 0
    else:
        prim = 0
        
    return oran, prim

st.title("🎯 Molène Mağaza Performans ve Prim Simülasyonu")
st.markdown("Mağaza bazlı ciro hedefleri, gerçekleşmeler ve anlık prim hakediş simülasyonu.")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Örn: Ankara mağazası prim durumu nedir? Veya Zeruj hedefe ulaşırsa ne alır?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        soru = prompt.lower()
        bot_yaniti = ""

        # 1. Yiğit Deniz Kuralı
        if any(k in soru for k in ["yiğit", "deniz", "ünseven"]):
            bot_yaniti = "O sizin için burada, sorgulamayın, dediğini yapın geçin! :)"
        
        # 2. Patronlar ve Şirket Bilgisi
        elif any(k in soru for k in ["patron", "sahip", "kurucu", "ortak", "bilal", "semih", "molène", "molene"]):
            bot_yaniti = (
                "Molène markasının kurucu ortakları Bilal Bey & eşi Ayşegül Hanım ile Semih Bey & eşi Esma Hanım'dır. "
                "İdari, raporlama ve operasyonel yönetim otoritesi ise Yiğit Deniz Ünseven'dir."
            )
        
        # 3. Ankara Prim Simülasyonu
        elif "ankara" in soru:
            hedef = 3506994
            gerceklesen = 187495  # İlk 3 günlük mevcut
            oran, prim = prim_hesapla("ankara", gerceklesen, hedef)
            
            # Simülasyon: Eğer %100 yapılırsa
            prim_100 = 42084
            prim_110 = 57865
            
            bot_yaniti = (
                "🏛️ **Ankara Mağaza Prim ve Hedef Durumu:**\n"
                f"- **Hedef Ciro:** {hedef:,} TRY\n"
                f"- **Mevcut Gerçekleşen:** {gerceklesen:,} TRY (Gerçekleşme Oranı: %{oran:.1f})\n"
                f"- **Mevcut Prim Hakedişi:** {prim:,} TRY\n\n"
                "📌 **Simülasyon / Hedef Baremleri:**\n"
                f"- %90 - %99 aralığında: 25.250 TRY\n"
                f"- %100 - %109 aralığında: {prim_100:,} TRY\n"
                f"- %110 ve üzeri: {prim_110:,} TRY\n"
                "Hedeflerin çok gerisindeyiz, ekibin primi hak etmesi için ciroyu acilen patlatmamız gerekiyor! 📉😔"
            )

        # 4. Merter Prim Simülasyonu
        elif "merter" in soru:
            hedef = 1108987
            gerceklesen = 68620
            oran, prim = prim_hesapla("merter", gerceklesen, hedef)
            
            bot_yaniti = (
                "🏬 **Merter Mağaza Prim ve Hedef Durumu:**\n"
                f"- **Hedef Ciro:** {hedef:,} TRY\n"
                f"- **Mevcut Gerçekleşen:** {gerceklesen:,} TRY (Gerçekleşme Oranı: %{oran:.1f})\n"
                f"- **Mevcut Prim Hakedişi:** {prim:,} TRY\n\n"
                "📌 **Simülasyon / Hedef Baremleri:**\n"
                "- %90 - %99: 7.985 TRY\n"
                "- %100 - %109: 13.308 TRY\n"
                "- %110+: 18.298 TRY\n"
                "3 Eylül'deki düşüş primi tehlikeye atıyor, içim sızlıyor... 📉😔"
            )

        # 5. Zeruj Prim Simülasyonu
        elif "zeruj" in soru:
            hedef = 7470294
            gerceklesen = 370499
            oran, prim = prim_hesapla("zeruj", gerceklesen, hedef)
            
            bot_yaniti = (
                "🛍️ **Zeruj Toplam Prim ve Hedef Durumu:**\n"
                f"- **Hedef Ciro:** {hedef:,} TRY\n"
                f"- **Mevcut Gerçekleşen:** {gerceklesen:,} TRY (Gerçekleşme Oranı: %{oran:.1f})\n"
                f"- **Mevcut Prim Hakedişi:** {prim:,} TRY\n\n"
                "📌 **Simülasyon / Hedef Baremleri:**\n"
                "- %90 - %99: 53.786 TRY\n"
                "- %100 - %109: 89.644 TRY\n"
                "- %110+: 123.260 TRY\n"
                "Hacim büyük, ödül büyük ama mevcut seyir bizi üzüyor..."
            )

        # 6. Genel Durum
        elif any(k in soru for k in ["hedef", "ciro", "eylül", "prim", "bütçe"]):
            bot_yaniti = (
                "📉 **Genel Prim ve Hedef Durumu:**\n"
                "Eylül ayı genel ciro hedeflerimizin altındayız. Ankara, Merter veya Zeruj mağazalarından hangisinin prim simülasyonunu ve detaylı baremlerini görmek istiyorsun?"
            )

        # 7. Kapsam Dışı Güvenlik Duvarı
        else:
            bot_yaniti = "Bu konu hakkında bilgi vermem, Deniz bey kızar :)"

        st.markdown(bot_yaniti)
        st.session_state.messages.append({"role": "assistant", "content": bot_yaniti})
