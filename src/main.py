from PyQt6.QtWidgets import QApplication
import sys
# import subprocess
from gui.main_window import MainWindow

# def ensure_coursera_helper():
#     try:
#         from coursera_helper import __version__
#     except ImportError:
#         print("coursera-helper not found. Installing...")
#         subprocess.run(
#             [sys.executable, "-m", "pip", "install", "git+https://github.com/mathyc0de/coursera-helper-py3.13"],
#             check=True
#         )

def main():
    # ensure_coursera_helper()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()