import streamlit as st

# App-Konfiguration für Smartphones optimieren
st.set_page_config(page_title="HAUG CHEMIE Vorbehandlung", page_icon="🧪", layout="centered")

# --- DESIGN-UPGRADE: ANIMIERTES STAHLBECKEN (CSS INJECTION) ---
st.markdown(
    """
    <style>
    /* Hintergrund der gesamten App: Gebürsteter Industriestahl mit Schimmereffekt */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #4b535c, #788491, #a1b0be, #788491, #4b535c);
        background-size: 400% 400%;
        animation: steelShine 14s ease-in-out infinite;
    }

    /* Animation für den metallischen Lichtreflex */
    @keyframes steelShine {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Die Inhaltskarte: Leicht transparent, damit das Stahlbecken durchschimmert, aber der Text perfekt lesbar bleibt */
    [data-testid="stMainBlockContainer"] {
        background-color: rgba(255, 255, 255, 0.94);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.4);
        border: 3px solid #5d6770;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    
    /* Schickere Tabs für die Beckenauswahl */
    .stTabs [data-baseweb="tab"] {
        font-weight: bold;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
bandfilter_status = st.radio(
    "Zustand des Filtervlieses:",
    ["Vlies ausreichend / OK", "🚨 Filtervlies ist leer / muss getauscht werden"],
    index=0
)

bandfilter_bereit = False
filter_becken = "Kein Tausch erforderlich"

if bandfilter_status == "🚨 Filtervlies ist leer / muss getauscht werden":
    filter_becken = st.selectbox(
        "Bei welchem Becken muss das Vlies getauscht werden?",
        ["Becken 1 (Entfettung)", "Becken 4 (Passivierung)", "Zentraler Bandfilter / Andere"]
    )
    filter_gewechselt = st.checkbox("✅ Tausch durchgeführt (Neues Vlies ist eingelegt)")
    if filter_gewechselt:
        st.success(f"👍 Tausch an '{filter_becken}' erfolgreich dokumentiert.")
        bandfilter_bereit = True
else:
    bandfilter_bereit = True

st.divider()

# Salzstand-Option mit Sack-Zähler
st.subheader("🧂 Enthärtungsanlage (Salzstand)")
salz_geprueft = st.checkbox("🔍 Salzstand kontrolliert")
salz_nachgefuellt = st.checkbox("➕ Wurde heute Salz nachgefüllt?")

saecke_salz = 0
if salz_nachgefuellt:
    saecke_salz = st.radio(
        "Wie viele Säcke (je 25 kg) wurden nachgefüllt?",
        [1, 2, 3],
        horizontal=True
    )
    st.info(f"💾 Protokoll: {saecke_salz} Sack Salz hinzugefügt.")

# Freigabe-Logik für die Beckenanalyse
if uv_anlage and pumpen and bandfilter_bereit and salz_geprueft:
    st.success("✅ Morgen-Check-up erfolgreich abgeschlossen! Bereit für die Messwerte.")
    st.divider()
    
    # --- SCHRITT 2: DIE 5 BECKEN ---
    st.header("2. Analyse & Messwerte der Becken")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Entfettung", 
        "2. Spüle 2", 
        "3. VE-Spüle 1", 
        "4. Passivierung", 
        "5. VE-Spüle 2"
    ])
    
    # --- BECKEN 1: ENTFETTUNG (eska phor N 6811) ---
    with tab1:
        st.subheader("Becken 1: Entfettung (Max. 4.000 Liter)")
        st.caption("Eingesetzte Chemie: eska phor N 6811 (Neutralreiniger)")
        
        fs1 = st.slider("Aktueller Füllstand (in %):", min_value=50, max_value=100, value=70, step=1, key="fs1")
        v_eff1 = 4000 * (fs1 / 100.0)
        st.info(f"Berechnetes aktuelles Beckenvolumen: {int(v_eff1)} Liter")
        
        ph1 = st.number_input("pH-Wert (Ziel: 9.0 - 9.5):", min_value=0.0, max_value=14.0, value=9.2, step=0.1, key="ph1")
        lw1 = st.number_input("Leitwert (Ziel: 4000 - 9000 µS/cm):", min_value=0, max_value=20000, value=5500, step=100, key="lw1")
        temp1 = st.number_input("Temperatur (Ziel: 55 - 60 °C):", min_value=0, max_value=100, value=58, step=1, key="temp1")
        
        st.markdown("**Laboranalyse (Titration):**")
        ml1 = st.number_input("Verbrauch Titrierlösung in ml (Entfettung):", min_value=0.0, max_value=50.0, value=5.5, step=0.1, key="ml1")
        
        titrations_faktor_entfettung = 0.5 
        ist_konz1 = ml1 * titrations_faktor_entfettung
        soll_min1 = 2.5
        soll_max1 = 3.0
        soll_ziel1 = 2.75
        
        st.markdown("### 📋 Handlungsanweisung:")
        
        if not (9.0 <= ph1 <= 9.5):
            st.error(f"❌ pH-Wert außerhalb! Aktuell: {ph1} (Soll: 9.0 - 9.5).")
        if not (4000 <= lw1 <= 9000):
            st.error(f"❌ Leitwert außerhalb! Aktuell: {lw1} µS/cm (Soll: 4000 - 9000 µS/cm).")
        if not (55 <= temp1 <= 60):
            st.warning(f"⚠️ Heizung/Temperatur prüfen! Aktuell: {temp1} °C (Soll: 55 - 60 °C).")
            
        st.metric(label="Aktuelle Konzentration Entfettung", value=f"{ist_konz1} %", delta=f"{round(ist_konz1 - soll_ziel1, 2)} % (Ziel: 2.5 - 3.0%)")
        
        if ist_konz1 < soll_min1:
            fehlende_prozent = soll_ziel1 - ist_konz1
            chemie_faktor1 = 10.0 
            bedarf_kg = (fehlende_prozent * (v_eff1 / 1000.0)) * chemie_faktor1
            bedarf_liter = bedarf_kg / 1.09
            
            st.error(f"❌ KONZENTRATION ZU GERING! Bitte exakt nachdosieren:")
            st.markdown(f"### ⚖️ **{round(bedarf_kg, 1)} kg** oder 🧪 **{round(bedarf_liter, 1)} Liter** eska phor N 6811 hinzugeben.")
            
            st.warning("""
            **⚠️ VORGESCHRIEBENE PSA (Laut Sicherheitsdatenblatt eska phor N 6811):**
            * Signalwort: **GEFAHR** (Verursacht schwere Augenschäden & Hautreizungen) [cite: 901, 902, 906]
            * Schutzbrille: **Gestellbrille mit Seitenschutz** tragen! [cite: 1130]
            * Handschutz: **Fluorkautschuk (FKM, 0.7 mm)** oder **Polychloropren (CR, 0.65 mm)** nutzen! [cite: 1135, 1136, 1137]
            * Körperschutz: **Schürze** verpflichtend! [cite: 1142]
            """)
        elif ist_konz1 > soll_max1:
            st.warning("⚠️ Konzentration zu hoch! Automatische Dosierpumpe drosseln oder vorübergehend abschalten.")
        else:
            st.success("🎯 Konzentration und Beckenwerte sind perfekt im Soll!")

    # --- BECKEN 2: SPÜLE 2 ---
    with tab2:
        st.subheader("Becken 2: Spüle 2 (Max. 1.000 Liter)")
        lw2 = st.number_input("Leitwert (Ziel: max. 1500 µS/cm):", min_value=0, max_value=5000, value=1100, key="lw2")
        temp2 = st.number_input("Temperatur (Ziel: 30 - 40 °C):", min_value=0, max_value=100, value=34, key="temp2")
        
        st.markdown("### 📋 Handlungsanweisung:")
        if lw2 > 1500:
            st.error(f"❌ Leitwert zu hoch ({lw2} µS/cm)! Spülwasser stark verschleppt. Bitte Frischwasserzulauf erhöhen oder Becken teilentleeren.")
        else:
            st.success("✅ Spülwasser-Leitwert ist in Ordnung.")
        if not (30 <= temp2 <= 40):
            st.warning(f"⚠️ Temperatur prüfen! Aktuell: {temp2} °C (Soll: 30 - 40 °C).")

    # --- BECKEN 3: VE-SPÜLE 1 ---
    with tab3:
        st.subheader("Becken 3: VE-Spüle 1 (Max. 1.000 Liter)")
        lw3 = st.number_input("Leitwert (Ziel: max. 250 µS/cm):", min_value=0, max_value=2000, value=150, key="lw3")
        temp3 = st.number_input("Temperatur (Ziel: max. 30 °C):", min_value=0, max_value=100, value=22, key="temp3")
        
        st.markdown("### 📋 Handlungsanweisung:")
        if lw3 > 250:
            st.error(f"❌ Leitwert zu hoch ({lw3} µS/cm)! VE-Wasserqualität ungenügend. Kreislauf / Patrone prüfen!")
        else:
            st.success("✅ Erste VE-Spüle läuft sauber.")

    # --- BECKEN 4: PASSIVIERUNG (eska phor P 355-2) ---
    with tab4:
        st.subheader("Becken 4: Passivierung (Max. 1.000 Liter)")
        st.caption("Eingesetzte Chemie: eska phor P 355-2 (Dünnschichtpassivierung)")
        
        fs4 = st.slider("Aktueller Füllstand (in %):", min_value=50, max_value=100, value=70, step=1, key="fs4")
        v_eff4 = 1000 * (fs4 / 100.0)
        st.info(f"Berechnetes aktuelles Passivierungsvolumen: {int(v_eff4)} Liter")
        
        ph4 = st.number_input("pH-Wert (Ziel: 4.5 - 5.0):", min_value=0.0, max_value=14.0, value=4.7, step=0.1, key="ph4")
        lw4 = st.number_input("Leitwert (Ziel: max. 500 µS/cm):", min_value=0, max_value=5000, value=350, key="lw4")
        temp4 = st.number_input("Temperatur (Ziel: max. 30 °C):", min_value=0, max_value=100, value=22, key="temp4")
        
        st.markdown("**Laboranalyse (Titration):**")
        ml4 = st.number_input("Verbrauch Titrierlösung Passivierung in ml:", min_value=0.0, max_value=50.0, value=4.4, step=0.1, key="ml4")
        
        titrations_faktor_passivierung = 0.05 
        ist_konz4 = ml4 * titrations_faktor_passivierung
        soll_min4 = 0.15
        soll_max4 = 0.30
        soll_ziel4 = 0.225
        
        st.markdown("### 📋 Handlungsanweisung:")
        if not (4.5 <= ph4 <= 5.0):
            st.error(f"❌ pH-Wert außerhalb! Aktuell: {ph4} (Soll: 4.5 - 5.0). Korrekturchemie erforderlich!")
        if lw4 > 500:
            st.error(f"❌ Leitwert zu hoch ({lw4} µS/cm)! Salzfracht in der Passivierung beeinträchtigt die Schicht.")
        if temp4 > 30:
            st.warning(f"⚠️ Bad-Temperatur zu hoch! Aktuell: {temp4} °C (Soll: max. 30 °C).")
            
        st.metric(label="Aktuelle Konzentration Passivierung", value=f"{round(ist_konz4, 3)} %", delta=f"{round(ist_konz4 - soll_ziel4, 3)} % (Ziel: 0.15 - 0.30%)")
        
        if ist_konz4 < soll_min4:
            fehlende_prozent4 = soll_ziel4 - ist_konz4
            chemie_faktor4 = 10.0 
            bedarf_kg4 = (fehlende_prozent4 * (v_eff4 / 1000.0)) * chemie_faktor4
            bedarf_liter4 = bedarf_kg4 / 1.09
            
            st.error(f"❌ KONZENTRATION ZU GERING! Bitte exakt nachdosieren:")
            st.markdown(f"### ⚖️ **{round(bedarf_kg4, 2)} kg** oder 🧪 **{round(bedarf_liter4, 2)} Liter** eska phor P 355-2 hinzugeben.")
            
            st.warning("""
            **⚠️ VORGESCHRIEBENE PSA (Laut Sicherheitsdatenblatt eska phor P 355-2):**
            * Signalwort: **GEFAHR** (Enthält Triethanolammoniumhexafluorozirconat. Verursacht schwere Augenschäden & Hautreizungen) [cite: 478, 479, 485, 487]
            * Schutzbrille: **Gestellbrille mit Seitenschutz** zwingend erforderlich! [cite: 609]
            * Handschutz: **Fluorkautschuk (FKM, 0.7 mm)** oder **Polychloropren (CR, 0.65 mm)**! [cite: 615, 616, 617]
            * Körperschutz: Flüssigkeitsdichte **Schürze** anlegen! [cite: 622]
            """)
        elif ist_konz4 > soll_max4:
            st.warning("⚠️ Konzentration der Passivierung zu hoch! Gefahr von Haftungsproblemen unter dem Pulverlack. Dosierpumpe drosseln.")
        else:
            st.success("🎯 Passivierungsbad läuft stabil im optimalen Bereich.")

    # --- BECKEN 5: VE-SPÜLE 2 ---
    with tab5:
        st.subheader("Becken 5: VE-Spüle 2 (Letzte Spüle vor dem Trockner)")
        lw5 = st.number_input("Leitwert (Ziel: max. 50 µS/cm):", min_value=0, max_value=500, value=15, key="lw5")
        temp5 = st.number_input("Temperatur (Ziel: max. 30 °C):", min_value=0, max_value=100, value=21, key="temp5")
        
        st.markdown("### 📋 Handlungsanweisung:")
        if lw5 > 50:
            st.error(f"🚨 KRITISCH! Leitwert viel zu hoch ({lw5} µS/cm)! Gefahr von Salzflecken unter der Pulverschicht! Sofort Mischbett-Harz wechseln / VE-Anlage prüfen!")
        else:
            st.success("🎯 Perfekt! Leitwert ist optimal. Keine Salzflecken auf der Ware zu befürchten.")

else:
    st.info("💡 Bitte hake zuerst alle Punkte des Morgen-Check-ups ab, um die Beckenanalyse freizuschalten.")
