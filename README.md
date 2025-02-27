# My Python GUI OCR Application

This project is a Python application with a graphical user interface (GUI) that allows users to drag and drop or click to select a PDF file for Optical Character Recognition (OCR) processing. The application processes the selected PDF file and displays the results.

## Project Structure

```
my-python-gui-app
├── src
│   ├── main.py          # Entry point of the application
│   ├── ocr_processor.py  # Logic for processing PDF files using OCR
│   └── gui
│       └── app.py       # GUI components and file selection handling
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

## Requirements

To run this application, you need to install the following dependencies:

- tkinter
- pillow
- pytesseract
- pdf2image

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Usage

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies as mentioned above.
4. Run the application using the following command:

```
python src/main.py
```

5. A window will open where you can drag and drop a PDF file or click to select one.
6. The application will process the PDF file and display the OCR results.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.