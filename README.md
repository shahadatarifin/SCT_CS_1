# SCT_CS_1 – Image Encryption & Decryption Tool

## 🔒 Task Objective

The goal of this task was to build a basic **Image Encryption and Decryption Tool** using Python. This tool should:
- Encrypt an image using multiple transformation techniques.
- Allow the encrypted image to be saved.
- Decrypt the image back to its original form using the reverse sequence of operations.
- Provide a simple GUI interface for user interaction.

---

## 🧠 Approach

To achieve the task objectives, I followed a modular approach:
1. **Image Processing with NumPy & PIL**: The image is read as an array of pixel values.
2. **Encryption Techniques**:
   - **RGB Channel Swapping**: Change RGB to BGR to obfuscate color data.
   - **XOR Operation**: Bitwise XOR for lightweight encryption.
   - **Row and Column Shuffling**: Randomize pixel rows/columns using a seed for reversible encryption.
   - **Addition and Multiplication**: Modify pixel intensity with modulo operations.
3. **Decryption Logic**:
   - Reverse the operations in the **exact opposite order**.
   - For non-invertible operations like multiplication, a simplified inverse is attempted.
4. **GUI with Tkinter**: A minimal interface for loading images, encrypting, and decrypting using user actions.

---

## 🛠 Tools Used

- **Python 3**
- **Tkinter** – GUI interface
- **NumPy** – Numerical array operations on image pixels
- **PIL (Pillow)** – Image handling and manipulation

---

## 📚 What I Learned

Through this task, I gained hands-on experience with:
- **Basic Cryptographic Techniques** for multimedia data.
- **Image Manipulation** using NumPy and PIL.
- **Tkinter GUI Programming**, including file dialogs and message boxes.
- Understanding how simple operations like XOR, pixel shifting, and RGB channel swaps can act as reversible encryption mechanisms.
- Modular coding principles and UI logic separation.

---

## 🚀 How It Works

1. Launch the tool and load an image.
2. Click **Encrypt Image** to perform encryption with defined operations.
3. Save the encrypted image.
4. Click **Decrypt Image** and load the encrypted file to reverse the operations and restore the original image.

---

## 📸 Example Operations Used
```python
operations = [
    {'name': 'swap'},
    {'name': 'xor', 'key': 42},
    {'name': 'shuffle_rows', 'seed': 1234}
]
