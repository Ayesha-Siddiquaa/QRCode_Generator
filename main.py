import tkinter as tk
from tkinter import ttk, filedialog
import qrcode
from PIL import Image, ImageTk
import webbrowser

class QRCodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("QR Code Generator")

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Set theme to "clam" for a modern look
        self.style.configure("TButton", padding=10, relief="flat", background="#4CAF50", foreground="white", font=("Helvetica", 12, "bold"))
        self.style.configure("TLabel", padding=10, font=("Helvetica", 12))
        self.style.configure("TEntry", padding=10, font=("Helvetica", 12))

        self.url_label = ttk.Label(master, text="Enter URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)

        self.url_entry = ttk.Entry(master, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        self.generate_button = ttk.Button(master, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_button.grid(row=0, column=2, padx=10, pady=10)

        self.preview_label = ttk.Label(master)
        self.preview_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.share_button = ttk.Button(master, text="Share", command=self.share_qr_code)
        self.share_button.grid(row=2, column=1, padx=10, pady=10)

        self.error_label = ttk.Label(master, text="", foreground="red")
        self.error_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def generate_qr_code(self):
        url = self.url_entry.get()
        if url:
            self.error_label.config(text="")  # Clear any previous error message
            qr_image = self.create_qr_code(url)
            self.show_preview(qr_image)
        else:
            self.error_label.config(text="URL cannot be empty.")

    def create_qr_code(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        return qr_image

    def show_preview(self, qr_image):
        qr_image = qr_image.resize((200, 200), Image.LANCZOS)  # Use Image.LANCZOS for resizing
        photo = ImageTk.PhotoImage(qr_image)
        self.preview_label.config(image=photo)
        self.preview_label.image = photo

    def share_qr_code(self):
        url = self.url_entry.get()
        if url:
            qr_image = self.create_qr_code(url)
            qr_image.save("temp_qr_code.png")  # Save the QR code image temporarily
            whatsapp_url = "https://web.whatsapp.com/send?text=Check%20out%20this%20QR%20code!&source=data:image/png;base64,"
            webbrowser.open_new_tab(whatsapp_url + "temp_qr_code.png")
        else:
            self.error_label.config(text="URL cannot be empty.")

def main():
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
