import os
from pdf2image import convert_from_path

# Path to your folder
pdf_folder = "donnees"
output_folder = "images"

# Optional: create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all PDFs in the folder
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        try:
            images = convert_from_path(pdf_path, first_page=1, last_page=1)
            # Save the first page as image
            image_name = os.path.splitext(filename)[0] + "_page1.png"
            image_path = os.path.join(output_folder, image_name)
            images[0].save(image_path, "PNG")
            print(f"Saved: {image_path}")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
