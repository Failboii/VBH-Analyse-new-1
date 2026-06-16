import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# App-Konfiguration für Smartphones optimieren
st.set_page_config(page_title="HAUG CHEMIE Vorbehandlung", page_icon="🧪", layout="centered")

# --- DESIGN-UPGRADE: KÄRCHER-STYLE (RAL 7012 BASALTLGRAU & KÄRCHER GELB) ---
st.markdown(
    """
    <style>
    /* Hintergrund der App: RAL 7012 Basaltgrau */
    [data-testid="stAppViewContainer"] {
        background-color: #5F696E !important;
    }

    /* Die Hauptkarte: Weiß, übersichtlich, mit Kärcher-Gelb Akzentstreifen oben */
    [data-testid="stMainBlockContainer"] {
        background-color: #FFFFFF !important;
        padding: 2.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.4);
        border-top: 12px solid #FFDD00; /* Kärcher Gelb */
        margin-top: 30px;
        margin-bottom: 30px;
    }
    
    /* RADIKALER KONTRAST-FIX: Zwingt allen Text, Überschriften und Labels im Hauptfenster dazu, dunkelgrau zu sein */
    [data-testid="stMainBlockContainer"] h1, 
    [data-testid="stMainBlockContainer"] h2, 
    [data-testid="stMainBlockContainer"] h3, 
    [data-testid="stMainBlockContainer"] p,
    [data-testid="stMainBlockContainer"] label,
    [data-testid="stMainBlockContainer"] span,
    [data-testid="stMainBlockContainer"] div {
        color: #222222 !important;
    }
    
    /* Ausnahme für Text in Warn- und Erfolgsboxen (damit die Lesbarkeit dort passt) */
    [data-testid="stNotification"] p,
    [data-testid="stNotification"] h1,
    [data-testid="stNotification"] h2,
    [data-testid="stNotification"] h3,
    [data-testid="stNotification"] span {
        color: inherit !important;
    }

    /* Aktivierter Reiter (Tab) bekommt einen Kärcher-Gelben Balken */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #FFDD00 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- FUNKTION: E-MAIL SENDEN ---
def sende_protokoll_email(bericht_text):
    smtp_server = "smtp.gmail.com"  # Falls du Gmail nutzt, sonst z.B. smtp.strato.de etc.
    port = 465  # SSL Port
    absender_email = "DEINE_ANLAGEN_EMAIL@gmail.com" 
    passwort = "DEIN_SMTP_APP_PASSWORT" 
    empfaenger_email = "DEINE_CHEF_EMAIL@deinefirma.de"

    msg = MIMEMultipart()
    msg['From'] = absender_email
    msg['To'] = empfaenger_email
    msg['Subject'] = f"🧪 VBH-Analyse Protokoll vom {datetime.now().strftime('%d.%m.%Y - %H:%M')}"

    msg.attach(MIMEText(bericht_text, 'plain'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(absender_email, passwort)
        server.sendmail(absender_email, empfaenger_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"E-Mail-Fehler: {e}")
        return False

# --- ANWENDUNGSTART ---
st.title("🧪 Qualitätskontrolle Vorbehandlung")
st.write("Produktionsüberwachung & Dosierrechner")

# --- SCHRITT 1: MORGEN-CHECK ---
st.header("1. Morgen-Check-up")
st.write("Bitte zuerst alle mechanischen Prüfungen bestätigen:")

col1, col2 = st.columns(2)
with col1:
    uv_anlage = st.checkbox("🔄 UV-Anlage gestartet")
    pumpen = st.checkbox("⚙️ Pumpen auf Automatik geschaltet")

st.divider()

# Bandfilter-Option mit Tausch-Logik
st.subheader("📄 Bandfilter-Prüfung")
bandfilter_status = st.radio("Zustand des Filtervlieses:", ["Vlies ausreichend / OK", "🚨 Filtervlies ist leer / muss getauscht werden"])
bandfilter_bereit = True if bandfilter_status == "Vlies ausreichend / OK" else st.checkbox("✅ Tausch durchgeführt (Neues Vlies eingelegt)")

st.divider()

# Salzstand-Option mit Sack-Zähler
st.subheader("🧂 Enthärtungsanlage (Salzstand)")
salz_geprueft = st.checkbox("🔍 Salzstand kontrolliert")
salz_nachgefuellt = st.checkbox("➕ Wurde heute Salz nachgefüllt?")
saecke = st.radio("Wie viele Säcke?", [1, 2, 3], horizontal=True) if salz_nachgefuellt else 0

if uv_anlage and pumpen and bandfilter_bereit and salz_geprueft:
    st.success("✅ Morgen-Check-up erfolgreich abgeschlossen!")
    st.divider()
    
    # --- SCHRITT 2: DIE BECKEN ---
    st.header("2. Analyse & Messwerte")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["1. Entfettung", "2. Spüle 2", "3. VE-Spüle 1", "4. Passivierung", "5. VE-Spüle 2", "📊 Historie & Absenden"])
    
    with tab1:
        st.subheader("Becken 1: Entfettung (eska phor N 6811)")
        fs1 = st.slider("Füllstand (%):", 50, 100, 70)
        v_eff1 = 4000 * (fs1 / 100.0)
        ph1 = st.number_input("pH-Wert (9.0-9.5):", 0.0, 14.0, 9.2, step=0.1, key="p1")
        lw1 = st.number_input("Leitwert (4000-9000):", 0, 20000, 5500, step=100, key="l1")
        temp1 = st.number_input("Temperatur (55-60 °C):", 0, 100, 58, key="t1")
        ml1 = st.number_input("Titration (ml):", 0.0, 50.0, 5.5, key="m1")
        ist_konz1 = ml1 * 0.5
        
        bedarf_kg1 = max(0.0, (2.75 - ist_konz1) * (v_eff1 / 1000.0) * 10.0) if ist_konz1 < 2.5 else 0.0
        
        st.metric(label="Aktuelle Konzentration Entfettung", value=f"{ist_konz1} %", delta=f"{round(ist_konz1 - 2.75, 2)} %")
        if bedarf_kg1 > 0:
            st.error(f"❌ KONZENTRATION ZU GERING! Bitte exakt nachdosieren:")
            st.markdown(f"### ⚖️ **{round(bedarf_kg1, 1)} kg** oder 🧪 **{round(bedarf_kg1/1.09, 1)} Liter** eska phor N 6811 hinzugeben.")

    with tab2:
        st.subheader("Becken 2: Spüle 2")
        lw2 = st.number_input("Leitwert (max. 1500):", 0, 5000, 1100, key="l2")
        temp2 = st.number_input("Temperatur (30-40 °C):", 0, 100, 34, key="t2")
        if lw2 > 1500: st.error("❌ Leitwert zu hoch!")

    with tab3:
        st.subheader("Becken 3: VE-Spüle 1")
        lw3 = st.number_input("Leitwert (max. 250):", 0, 2000, 150, key="l3")
        if lw3 > 250: st.error("❌ Leitwert zu hoch!")

    with tab4:
        st.subheader("Becken 4: Passivierung (eska phor P 355-2)")
        fs4 = st.slider("Füllstand Passivierung (%):", 50, 100, 70)
        v_eff4 = 1000 * (fs4 / 100.0)
        ph4 = st.number_input("pH-Wert (4.5-5.0):", 0.0, 14.0, 4.7, step=0.1, key="p4")
        lw4 = st.number_input("Leitwert (max. 500):", 0, 5000, 350, key="l4")
        ml4 = st.number_input("Titration Passivierung (ml):", 0.0, 50.0, 4.4, key="m4")
        ist_konz4 = ml4 * 0.05
        
        bedarf_kg4 = max(0.0, (0.225 - ist_konz4) * (v_eff4 / 1000.0) * 10.0) if ist_konz4 < 0.15 else 0.0
        
        st.metric(label="Aktuelle Konzentration Passivierung", value=f"{round(ist_konz4, 3)} %", delta=f"{round(ist_konz4 - 0.225, 3)} %")
        if bedarf_kg4 > 0:
            st.error(f"❌ KONZENTRATION ZU GERING! Bitte exakt nachdosieren:")
            st.markdown(f"### ⚖️ **{round(bedarf_kg4, 2)} kg** oder 🧪 **{round(bedarf_liter4, 2)} Liter** eska phor P 355-2 hinzugeben.")

    with tab5:
        st.subheader("Becken 5: VE-Spüle 2")
        lw5 = st.number_input("Leitwert (max. 50):", 0, 500, 15, key="l5")
        if lw5 > 50: st.error("🚨 KRITISCH! Leitwert zu hoch!")

    # --- TAB 6: HISTORIE & ABSENDEN ---
    with tab6:
        st.subheader("📊 Datenauswertung (Letzte 4 Tage)")
        historische_daten = {
            "Datum": ["12.06.", "13.06.", "14.06.", "15.06."],
            "Konzentr. Entfettung (%)": [2.8, 2.6, 2.4, 2.7],
            "Leitwert VE-Spüle 2 (µS)": [12, 18, 35, 15],
            "pH Passivierung": [4.7, 4.8, 4.6, 4.7]
        }
        df = pd.DataFrame(historische_daten)
        st.dataframe(df, use_container_width=True)
        st.line_chart(df.set_index("Datum")["Konzentr. Entfettung (%)"])

        st.divider()
        st.subheader("✉️ Protokoll an Chef senden")
        mitarbeiter_name = st.text_input("Name des Prüfers:", placeholder="z.B. Max Mustermann")
        
        if st.button("🚀 Analyse absenden & E-Mail verschicken"):
            if mitarbeiter_name == "":
                st.warning("Bitte trage zuerst deinen Namen ein!")
            else:
                bericht = f"""Hallo Chef,
die tägliche VBH-Analyse wurde soeben durchgeführt.

Prüfer: {mitarbeiter_name}
Zeitstempel: {datetime.now().strftime('%d.%m.%Y um %H:%M Uhr')}

--- 1. REINIGUNG & GEWERKE ---
Bandfilter-Status: {bandfilter_status}
Salz nachgefüllt: {'Ja, ' + str(saecke) + ' Säcke' if salz_nachgefuellt else 'Nein'}

--- 2. MESSWERTE ---
Becken 1 (Entfettung):
- Aktuelle Konz.: {ist_konz1} % (Soll: 2.5 - 3.0%)
- pH-Wert: {ph1} | Leitwert: {lw1} µS | Temp: {temp1} °C
- Nachdosiermenge: {round(bedarf_kg1, 1)} kg ({round(bedarf_kg1/1.09, 1)} Liter)

Becken 2 (Spüle 2): Leitwert {lw2} µS
Becken 3 (VE-Spüle 1): Leitwert {lw3} µS

Becken 4 (Passivierung):
- Aktuelle Konz.: {round(ist_konz4, 3)} % (Soll: 0.15 - 0.30%)
- pH-Wert: {ph4} | Leitwert: {lw4} µS
- Nachdosiermenge: {round(bedarf_kg4, 2)} kg

Becken 5 (VE-Spüle 2): Leitwert {lw5} µS (Soll: max. 50 µS)

Schöne Grüße,
Deine Vorbehandlungs-App"""
                
                with st.spinner("E-Mail wird gesendet..."):
                    erfolg = sende_protokoll_email(bericht)
                    if erfolg: st.success("🎉 Protokoll per E-Mail gesendet!")
                    else: st.error("❌ E-Mail-Versand fehlgeschlagen.")
else:
    st.info("💡 Bitte hake zuerst alle Punkte des Morgen-Check-ups ab, um die Analyse freizuschalten.")
