import sys
import os
import json
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from ocr_processor import OCRProcessor
from logging_config import setup_logging

logger = setup_logging()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF OCR Processor")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel("Drag and drop a PDF file here or click to select.")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.select_button = QPushButton("Select PDF")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        self.export_button = QPushButton("Export to Excel")
        self.export_button.clicked.connect(self.export_to_excel)
        self.export_button.setEnabled(False)  # Disable until data is loaded
        layout.addWidget(self.export_button)

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.setLayout(layout)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path) and file_path.endswith('.pdf'):
                self.process_file(file_path)
            else:
                QMessageBox.critical(self, "Invalid File", "Please drop a valid PDF file.")

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        try:
            processor = OCRProcessor()
            result = processor.process_pdf(file_path)
            self.display_result(result)
        except Exception as e:
            QMessageBox.critical(self, "Processing Error", str(e))

    def display_result(self, result):
        if result['status'] == 'success':
            data = result['data']
            if data:
                headers = data[0].keys()
                self.result_table.setColumnCount(len(headers))
                self.result_table.setHorizontalHeaderLabels(headers)
                self.result_table.setRowCount(len(data))

                for row_idx, row_data in enumerate(data):
                    for col_idx, (key, value) in enumerate(row_data.items()):
                        self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
                
                self.export_button.setEnabled(True)  # Enable export button
                self.data = data  # Store data for export
            else:
                QMessageBox.information(self, "No Data", "No valid data found in the PDF.")
                self.export_button.setEnabled(False)
        else:
            QMessageBox.critical(self, "Processing Error", result['message'])
            self.export_button.setEnabled(False)

    def export_to_excel(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_path:
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'
            try:
                df = pd.DataFrame(self.data)
                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Export Successful", f"Data exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())