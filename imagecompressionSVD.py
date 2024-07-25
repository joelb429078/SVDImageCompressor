import tkinter as tk
from tkinter import filedialog, Scale
from PIL import Image, ImageTk
import numpy as np
from skimage import io
import os

class ImageCompressorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Compressor")
        self.geometry("691x401")
        self.configure(bg="#FFFFFF")
        
        self.frame1 = Frame1(self)
        self.frame2 = Frame2(self)
        
        self.show_frame1()

    def show_frame1(self):
        self.frame2.pack_forget()
        self.frame1.pack(fill=tk.BOTH, expand=True)

    def show_frame2(self):
        self.frame1.pack_forget()
        self.frame2.pack(fill=tk.BOTH, expand=True)
        self.frame2.show_images()

class Frame1(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="#FFFFFF", height=401, width=691, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_text(95, 49, anchor="nw", text="Image compressor:", fill="#000000", font=("Inter Bold", 28))
        self.canvas.create_text(135, 148, anchor="nw", text="Upload an image to compress, then select compression ratio", fill="#000000", font=("Inter", 14))

        self.canvas.create_rectangle(250, 180, 450, 280, outline="#000000", fill="#D9D9D9", width=2, dash=(5, 2))

        icon_path = os.path.join("assets", "download.png")
        if os.path.exists(icon_path):
            self.upload_icon = Image.open(icon_path)
            self.upload_icon = self.upload_icon.resize((35, 35), Image.LANCZOS)
            self.upload_icon = ImageTk.PhotoImage(self.upload_icon)
            self.canvas.create_image(350, 230, image=self.upload_icon)
        else:
            print(f"Warning: Icon file not found at {icon_path}")

        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image, bg="#D9D9D9", relief="flat")
        self.upload_button.place(x=250, y=180, width=200, height=100)

        self.k_slider = Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, label="Compression Ratio", bg="#FFFFFF", highlightthickness=0)
        self.k_slider.place(x=150, y=290, width=400)

        self.compress_button = tk.Button(self, text="Compress", command=self.compress_image, bg="#4CAF50", fg="#FFFFFF", font=("Inter Bold", 14), relief="flat")
        self.compress_button.place(x=300, y=350, width=100)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if self.image_path:
            self.master.original_image = io.imread(self.image_path, as_gray=True)
            if self.master.original_image.max() > 1.0:
                self.master.original_image = self.master.original_image / 255.0
            print(f"Image uploaded: {self.image_path}") 

    def compress_image(self):
        if hasattr(self.master, 'original_image'):
            k = self.k_slider.get()
            compressed_image = compression(self.master.original_image, k)
            self.master.compressed_image = compressed_image
            self.master.show_frame2()
        else:
            print("No image uploaded yet") 

class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="#FFFFFF", height=401, width=691, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_text(78, 46, anchor="nw", text="Image compressor:", fill="#000000", font=("Inter Bold", 24))
        self.canvas.create_text(136, 100, anchor="nw", text="Here is the before and after of your image, ready for download!", fill="#000000", font=("Inter", 14))

        self.before_image_label = tk.Label(self, bg="#D9D9D9")
        self.before_image_label.place(x=120, y=150, width=200, height=150)
        
        self.after_image_label = tk.Label(self, bg="#D9D9D9")
        self.after_image_label.place(x=370, y=150, width=200, height=150)

        self.download_button = tk.Button(self, text="Download", command=self.download_image, bg="#4CAF50", fg="#FFFFFF", font=("Inter Bold", 14), relief="flat")
        self.download_button.place(x=300, y=350, width=100)

        self.back_button = tk.Button(self, text="Back", command=self.master.show_frame1, bg="#D9D9D9", font=("Inter", 12), relief="flat")
        self.back_button.place(x=50, y=350, width=60)

    def show_images(self):
        if hasattr(self.master, 'original_image') and hasattr(self.master, 'compressed_image'):
            original_image = Image.fromarray((self.master.original_image * 255).astype(np.uint8))
            compressed_image = Image.fromarray((self.master.compressed_image * 255).astype(np.uint8))

            original_photo = ImageTk.PhotoImage(original_image.resize((200, 150)))
            compressed_photo = ImageTk.PhotoImage(compressed_image.resize((200, 150)))

            self.before_image_label.config(image=original_photo)
            self.before_image_label.image = original_photo
            self.after_image_label.config(image=compressed_photo)
            self.after_image_label.image = compressed_photo
        else:
            print("Images not available")

    def download_image(self):
        if hasattr(self.master, 'compressed_image'):
            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            if save_path:
                compressed_image = Image.fromarray((self.master.compressed_image * 255).astype(np.uint8))
                compressed_image.save(save_path)
                print(f"Image saved to {save_path}")
        else:
            print("No compressed image available") 

def compression(image, k):
    U, S, VT = np.linalg.svd(image, full_matrices=False)
    S_k = np.zeros((k, k))
    np.fill_diagonal(S_k, S[:k])
    U_k = U[:, :k]
    VT_k = VT[:k, :]
    compressed_image = np.dot(U_k, np.dot(S_k, VT_k))
    return np.clip(compressed_image, 0, 1)

if __name__ == "__main__":
    app = ImageCompressorApp()
    app.mainloop()