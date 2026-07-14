# 📦 PackLock

> **"Pack it. Lock it. Share it safely."**

PackLock is a lightweight, secure desktop utility that bundles entire directories into a single compressed archive and encrypts them using military-grade **AES-256 (GCM)** encryption. Perfect for sharing sensitive documents, private images, or entire project folders across public networks without worrying about prying eyes.

---

## ✨ Features

*   **Folder-to-Vault:** PackLock automatically archives your entire directory structure (including nested folders and miscellaneous files) into a single secure file.
*   **Unbreakable Security:** Powered by **AES-256-GCM** encryption and PBKDF2 key derivation—the industry standard for securing top-secret data.
*   **Metadata Hiding:** By archiving your folders before encrypting, PackLock hides all internal filenames, sizes, and file types from attackers.
*   **No Dependency Leakage:** Completely open-source, written in Python, and respects your privacy. No cloud servers, no trackers—your keys never leave your machine.

---

## 🚀 How It Works

```
📂 Your Folder       📦 Zip Archive        🔒 Secure Vault
[Files & Photos]  ➡️  [PackLock Zips It]  ➡️  [AES-256 Encryption]  ➡️  file.vault
```

1. **Pack:** PackLock compresses your folder into a temporary zip archive.
2. **Lock:** It generates a cryptographically secure key from your password, encrypts the zip archive, and packages it as a `.vault` file.
3. **Share:** Send the `.vault` file to anyone. They only need PackLock and your password to unlock it.

---

## 🖥️ Platform Support

PackLock is written in pure Python and runs on both **Windows** and **Linux** (as well as macOS).

---

## 🛠️ Quick Start

### Prerequisites
Make sure you have Python 3.8+ installed on your computer.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/abdhamza/PackLock.git
   cd PackLock
   ```
2. Install PackLock (editable install, exposes the `packlock` command):
   ```bash
   pip install -e .
   ```

### Usage

**Lock a folder:**
```bash
packlock lock /path/to/your/folder
```
You'll be prompted for a password (twice, to confirm). PackLock produces a `folder.vault` file next to the original folder.

**Unlock a vault:**
```bash
packlock unlock folder.vault
```
Enter the same password to restore the original folder contents into `folder/`.

Use `-o/--output` on either command to choose a custom output path.

---

## 🧑‍💻 Development

Clone the repo and install it in editable mode with the test dependencies:
```bash
pip install -e ".[dev]"
```

Run the test suite:
```bash
pytest -v
```

---

## 📄 License

PackLock is licensed under the [GNU General Public License v3.0](LICENSE).