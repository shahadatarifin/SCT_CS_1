import os
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox


class ImageEncryptor:
    def __init__(self, image_path=None):
        self.image_path = image_path
        if image_path:
            self.image = Image.open(image_path)
            self.pixels = np.array(self.image)
            self.original_shape = self.pixels.shape
        else:
            self.image = None
            self.pixels = None

    def load_image(self, image_path):
        """Load an image from a file path."""
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.pixels = np.array(self.image)
        self.original_shape = self.pixels.shape

    def save_image(self, output_path):
        """Save the modified image to a file."""
        if self.pixels is not None:
            encrypted_img = Image.fromarray(self.pixels)
            encrypted_img.save(output_path)
            return True
        return False

    def swap_channels(self):
        """Swap RGB channels (BGR instead of RGB)."""
        if len(self.pixels.shape) == 3:  # Only for color images
            self.pixels = self.pixels[:, :, [2, 1, 0]]  # BGR instead of RGB

    def apply_xor(self, key=123):
        """Apply XOR operation on each pixel with a key."""
        self.pixels = np.bitwise_xor(self.pixels, key)

    def apply_addition(self, value=50):
        """Add a value to each pixel (with modulo 256 to prevent overflow)."""
        self.pixels = (self.pixels + value) % 256

    def apply_multiplication(self, factor=2):
        """Multiply each pixel by a factor (with modulo 256)."""
        self.pixels = (self.pixels * factor) % 256

    def shuffle_rows(self, seed=None):
        """Randomly shuffle rows of the image (reversible if seed is fixed)."""
        if seed is not None:
            np.random.seed(seed)
            np.random.shuffle(self.pixels)

    def shuffle_columns(self, seed=None):
        """Randomly shuffle columns of the image (reversible if seed is fixed)."""
        if seed is not None:
            np.random.seed(seed)
            self.pixels = np.random.permutation(self.pixels.T).T

    def encrypt(self, operations, output_path):
        """Apply a sequence of encryption operations."""
        for op in operations:
            if op['name'] == 'swap':
                self.swap_channels()
            elif op['name'] == 'xor':
                self.apply_xor(op.get('key', 123))
            elif op['name'] == 'add':
                self.apply_addition(op.get('value', 50))
            elif op['name'] == 'multiply':
                self.apply_multiplication(op.get('factor', 2))
            elif op['name'] == 'shuffle_rows':
                self.shuffle_rows(op.get('seed', None))
            elif op['name'] == 'shuffle_cols':
                self.shuffle_columns(op.get('seed', None))
        self.save_image(output_path)

    def decrypt(self, operations, output_path):
        """Reverse the encryption operations in reverse order."""
        for op in reversed(operations):
            if op['name'] == 'swap':
                self.swap_channels()  # Swap again to reverse
            elif op['name'] == 'xor':
                self.apply_xor(op.get('key', 123))  # XOR is reversible
            elif op['name'] == 'add':
                self.apply_addition(-op.get('value', 50))  # Subtract to reverse
            elif op['name'] == 'multiply':
                # To reverse multiplication, modular inverse is complex
                # Here, simply dividing (not always accurate)
                inv_factor = 1 / op.get('factor', 2)
                self.pixels = (self.pixels * inv_factor).astype(np.uint8)
            elif op['name'] == 'shuffle_rows':
                self.shuffle_rows(op.get('seed', None))  # Same seed = same shuffle
            elif op['name'] == 'shuffle_cols':
                self.shuffle_columns(op.get('seed', None))
        self.save_image(output_path)

# ==================== GUI Application ====================
class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")
        self.encryptor = None

        # === SET YOUR DEFAULT IMAGE PATH HERE ===
        default_path = "/Users/apple/Desktop/SI_project_vscode/photo1.png"
        if os.path.exists(default_path):
            try:
                self.encryptor = ImageEncryptor(default_path)
                status_text = f"Auto-loaded: {default_path}"
            except Exception as e:
                status_text = f"Failed to load default image: {e}"
        else:
            status_text = "No image loaded"

        # GUI Elements
        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        self.encrypt_button = tk.Button(root, text="Encrypt Image", command=self.encrypt_image)
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = tk.Button(root, text="Decrypt Image", command=self.decrypt_image)
        self.decrypt_button.pack(pady=5)

        self.status_label = tk.Label(root, text=status_text)
        self.status_label.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                self.encryptor = ImageEncryptor(file_path)
                self.status_label.config(text=f"Loaded: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{e}")

    def encrypt_image(self):
        if not self.encryptor:
            messagebox.showerror("Error", "No image loaded!")
            return

        operations = [
            {'name': 'swap'},
            {'name': 'xor', 'key': 42},
            {'name': 'shuffle_rows', 'seed': 1234}
        ]

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if output_path:
            self.encryptor.encrypt(operations, output_path)
            messagebox.showinfo("Success", f"Image encrypted and saved to:\n{output_path}")

    def decrypt_image(self):
        if not self.encryptor:
            messagebox.showerror("Error", "No image loaded!")
            return

        operations = [
            {'name': 'swap'},
            {'name': 'xor', 'key': 42},
            {'name': 'shuffle_rows', 'seed': 1234}
        ]

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if output_path:
            self.encryptor.decrypt(operations, output_path)
            messagebox.showinfo("Success", f"Image decrypted and saved to:\n{output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
