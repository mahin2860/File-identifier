# 📚 SSC & HSC Question Paper Organizer

A professional system to organize large collections of education question papers. It scans filenames, identifies the education level (SSC/HSC) and subject, and automatically moves them into a structured folder system.

**Developed by Erfan Noor Mahin**

## 🚀 Quick Start

1.  **Prepare your files**:
    *   Go to the `input` folder.
    *   Place all your question papers (individual files) or a **single ZIP archive** inside the `input` folder.
2.  **Run the organizer**:
    *   Open your terminal/PowerShell.
    *   Run the following command:
      ```powershell
      cd "SSC_HSC_Organizer"
      python organize.py
      ```
3.  **Get your results**:
    *   Your organized files will appear in the `output` folder.
    *   Check `output/report.csv` to see exactly where each file was placed.

---

## 🛠 How it Works

The system uses a **Keyword-Based Identifier**. It looks for specific short-codes in the filenames to ensure accuracy:

| Subject | Keyword | Example Filename |
| :--- | :--- | :--- |
| **Bangla** | `ban` | `SSC_ban_2024.pdf` |
| **English** | `eng` | `HSC_eng_1st_2023.pdf` |
| **Math** | `math` | `SSC_math_dhaka.pdf` |
| **Higher Math**| `hmath` | `HSC_hmath_2nd.pdf` |
| **Biology** | `bio` | `SSC_bio_2024.pdf` |

### Folder Structure Generated:
- `output/SSC/[Subject Name]/`
- `output/HSC/[Subject Name]/`
- `output/_Uncategorized/` (Files with no detectable subject)
- `output/_Review_Required/` (Files with no detectable SSC/HSC level)

---

## ⚙️ Customization

If you want to use folders outside of the `input/output` directories:
1. Open `organize.py` in a text editor.
2. Find the bottom section and change the paths:
   ```python
   INPUT = r"C:\Your\Custom\Input\Path"
   OUTPUT = r"C:\Your\Custom\Output\Path"
   ```

## 📋 Requirements
- **Python 3.x** installed on your system.

## ⚠️ Troubleshooting
- **File went to _Review_Required?**: The filename is missing "SSC" or "HSC". Rename the file to include the level and run again.
- **File went to _Uncategorized?**: The filename doesn't contain any recognized subject keywords (like `ban`, `eng`, `bio`).
