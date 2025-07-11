import os
import fitz  # PyMuPDF

pdf_folder = "donnees"
output_folder = "images"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)  # first page
            pix = page.get_pixmap()
            
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_page1.png")
            pix.save(output_path)
            
            print(f"Saved: {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
