"""
ESC - Urlaubsplan Transformation Tool
======================================
Streamlit-App zur Transformation von Urlaubsplandaten aus Excel
in konsolidierte CSV-Formate mit zusammenhängenden Abwesenheitsblöcken.

Autor: Pete (E+SERVICE+CHECK Marketing)
Erstellt: Januar 2026
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import re
import io

# ============================================================================
# SEITENKONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Urlaubsplan Transformation",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# HILFSFUNKTIONEN
# ============================================================================

def extract_year_from_sheetname(sheet_name):
    """
    Extrahiert das Jahr aus dem Tabellenblatt-Namen.
    Beispiele:
    - "Januar" → 2026 (Standard)
    - "Januar 2027" → 2027
    """
    year_match = re.search(r'\b(20\d{2})\b', sheet_name)
    if year_match:
        return int(year_match.group(1))
    else:
        return 2026  # Standardjahr


def consolidate_absences(data_list):
    """
    Gruppiert zusammenhängende Abwesenheiten desselben Typs für jeden Mitarbeiter.
    
    Beispiel:
    Input:  1418,K,27.1.2026,27.1.2026
            1418,K,28.1.2026,28.1.2026
            1418,K,29.1.2026,29.1.2026
    Output: 1418,K,27.1.2026,29.1.2026
    """
    if not data_list:
        return []
    
    df = pd.DataFrame(data_list)
    df['Start_dt'] = pd.to_datetime(df['Start'], format='%d.%m.%Y')
    df['Ende_dt'] = pd.to_datetime(df['Ende'], format='%d.%m.%Y')
    df = df.sort_values(['Pers_Nr', 'Abwesenheitsart', 'Start_dt']).reset_index(drop=True)
    
    consolidated = []
    
    for (pers_nr, abw_art), group in df.groupby(['Pers_Nr', 'Abwesenheitsart'], sort=False):
        group = group.sort_values('Start_dt').reset_index(drop=True)
        
        if len(group) == 0:
            continue
        
        block_start = group.iloc[0]['Start_dt']
        block_end = group.iloc[0]['Ende_dt']
        
        for i in range(1, len(group)):
            current_date = group.iloc[i]['Start_dt']
            
            if (current_date - block_end).days == 1:
                block_end = group.iloc[i]['Ende_dt']
            else:
                consolidated.append({
                    'Pers_Nr': pers_nr,
                    'Abwesenheitsart': abw_art,
                    'Start': f"{block_start.day}.{block_start.month}.{block_start.year}",
                    'Ende': f"{block_end.day}.{block_end.month}.{block_end.year}"
                })
                block_start = current_date
                block_end = group.iloc[i]['Ende_dt']
        
        consolidated.append({
            'Pers_Nr': pers_nr,
            'Abwesenheitsart': abw_art,
            'Start': f"{block_start.day}.{block_start.month}.{block_start.year}",
            'Ende': f"{block_end.day}.{block_end.month}.{block_end.year}"
        })
    
    return consolidated


def process_excel_file(uploaded_file):
    """
    Verarbeitet die hochgeladene Excel-Datei und gibt das transformierte DataFrame zurück.
    """
    xl_file = pd.ExcelFile(uploaded_file)
    
    result_data = []
    processing_info = {
        'sheets': [],
        'total_days': 0,
        'total_blocks': 0
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_sheets = len(xl_file.sheet_names)
    
    for idx, sheet_name in enumerate(xl_file.sheet_names):
        status_text.text(f"Verarbeite Tabellenblatt {idx + 1}/{total_sheets}: {sheet_name}")
        progress_bar.progress((idx + 1) / total_sheets)
        
        year = extract_year_from_sheetname(sheet_name)
        
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=None)
        date_row = df.iloc[0, :]
        
        # Suche erste Spalte mit Datum
        first_date_col = None
        for col_idx in range(2, len(df.columns)):
            if pd.notna(date_row.iloc[col_idx]):
                if isinstance(date_row.iloc[col_idx], (pd.Timestamp, datetime)):
                    first_date_col = col_idx
                    break
        
        if first_date_col is None:
            processing_info['sheets'].append({
                'name': sheet_name,
                'entries': 0,
                'status': 'Keine Datumsangaben gefunden'
            })
            continue
        
        entries_in_sheet = 0
        
        # Verarbeite alle Mitarbeiterzeilen
        for row_idx in range(1, len(df)):
            pers_nr = df.iloc[row_idx, 0]
            
            if pd.isna(pers_nr):
                continue
            
            try:
                pers_nr = int(pers_nr)
            except:
                continue
            
            for col_idx in range(first_date_col, len(df.columns)):
                abwesenheitsart = df.iloc[row_idx, col_idx]
                
                if pd.notna(abwesenheitsart):
                    datum = date_row.iloc[col_idx]
                    
                    if pd.notna(datum) and isinstance(datum, (pd.Timestamp, datetime)):
                        datum_str = f"{datum.day}.{datum.month}.{datum.year}"
                        
                        result_data.append({
                            'Pers_Nr': pers_nr,
                            'Abwesenheitsart': abwesenheitsart,
                            'Start': datum_str,
                            'Ende': datum_str
                        })
                        entries_in_sheet += 1
        
        processing_info['sheets'].append({
            'name': sheet_name,
            'entries': entries_in_sheet,
            'status': 'Erfolgreich'
        })
        processing_info['total_days'] += entries_in_sheet
    
    status_text.text("Konsolidiere zusammenhängende Abwesenheitsblöcke...")
    
    # Konsolidierung
    result_data = consolidate_absences(result_data)
    processing_info['total_blocks'] = len(result_data)
    
    # DataFrame erstellen
    result_df = pd.DataFrame(result_data)
    if len(result_df) > 0:
        result_df = result_df[['Pers_Nr', 'Abwesenheitsart', 'Start', 'Ende']]
        result_df = result_df.sort_values(['Pers_Nr', 'Start']).reset_index(drop=True)
    
    progress_bar.empty()
    status_text.empty()
    
    return result_df, processing_info


# ============================================================================
# HAUPTANWENDUNG
# ============================================================================

def main():
    # Header
    st.title("📅 Urlaubsplan Transformation")
    st.markdown("""
    Diese Anwendung transformiert Excel-Urlaubspläne mit monatlichen Tabellenblättern 
    in ein strukturiertes CSV-Format mit konsolidierten Abwesenheitsblöcken.
    """)
    
    # Sidebar - Informationen
    with st.sidebar:
        st.header("ℹ️ Anleitung")
        st.markdown("""
        **Schritt 1:** Excel-Datei hochladen
        
        **Schritt 2:** Vorschau prüfen
        
        **Schritt 3:** CSV-Datei herunterladen
        
        ---
        
        **Erwartetes Format:**
        - Mehrere Tabellenblätter (Monate)
        - Zeile 1: Datumsangaben
        - Spalte A: Personalnummer
        - Spalte B: Name (optional)
        - Ab Spalte C: Abwesenheiten
        
        ---
        
        **Features:**
        - ✅ Konsolidierung zusammenhängender Abwesenheiten
        - ✅ Deutsches Datumsformat (Tag.Monat.Jahr)
        - ✅ Automatische Jahr-Erkennung
        - ✅ Verarbeitung mehrerer Monate
        """)
        
        st.header("📊 Statistiken")
        if 'processing_info' in st.session_state:
            info = st.session_state.processing_info
            st.metric("Verarbeitete Tabellenblätter", len(info['sheets']))
            st.metric("Einzeltage (Input)", f"{info['total_days']:,}")
            st.metric("Konsolidierte Blöcke (Output)", f"{info['total_blocks']:,}")
            if info['total_days'] > 0:
                reduction = (1 - info['total_blocks'] / info['total_days']) * 100
                st.metric("Reduzierung", f"{reduction:.1f}%")
    
    # Datei-Upload
    uploaded_file = st.file_uploader(
        "Excel-Datei auswählen",
        type=['xlsx', 'xls'],
        help="Wähle eine Excel-Datei mit Urlaubsplan-Daten"
    )
    
    if uploaded_file is not None:
        try:
            # Verarbeite die Datei
            with st.spinner('Verarbeite Excel-Datei...'):
                result_df, processing_info = process_excel_file(uploaded_file)
                st.session_state.result_df = result_df
                st.session_state.processing_info = processing_info
            
            st.success(f"✅ Verarbeitung erfolgreich! {len(result_df)} Abwesenheitsblöcke erstellt.")
            
            # Tabs für verschiedene Ansichten
            tab1, tab2, tab3 = st.tabs(["📋 Vorschau", "📈 Statistiken", "📄 Verarbeitungsdetails"])
            
            with tab1:
                st.subheader("Vorschau der transformierten Daten")
                
                # Anzahl der anzuzeigenden Zeilen
                col1, col2 = st.columns([3, 1])
                with col2:
                    n_rows = st.selectbox("Anzahl Zeilen", [10, 25, 50, 100, "Alle"], index=0)
                
                if n_rows == "Alle":
                    st.dataframe(result_df, use_container_width=True, height=600)
                else:
                    st.dataframe(result_df.head(n_rows), use_container_width=True)
                
                st.caption(f"Gesamt: {len(result_df)} Zeilen")
            
            with tab2:
                st.subheader("Statistische Auswertung")
                
                # Metriken in Spalten
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Anzahl Mitarbeiter", result_df['Pers_Nr'].nunique())
                
                with col2:
                    multiday = result_df[result_df['Start'] != result_df['Ende']]
                    st.metric("Mehrtägige Blöcke", f"{len(multiday)} ({len(multiday)/len(result_df)*100:.1f}%)")
                
                with col3:
                    singleday = len(result_df) - len(multiday)
                    st.metric("Einzeltage", f"{singleday} ({singleday/len(result_df)*100:.1f}%)")
                
                # Abwesenheitsarten
                st.subheader("Verteilung der Abwesenheitsarten")
                absence_counts = result_df['Abwesenheitsart'].value_counts()
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.bar_chart(absence_counts)
                
                with col2:
                    st.dataframe(
                        absence_counts.reset_index().rename(
                            columns={'index': 'Abwesenheitsart', 'Abwesenheitsart': 'Anzahl'}
                        ),
                        use_container_width=True,
                        height=400
                    )
            
            with tab3:
                st.subheader("Verarbeitungsdetails")
                
                sheets_df = pd.DataFrame(processing_info['sheets'])
                st.dataframe(sheets_df, use_container_width=True)
            
            # Download-Button
            st.markdown("---")
            st.subheader("💾 Download")
            
            # CSV erstellen
            csv_buffer = io.StringIO()
            result_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
            csv_data = csv_buffer.getvalue()
            
            # Dateiname mit Zeitstempel
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'urlaubsplan_consolidated_{timestamp}.csv'
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 CSV-Datei herunterladen",
                    data=csv_data,
                    file_name=filename,
                    mime='text/csv',
                    use_container_width=True
                )
        
        except Exception as e:
            st.error(f"❌ Fehler beim Verarbeiten der Datei: {str(e)}")
            st.exception(e)
    
    else:
        # Platzhalter wenn keine Datei hochgeladen
        st.info("👆 Bitte laden Sie eine Excel-Datei hoch, um zu beginnen.")
        
        # Beispiel-Datenstruktur anzeigen
        with st.expander("📖 Beispiel-Datenstruktur"):
            st.markdown("""
            **Erwartete Excel-Struktur:**
            
            | Spalte A | Spalte B | Spalte C | Spalte D | Spalte E | ... |
            |----------|----------|----------|----------|----------|-----|
            | Heute ist | | 1.1.2026 | 2.1.2026 | 3.1.2026 | ... |
            | 3 | Becker, Matthias | U | | K | ... |
            | 35 | Korb, Thomas | | U | U | ... |
            | 80 | Piur, Thomas | K | K | | ... |
            
            **Abwesenheitsarten:**
            - U = Urlaub
            - K = Krank
            - KG = Krankengeld
            - EZ = Elternzeit
            - Ü = Überstunden
            - etc.
            """)
    
    # Footer
    st.markdown("---")
    st.caption("Entwickelt für E+SERVICE+CHECK GmbH | Januar 2026")


if __name__ == "__main__":
    main()
