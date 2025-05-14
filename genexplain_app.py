
import streamlit as st
import pandas as pd

# Sample ClinVar-like database
clinvar_db = {
    "BRCA1 c.68_69delAG": {
        "condition": "Hereditary breast and ovarian cancer syndrome",
        "clinical_significance": "Pathogenic",
        "recommendation": "Refer patient for genetic counseling and consider preventive surgery."
    },
    "TP53 c.743G>A": {
        "condition": "Li-Fraumeni syndrome",
        "clinical_significance": "Likely pathogenic",
        "recommendation": "Enhanced cancer screening is recommended."
    }
}

# Function to interpret genomic variants
def explain_variant(variant):
    if variant in clinvar_db:
        data = clinvar_db[variant]
        return {
            "condition": data["condition"],
            "clinical_significance": data["clinical_significance"],
            "recommendation": data["recommendation"]
        }
    else:
        return {
            "condition": "Not found in database",
            "clinical_significance": "Unknown",
            "recommendation": f"The variant ({variant}) may affect gene function. Consult a genetic specialist for further interpretation."
        }

# Function to extract variants from VCF-formatted text
def extract_variants(text):
    variant_lines = []
    for line in text.splitlines():
        if line.startswith("#") or line.strip() == "":
            continue
        columns = line.strip().split("\t")
        if len(columns) >= 5:
            chrom, pos, _, ref, alt = columns[:5]
            variant_id = f"{chrom}:{pos} {ref}>{alt}"
            variant_lines.append(variant_id)
    return variant_lines if variant_lines else [text.strip()]

# Streamlit UI layout
st.set_page_config(page_title="GenExplain AI", layout="wide")
st.title("GenExplain AI – Universal Genomic Variant Interpreter")

with st.expander("About GenExplain"):
    st.markdown("""
    **GenExplain AI** provides instant interpretations of gene variants based on known databases
    and general genomic knowledge. You can paste gene variant names or upload a VCF file for AI-powered interpretation.
    """)

col1, col2 = st.columns(2)
with col1:
    input_text = st.text_area("Paste gene variant or VCF content here", height=150)
with col2:
    uploaded_file = st.file_uploader("Or upload a VCF file", type=["vcf", "txt"])

if st.button("Interpret Now"):
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
    elif input_text.strip():
        content = input_text
    else:
        st.warning("Please provide a variant input or upload a file.")
        st.stop()

    st.markdown("### Interpretation Results")
    variants = extract_variants(content)
    for var in variants:
        result = explain_variant(var)
        st.subheader(f"Variant: {var}")
        st.write(f"**Condition**: {result['condition']}")
        st.write(f"**Clinical Significance**: {result['clinical_significance']}")
        st.info(f"**Recommendation**: {result['recommendation']}")
