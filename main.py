import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSignal, QObject
from unlock_pdf import unlock_pdf
import time 

class WorkerSignals(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

class UnlockWorker(QRunnable):
    def __init__(self, input_file, output_file, start, end):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.start = start
        self.end = end
        self.signals = WorkerSignals()

    def run(self):
        for i in range(self.start, self.end + 1):
            candidate_password = str(i).zfill(10) 
            if unlock_pdf(candidate_password, self.input_file, self.output_file):
                self.signals.finished.emit(f"Unlocked with password: {candidate_password}")
                return

            self.signals.progress.emit(1)  

            time.sleep(0.01) 

        self.signals.finished.emit("Failed to unlock PDF with provided passwords.")

class PDFUnlocker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Unlocker")

        self.layout = QVBoxLayout()

        self.input_file_label = QLabel("Input PDF File:")
        self.layout.addWidget(self.input_file_label)
        self.input_file_entry = QLineEdit()
        self.layout.addWidget(self.input_file_entry)
        self.input_file_button = QPushButton("Browse")
        self.input_file_button.clicked.connect(self.select_input_file)
        self.layout.addWidget(self.input_file_button)

        self.output_file_name_label = QLabel("Output File Name (without extension):")
        self.layout.addWidget(self.output_file_name_label)
        self.output_file_name_entry = QLineEdit()
        self.layout.addWidget(self.output_file_name_entry)

        self.output_file_path_label = QLabel("Output File Path (optional):")
        self.layout.addWidget(self.output_file_path_label)
        self.output_file_path_entry = QLineEdit()
        self.layout.addWidget(self.output_file_path_entry)

        self.start_range_label = QLabel("Start Password (e.g. 0000000000):")
        self.layout.addWidget(self.start_range_label)
        self.start_range_entry = QLineEdit()
        self.layout.addWidget(self.start_range_entry)

        self.end_range_label = QLabel("End Password (e.g. 9999999999):")
        self.layout.addWidget(self.end_range_label)
        self.end_range_entry = QLineEdit()
        self.layout.addWidget(self.end_range_entry)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.percentage_label = QLabel("Progress: 0%")
        self.layout.addWidget(self.percentage_label)

        self.start_button = QPushButton("Unlock PDF")
        self.start_button.clicked.connect(self.brute_force_unlock)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        self.threadpool = QThreadPool()

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

        total_attempts = end_range - start_range + 1
        self.progress_bar.setMaximum(total_attempts)
        self.progress_bar.setValue(0)

        # Start the worker
        worker = UnlockWorker(input_file, output_file, start_range, end_range)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.finished.connect(self.show_result)
        self.threadpool.start(worker)

    def update_progress(self, value):
        self.progress_bar.setValue(self.progress_bar.value() + value)
        percentage = (self.progress_bar.value() / self.progress_bar.maximum()) * 100
        self.percentage_label.setText(f"Progress: {percentage:.2f}%")

    def show_result(self, message):
        QMessageBox.information(self, "Result", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFUnlocker()
    window.show()
    sys.exit(app.exec_())
