import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Akıllı Filtre Tıkanma İzleme", layout="wide")
st.title("Akıllı Filtre Tıkanma İzleme (ΔP Tabanlı)")

# Sidebar ayarları
warn_thr = st.sidebar.number_input("Uyarı eşiği (bar)", value=0.30, step=0.05)
alarm_thr = st.sidebar.number_input("Alarm eşiği (bar)", value=0.50, step=0.05)
mode = st.sidebar.selectbox("Veri kaynağı", ["Simülasyon", "CSV yükle"])
n_samples = st.sidebar.slider("Örnek sayısı (simülasyon için)", 20, 200, 60)

# E-posta ayarları (basic)
st.sidebar.subheader("E-posta Bildirimi")
send_email_enabled = st.sidebar.checkbox("Alarmda e-posta gönder", value=False)
sender_email = st.sidebar.text_input("Gönderici e-posta", value="")
sender_password = st.sidebar.text_input("E-posta şifresi", type="password")
receiver_email = st.sidebar.text_input("Alıcı e-posta", value="")

# Alarm e-posta gönderme fonksiyonu
def send_email(subject, body):
    if not (sender_email and sender_password and receiver_email):
        st.warning("E-posta ayarlarını tamamlayın!")
        return
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        st.success("E-posta gönderildi!")
    except Exception as e:
        st.error(f"E-posta gönderilemedi: {e}")

def classify(dp):
    if dp >= alarm_thr:
        return "ALARM", "🔴"
    elif dp >= warn_thr:
        return "UYARI", "🟠"
    else:
        return "NORMAL", "🟢"

# Veri yükleme veya simülasyon
if mode == "CSV yükle":
    uploaded = st.file_uploader("CSV yükle (kolonlar: time, p_in, p_out)", type=["csv"])
    if uploaded is None:
        st.info("Örnek CSV için kolonlar: time, p_in, p_out")
        st.stop()
    df = pd.read_csv(uploaded)
else:
    p_in = 1.2
    p_out = np.linspace(1.15, 0.65, n_samples) + np.random.normal(0, 0.01, n_samples)
    df = pd.DataFrame({
        "time": np.arange(n_samples),
        "p_in": np.full(n_samples, p_in),
        "p_out": p_out
    })

df["dp"] = df["p_in"] - df["p_out"]

placeholder_metrics = st.empty()
placeholder_chart = st.empty()
placeholder_table = st.empty()

# Tekrar e-posta göndermemek için flag
email_sent = False

if mode == "Simülasyon":
    df_display = pd.DataFrame(columns=df.columns)
    for i in range(len(df)):
        latest = df.iloc[i]
        status, icon = classify(latest["dp"])

        # Metric
        col1, col2, col3 = placeholder_metrics.columns(3)
        col1.metric("Giriş Basıncı (bar)", f"{latest['p_in']:.2f}")
        col2.metric("Çıkış Basıncı (bar)", f"{latest['p_out']:.2f}")
        col3.metric("ΔP = P_in - P_out (bar)", f"{latest['dp']:.2f}")

        # Durum mesajı
        if status == "ALARM":
            st.error(f"{icon} Filtre tıkanma alarmı! Bakım / değişim önerilir.")
            if send_email_enabled and not email_sent:
                send_email("Filtre Alarmı!", f"Filtre alarmı! ΔP = {latest['dp']:.2f} bar")
                email_sent = True
        elif status == "UYARI":
            st.warning(f"{icon} Tıkanma artıyor. Backwash / temizlik önerilir.")
        else:
            st.success(f"{icon} Sistem normal çalışıyor.")

        # Grafik
        df_display = pd.concat([df_display, df.iloc[[i]]])
        base = alt.Chart(df_display).mark_line(point=True).encode(
            x="time",
            y="dp"
        )
        rule_warn = alt.Chart(pd.DataFrame({'y': [warn_thr]})).mark_rule(color="orange", strokeDash=[4,4]).encode(y="y")
        rule_alarm = alt.Chart(pd.DataFrame({'y': [alarm_thr]})).mark_rule(color="red", strokeDash=[4,4]).encode(y="y")
        chart = (base + rule_warn + rule_alarm).properties(height=300)
        placeholder_chart.altair_chart(chart, use_container_width=True)

        # Tablo
        placeholder_table.dataframe(df_display.tail(20))
        time.sleep(0.1)
else:
    latest = df.iloc[-1]
    status, icon = classify(latest["dp"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Giriş Basıncı (bar)", f"{latest['p_in']:.2f}")
    col2.metric("Çıkış Basıncı (bar)", f"{latest['p_out']:.2f}")
    col3.metric("ΔP = P_in - P_out (bar)", f"{latest['dp']:.2f}")

    if status == "ALARM":
        st.error(f"{icon} Filtre tıkanma alarmı! Bakım / değişim önerilir.")
        if send_email_enabled:
            send_email("Filtre Alarmı!", f"Filtre alarmı! ΔP = {latest['dp']:.2f} bar")
    elif status == "UYARI":
        st.warning(f"{icon} Tıkanma artıyor. Backwash / temizlik önerilir.")
    else:
        st.success(f"{icon} Sistem normal çalışıyor.")

    base = alt.Chart(df).mark_line(point=True).encode(
        x="time",
        y="dp"
    )
    rule_warn = alt.Chart(pd.DataFrame({'y': [warn_thr]})).mark_rule(color="orange", strokeDash=[4,4]).encode(y="y")
    rule_alarm = alt.Chart(pd.DataFrame({'y': [alarm_thr]})).mark_rule(color="red", strokeDash=[4,4]).encode(y="y")
    chart = (base + rule_warn + rule_alarm).properties(height=300)
    st.altair_chart(chart, use_container_width=True)
    st.subheader("Veri tablosu (son 20 örnek)")
    st.dataframe(df.tail(20))