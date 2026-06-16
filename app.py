import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# App-Konfiguration für Smartphones optimieren
st.set_page_config(page_title="HAUG CHEMIE Vorbehandlung", page_icon="🧪", layout="centered")

# --- FUNKTION: E-MAIL SENDEN ---
def sende_protokoll_email(bericht_text):
    smtp_server = "smtp.gmail.com"  
    port = 465  
    absender_email = "D_Wowi@web.de" 
    passwort = "KST3910" 
    empfaenger_email = "daniel.wowereit@karcher.com"

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
        st.caption("Eingesetzte Chemie: eska phor N 6811 (Neutralreiniger)")
        
        fs1 = st.slider("Füllstand (%):", 50, 100, 70)
        v_eff1 = 4000 * (fs1 / 100.0)
        st.info(f"Berechnetes aktuelles Beckenvolumen: {int(v_eff1)} Liter")
        
        ph1 = st.number_input("pH-Wert (Ziel: 9.0 - 9.5):", min_value=0.0, max_value=14.0, value=9.2, step=0.1, key="p1")
        lw1 = st.number_input("Leitwert (Ziel: 4000 - 9000 µS/cm):", min_value=0, max_value=20000, value=5500, step=100, key="l1")
        temp1 = st.number_input("Temperatur (Ziel: 55 - 60 °C):", min_value=0, max_value=100, value=58, key="t1")
        ml1 = st.number_input("Titration in ml (Entfettung):", min_value=0.0, max_value=50.0, value=5.5, key="m1")
        ist_konz1 = ml1 * 0.5
        
        bedarf_kg1 = max(0.0, (2.75 - ist_konz1) * (v_eff1 / 1000.0) * 10.0) if ist_konz1 < 2.5 else 0.0
        
        st.metric(label="Aktuelle Konzentration Entfettung", value=f"{ist_konz1} %", delta=f"{round(ist_konz1 - 2.75, 2)} % (Ziel: 2.5 - 3.0%)")
        if bedarf_kg1 > 0:
            st.error(f"❌ KONZENTRATION ZU GERING! Bitte exakt nachdosieren:")
            st.markdown(f"### ⚖️ **{round(bedarf_kg1, 1)} kg** oder 🧪 **{round(bedarf_kg1/1.09, 1)} Liter** eska phor N 6811 hinzugeben.")
            st.warning("""
            **⚠️ VORGESCHRIEBENE PSA (Laut Sicherheitsdatenblatt eska phor N 6811):**
            * Signalwort: **GEFAHR** (Verursacht schwere Augenschäden & Hautreizungen)
            * Schutzbrille: **Gestellbrille mit Seitenschutz** tragen!
            * Handschutz: **Fluorkautschuk (FKM, 0.7 mm)** oder **Polychloropren (CR, 0.65 mm)** nutzen!
            * Körperschutz: **Schürze** verpflichtend!
            """)
        else:
            st.success("🎯 Konzentration und Beckenwerte im optimalen Bereich!")

    with tab2:
        st.subheader("Becken 2: Spüle 2")
        lw2 = st.number_input("Leitwert (Ziel: max. 1500 µS/cm):", min_value=0, max_value=5000, value=1100, key="l2")
        temp2 = st.number_input("Temperatur (Ziel: 30 - 40 °C):", min_value=0, max_value=100, value=34, key="t2")
        if lw2 > 1500: 
            st.error("❌ Leitwert zu hoch! Bitte Frischwasserzulauf erhöhen.")
        else:
            st.success("✅ Spülwasser-Leitwert im grünen Bereich.")

    with tab3:
        st.subheader("Becken 3: VE-Spüle 1")
        lw3 = st.number_input("Leitwert (Ziel: max. 250 µS/cm):", min_value=0, max_value=2000, value=150, key="l3")
        if lw3 > 250: 
            st.error("❌ Leitwert zu hoch! VE-Wasserqualität ungenügend.")
        else:
            st.success("✅ Erste VE-Spüle läuft sauber.")

    with tab4:
        st.subheader("Becken 4: Passivierung (eska phor P 355-2)")
        st.caption("Eingesetzte Chemie: eska phor P 355-2 (Dünnschichtpassivierung)")
        
        fs4 = st.slider("Füllstand Passivierung (%):", 50, 100, 70)
        v_eff4 = 1000 * (fs4 / 100.0)
        st.info(f"Berechnetes aktuelles Passivierungsvolumen: {int(v_eff4)} Liter")
        
        ph4 = st.number_input("pH-Wert (Ziel: 4.5 - 5.0):", min_value=0.0, max_value=14.0, value=4.7, step=0.1, key="p4")
        lw4 = st.number_input("Leitwert (Ziel: max. 500 µS/cm):", min_value=0, max_value=5000, value=350, key="l4")
        ml4 = st.number_input("Titration Passivierung in ml:", min_value=0.0, max_value=50.0, value=4.4, key="m4")
        ist_konz4 = ml4 * 0.05
        
        bedarf_kg4 = max(0.0, (0.225 - ist_konz4) * (v_eff4 / 1000.0) * 10.0) if ist_konz4 < 0.15 else 0.0
        
        st.metric(label="Aktuelle Konzentration Passivierung", value=f"{round(ist_konz4, 3)} %", delta=f"{round(ist_konz4 - 0.225, 3)} % (Ziel: 0.15 - 0.30%)")
        if bedarf_kg4 > 0:
            st.error(f"❌ KONZENTRATION ZU GERING! Bitte exakt nachdosieren:")
            st.markdown(f"### ⚖️ **{round(bedarf_kg4, 2)} kg** oder 🧪 **{round(bedarf_kg4/1.09, 2)} Liter** eska phor P 355-2 hinzugeben.")
            st.warning("""
            **⚠️ VORGESCHRIEBENE PSA (Laut Sicherheitsdatenblatt eska phor P 355-2):**
            * Signalwort: **GEFAHR** (Enthält Triethanolammoniumhexafluorozirconat. Verursacht schwere Augenschäden)
            * Schutzbrille: **Gestellbrille mit Seitenschutz** zwingend erforderlich!
            * Handschutz: **Fluorkautschuk (FKM, 0.7 mm)** oder **Polychloropren (CR, 0.65 mm)**!
            * Körperschutz: Flüssigkeitsdichte **Schürze** anlegen!
            """)
        else:
            st.success("🎯 Passivierungsbad läuft stabil im optimalen Bereich.")

    with tab5:
        st.subheader("Becken 5: VE-Spüle 2")
        lw5 = st.number_input("Leitwert (Ziel: max. 50 µS/cm):", min_value=0, max_value=500, value=15, key="l5")
        if lw5 > 50: 
            st.error("🚨 KRITISCH! Leitwert zu hoch! Gefahr von Salzflecken unter dem Pulver!")
        else:
            st.success("🎯 Perfekt! Leitwert ist optimal.")

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
- Nachdosiermenge: {round(bedarf_kg4, 2)} kg ({round(bedarf_kg4/1.09, 2)} Liter)

Becken 5 (VE-Spüle 2): Leitwert {lw5} µS (Soll: max. 50 µS)

Schöne Grüße,
Deine Vorbehandlungs-App"""
                
                with st.spinner("E-Mail wird gesendet..."):
                    erfolg = sende_protokoll_email(bericht)
                    if erfolg: st.success("🎉 Protokoll per E-Mail gesendet!")
                    else: st.error("❌ E-Mail-Versand fehlgeschlagen.")
else:
    st.info("💡 Bitte hake zuerst alle Punkte des Morgen-Check-ups ab, um die Analyse freizuschalten.")
