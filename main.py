import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
)
from unlock_pdf import unlock_pdf

class PDFUnlocker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Unlocker")

        self.layout = QVBoxLayout()

        # Input PDF file
        self.input_file_label = QLabel("Input PDF File:")
        self.layout.addWidget(self.input_file_label)
        self.input_file_entry = QLineEdit()
        self.layout.addWidget(self.input_file_entry)
        self.input_file_button = QPushButton("Browse")
        self.input_file_button.clicked.connect(self.select_input_file)
        self.layout.addWidget(self.input_file_button)

        # Output file name
        self.output_file_name_label = QLabel("Output File Name (without extension):")
        self.layout.addWidget(self.output_file_name_label)
        self.output_file_name_entry = QLineEdit()
        self.layout.addWidget(self.output_file_name_entry)

        # Output file path
        self.output_file_path_label = QLabel("Output File Path (optional):")
        self.layout.addWidget(self.output_file_path_label)
        self.output_file_path_entry = QLineEdit()
        self.layout.addWidget(self.output_file_path_entry)

        # Password range
        self.start_range_label = QLabel("Start Password (e.g. 0000000000):")
        self.layout.addWidget(self.start_range_label)
        self.start_range_entry = QLineEdit()
        self.layout.addWidget(self.start_range_entry)

        self.end_range_label = QLabel("End Password (e.g. 9999999999):")
        self.layout.addWidget(self.end_range_label)
        self.end_range_entry = QLineEdit()
        self.layout.addWidget(self.end_range_entry)

        # Start button
        self.start_button = QPushButton("Unlock PDF")
        self.start_button.clicked.connect(self.brute_force_unlock)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def select_input_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Input PDF", "", "PDF files (*.pdf)")
        if filename:
            self.input_file_entry.setText(filename)

    def brute_force_unlock(self):
        input_file = self.input_file_entry.text()
        output_file_name = self.output_file_name_entry.text()
        output_file_path = self.output_file_path_entry.text()

        if not input_file or not output_file_name:
            QMessageBox.warning(self, "Input Error", "Please specify input PDF file and output file name.")
            return

        output_file = f"{output_file_path}/{output_file_name}.pdf" if output_file_path else f"{output_file_name}.pdf"

        try:
            start_range = int(self.start_range_entry.text())
            end_range = int(self.end_range_entry.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for the password range.")
            return

        QMessageBox.information(self, "Processing", "Starting to unlock the PDF... This may take a while.")

        for i in range(start_range, end_range + 1):
            candidate_password = str(i).zfill(10)  # Pad with zeros to make it 10 digits
            if unlock_pdf(candidate_password, input_file, output_file):
                QMessageBox.information(self, "Success", f"Unlocked with password: {candidate_password}")
                return

        QMessageBox.warning(self, "Failed", "Failed to unlock PDF with provided passwords.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFUnlocker()
    window.show()
    sys.exit(app.exec_())
