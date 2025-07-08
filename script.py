import pandas as pd
import streamlit as st
import io
import zipfile
import re

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name.strip().replace(" ", "_"))

def convert_to_vcf(row):
    vcf = "BEGIN:VCARD\nVERSION:3.0\n"
    if pd.notna(row['Nom Complet']):
        vcf += f"N:{row['Nom Complet']}\nFN:{row['Nom Complet']}\n"
    if pd.notna(row['Entreprise']):
        vcf += f"ORG:{row['Entreprise']}\n"
    if pd.notna(row['Poste']):
        vcf += f"TITLE:{row['Poste']}\n"
    if pd.notna(row['Téléphone']):
        vcf += f"TEL;TYPE=WORK:{row['Téléphone']}\n"
    if pd.notna(row['Téléphone cellulaire']):
        vcf += f"TEL;TYPE=CELL:{row['Téléphone cellulaire']}\n"
    if pd.notna(row['E-mail']):
        vcf += f"EMAIL;TYPE=INTERNET:{row['E-mail']}\n"
    if pd.notna(row['Adresse']):
        vcf += f"ADR;TYPE=WORK:;;{row['Adresse']};;;;\n"
    if pd.notna(row['Site']):
        vcf += f"URL:{row['Site']}\n"
    if pd.notna(row['Facebook']):
        vcf += f"URL;TYPE=Facebook:{row['Facebook']}\n"
    if pd.notna(row['Instagram']):
        vcf += f"URL;TYPE=Instagram:{row['Instagram']}\n"
    if pd.notna(row['Linkedin']):
        vcf += f"URL;TYPE=LinkedIn:{row['Linkedin']}\n"
    vcf += "END:VCARD\n"
    return vcf

def main():
    st.title("📇 Convertisseur CSV → VCF")

    uploaded_file = st.file_uploader("📤 Téléversez un fichier CSV (séparé par `;`)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file, sep=";")
        st.subheader("🧾 Aperçu des données")
        st.dataframe(df)

        # Create ZIP of individual VCF files
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for _, row in df.iterrows():
                full_name = row.get("Nom Complet", "contact")
                filename = sanitize_filename(full_name) or "contact"
                vcf_content = convert_to_vcf(row)
                zipf.writestr(f"{filename}.vcf", vcf_content)

        st.download_button(
            label="📦 Télécharger tous les fichiers VCF (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="contacts_vcf.zip",
            mime="application/zip"
        )

        st.markdown("---")
        st.subheader("📥 Téléchargements individuels")

        for _, row in df.iterrows():
            full_name = row.get("Nom Complet", "contact")
            filename = sanitize_filename(full_name) or "contact"
            vcf_content = convert_to_vcf(row)
            vcf_bytes = vcf_content.encode('utf-8')

            st.download_button(
                label=f"📇 Télécharger {full_name}.vcf",
                data=vcf_bytes,
                file_name=f"{filename}.vcf",
                mime="text/vcard"
            )

if __name__ == "__main__":
    main()
