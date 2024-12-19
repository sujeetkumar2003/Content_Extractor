import os
from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, messagebox, Frame
from PIL import Image as PILImage
from PyPDF2 import PdfReader
from docx import Document
import pytesseract

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        return f"Error extracting PDF: {e}"

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"Error extracting DOCX: {e}"

def extract_text_from_image(file_path):
    try:
        image = PILImage.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error extracting Image: {e}"

def save_content(content):
    file_path = filedialog.asksaveasfilename(title="Save File", defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Success", "Content saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

def select_file():
    file_path = filedialog.askopenfilename(title="Select a File",
                                           filetypes=[("PDF files", "*.pdf"),
                                                      ("Word Documents", "*.docx"),
                                                      ("Images", "*.jpg;*.jpeg;*.png"),
                                                      ("All files", "*.*")])
    if not file_path:
        messagebox.showinfo("No File Selected", "Please select a file to extract content.")
        return

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == ".pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        extracted_text = extract_text_from_docx(file_path)
    elif file_extension in [".jpg", ".jpeg", ".png"]:
        extracted_text = extract_text_from_image(file_path)
    else:
        messagebox.showerror("Unsupported File Type", "The selected file type is not supported.")
        return

    display_extracted_content(extracted_text)

def display_extracted_content(content):
    for widget in main_frame.winfo_children():
        widget.destroy()

    content_text = Text(main_frame, wrap="word", font=("Arial", 12))
    content_text.insert("1.0", content)
    content_text.configure(state="disabled")
    content_text.pack(expand=True, fill="both", padx=10, pady=10)

    button_frame = Frame(main_frame, bg="white")
    button_frame.pack(fill="x", pady=10, padx=10, anchor="se")

    save_button = Button(button_frame, text="Save Content", command=lambda: save_content(content),
                         font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
    save_button.pack(side="right", padx=5)

    select_button = Button(button_frame, text="Select Another File", command=reset_gui,
                           font=("Arial", 12), bg="#2196F3", fg="white", padx=10, pady=5)
    select_button.pack(side="right", padx=5)

def reset_gui():
    for widget in main_frame.winfo_children():
        widget.destroy()

    header_label = Label(main_frame, text="Content Extractor", font=("Arial", 24, "bold"), bg="white", fg="black")
    header_label.pack(pady=(50, 10))

    description_label = Label(main_frame, text="Convert your PDF, Images, or DOCX files with ease",
                               font=("Arial", 14), bg="white", fg="gray")
    description_label.pack(pady=(10, 30))

    select_button = Button(main_frame, text="Select File", command=select_file, font=("Arial", 16),
                            bg="#ff4d4d", fg="white", padx=20, pady=10, borderwidth=0, relief="flat")
    select_button.pack(pady=(10, 50))

root = Tk()
root.title("Content Extractor")
root.geometry("800x600")
root.configure(bg="white")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_frame = Frame(root, bg="white")
main_frame.grid(row=0, column=0, sticky="nsew")

reset_gui()

root.mainloop()
