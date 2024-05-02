import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
from pathlib import Path
import re


def extract_companies(file_path):
    
    reader = PdfReader(file_path)
    companies = {}
    current_compamy = None
    output_dir = Path(file_path).parent / "Split_PDF_files"
    output_dir.mkdir(exist_ok=True)

    for num, page in enumerate(reader.pages):
        text = page.extract_text()
        pattern = re.search(r'[^0-9]+\s(?:[A-Za-z]+\s)*[dD]\.[oO]\.[oO]\.', text)
        if pattern:
            company_name = pattern.group(0).strip()
            company_name = re.sub(r'[\\/\*?:"<>|]', '_', company_name)
            if company_name != current_compamy:
                current_compamy = company_name
                if company_name not in companies:
                    companies[company_name] = PdfWriter()
            companies[company_name].add_page(page)

    for company_name, pages in companies.items():
        output_file = output_dir /f"{company_name}.pdf"
        print("Saving to:", output_file)
        with open(output_file, "wb") as output:
            pages.write(output_file)

def GUI():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        extract_companies(file_path)
        messagebox.showinfo("Pripravljeno", "PDF Datoteka je bila uspešno razdelena.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Split PDF Files")
    root.geometry("300x100")

    label = tk.Label(root, text="Izberi Datoteko")
    label.pack(pady=10)

    button = tk.Button(root, text="Izberi Datoteko", command=GUI)
    button.pack(pady=5)

    root.mainloop()
