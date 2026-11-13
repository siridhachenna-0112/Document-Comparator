# 📄 Offline Document Comparator

An offline desktop-based application designed to compare two documents and identify differences between them. The application helps users analyze document changes by highlighting added, deleted, and modified content, making document verification easier and more efficient.

The application is designed to work locally without requiring an internet connection, ensuring privacy and security while processing documents.

## 🚀 Features

- **Offline Functionality:** Compare documents without an internet connection.
- **Document Comparison:** Select and compare two documents from the local system.
- **Text Difference Detection:** Identify added, deleted, and modified text.
- **Line Number Identification:** Display line numbers to help locate differences easily.
- **DOCX Support:** Compare Microsoft Word documents (`.docx`).
- **TXT Support:** Compare plain text documents (`.txt`).
- **Visual Difference Highlighting:** Highlight differences to make document changes easier to understand.
- **User-Friendly GUI:** Simple graphical interface for selecting and comparing documents.
- **Local File Processing:** Documents are processed on the user's system.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application development |
| PyQt | Graphical User Interface |
| python-docx | Reading and extracting Word document content |
| difflib | Identifying text differences |
| Pillow (PIL) | Image processing, if used |
| PyInstaller | Packaging the application into an executable |

## 📂 Project Structure

```text
Doc2Comp/
│
├── main.py
│
├── gui/
│   └── GUI-related files
│
├── utils/
│   └── Utility modules
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

*Note: The structure above is illustrative. Actual files and folders may vary depending on the project implementation.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/siridhachenna-0112/Document-Comparator.git
```

### 2. Navigate to the Project Directory

```bash
cd Document-Comparator
```

### 3. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python main.py
```

## 📖 How to Use

1. Launch the Offline Document Comparator application.
2. Select the first document using the file browser.
3. Select the second document you want to compare.
4. Click the Compare button.
5. The application processes both documents.
6. View the differences identified between the documents.
7. Examine highlighted changes and their corresponding line numbers.

## 🎯 Applications

- Comparing different versions of documents.
- Identifying modifications in reports and technical documents.
- Reviewing changes in text files.
- Document verification and validation.
- Detecting content changes between Word documents.

## 🔒 Privacy and Security

The application is designed for offline document comparison.

- No internet connection is required for document processing.
- Files are processed locally.
- Documents do not need to be uploaded to external servers.

## 🔮 Future Enhancements

- Improved image comparison inside Word documents.
- Table structure and cell-level comparison.
- Advanced formatting and layout comparison.
- Export comparison results as PDF or DOCX.
- Improved handling of large documents.
- More detailed difference reports.

## 👩‍💻 Developer

**Siridha Chenna**

Project: Offline Document Comparator

Technology: Python | PyQt | Document Processing

## 📜 License

This project is currently intended for educational and development purposes.
