from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox,
    QStackedWidget, QLineEdit, QFormLayout, QScrollArea, QCheckBox, QComboBox, QFileDialog, QProgressBar
)
from utils.data_type import DownloadParameters, Resolution, Subtitle
from downloader.coursera_downloader import CourseraDownloader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coursera Downloader")
        self.setGeometry(100, 100, 600, 400)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        success, cauth = CourseraDownloader.read_cauth_from_disk()
        if (success):
            self.downloader = CourseraDownloader(cauth)
            self.init_options_ui()
        else:
            self.init_auth_ui()
        
    def init_auth_ui(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Enter your CAUTH authentication string:"))
        self.cauth_input = QLineEdit()
        layout.addRow("CAUTH:", self.cauth_input)
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_cauth)
        layout.addRow(submit_btn)
        container = QWidget()
        container.setLayout(layout)
        self.stacked_widget.addWidget(container)
        self.stacked_widget.setCurrentWidget(container)
        
    def submit_cauth(self):
        self.cauth = self.cauth_input.text()
        if not self.cauth:
            QMessageBox.warning(self, "Error", "CAUTH string cannot be empty.")
            return
        if (CourseraDownloader.test_cauth(self.cauth)):
            self.downloader = CourseraDownloader(self.cauth)
            self.init_options_ui()
        else:
            QMessageBox.warning(self, "Error", "Invalid CAUTH")
        
    def init_options_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Welcome to the Coursera Downloader!")
        layout.addWidget(self.label)
        self.download_course_button = QPushButton("Download Course")
        self.download_course_button.clicked.connect(self.show_courses)
        layout.addWidget(self.download_course_button)
        self.download_specialization_button = QPushButton("Download Specialization")
        self.download_specialization_button.clicked.connect(self.download_specialization)
        layout.addWidget(self.download_specialization_button)
        container = QWidget()
        container.setLayout(layout)
        self.stacked_widget.addWidget(container)
        self.stacked_widget.setCurrentWidget(container)
        
    def show_courses(self):
        courses = self.downloader.get_courses() if hasattr(self.downloader, "get_courses") else ["Course 1", "Course 2"]
        layout = QVBoxLayout()
        label = QLabel("Select a course to download:")
        layout.addWidget(label)
        scroll = QScrollArea()
        course_widget = QWidget()
        course_layout = QVBoxLayout()
        for course in courses:
            btn = QPushButton(course)
            btn.clicked.connect(lambda _, c=course: self.show_download_parameters(c))
            course_layout.addWidget(btn)
        course_widget.setLayout(course_layout)
        scroll.setWidget(course_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        back_btn = QPushButton("Voltar")
        back_btn.clicked.connect(self.init_options_ui)
        layout.addWidget(back_btn)
        container = QWidget()
        container.setLayout(layout)
        self.stacked_widget.addWidget(container)
        self.stacked_widget.setCurrentWidget(container)


    def show_download_parameters(self, course_name):
        layout = QFormLayout()
        layout.addRow(QLabel(f"Download parameters for: {course_name}"))
        self.download_notebooks = QCheckBox("Donwload Notebooks")
        self.download_notebooks.setChecked(True)
        self.download_quizzes = QCheckBox("Download Quizzes (essa funcionalidade pode fazer o download travar)")
        self.resolution_selector = QComboBox()
        self.resolution_selector.addItems(["480p (SD)", "720p (HD)", "1080p (Full HD)"])
        self.resolution_selector.setCurrentIndex(1)
        self.substitles = QComboBox()
        self.substitles.addItems(["english", "portuguese", "english | portuguese"])
        self.substitles.setCurrentIndex(2)
        self.path_input = QLineEdit()
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)
        path_layout = QVBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        path_widget = QWidget()
        path_widget.setLayout(path_layout)

        layout.addRow("Resolution:", self.resolution_selector)
        layout.addRow("Subtitles:", self.substitles)
        layout.addWidget(self.download_notebooks)
        layout.addWidget(self.download_quizzes)
        layout.addRow("Download Path:", path_widget)
        download_btn = QPushButton("Start Download")
        download_btn.clicked.connect(lambda: self.start_course_download(course_name))
        layout.addRow(download_btn)
        back_btn = QPushButton("Voltar")
        back_btn.clicked.connect(self.init_options_ui)
        layout.addRow(back_btn)
        container = QWidget()
        container.setLayout(layout)
        self.stacked_widget.addWidget(container)
        self.stacked_widget.setCurrentWidget(container)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.path_input.setText(folder)

    def start_course_download(self, course_name):
        res = [Resolution.SD, Resolution.HD, Resolution.FULLHD][self.resolution_selector.currentIndex()]
        subtitle = [(Subtitle.english), (Subtitle.portuguese), (Subtitle.english, Subtitle.portuguese)][self.substitles.currentIndex()]
        self.downloader.__download_parameters = DownloadParameters(
            resolution=res,
            subtitles=subtitle,
            output_path=self.path_input.text(),
            download_notebooks = self.download_notebooks.isChecked(),
            download_quizzes = self.download_quizzes.isChecked()
        )

        # Progress bar UI
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Downloading {course_name}..."))
        layout.addWidget(self.progress_bar)
        container = QWidget()
        container.setLayout(layout)
        self.stacked_widget.addWidget(container)
        self.stacked_widget.setCurrentWidget(container)
        self.downloader.download_course(course_name)
        QMessageBox.information(self, "Download", f"Download for {course_name} started.")
        self.init_options_ui()

    def download_finished(self, course_name):
        self.progress_bar.setRange(0, 1)
        QMessageBox.information(self, "Download", f"Download for {course_name} finished.")
        self.init_options_ui()
        
    def download_specialization(self):
        layout = QFormLayout()
        self.spec_url = QLineEdit()
        layout.addRow("URL da especialização: ", self.spec_url)
        self.download_notebooks = QCheckBox("Donwload Notebooks")
        self.download_notebooks.setChecked(True)
        self.download_quizzes = QCheckBox("Download Quizzes")
        self.resolution_selector = QComboBox()
        self.resolution_selector.addItems(["480p (SD)", "720p (HD)", "1080p (Full HD)"])
        self.resolution_selector.setCurrentIndex(1)
        self.substitles = QComboBox()
        self.substitles.addItems(["english", "portuguese", "english | portuguese"])
        self.substitles.setCurrentIndex(2)

        # Path input and browse button
        self.path_input = QLineEdit()
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)
        path_layout = QVBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        path_widget = QWidget()
        path_widget.setLayout(path_layout)

        layout.addRow("Resolution:", self.resolution_selector)
        layout.addRow("Subtitles:", self.substitles)
        layout.addWidget(self.download_notebooks)
        layout.addWidget(self.download_quizzes)
        layout.addRow("Download Path:", path_widget)
        download_btn = QPushButton("Start Download")
        download_btn.clicked.connect(lambda: self.start_specialization_download(specialization_url=self.spec_url.text()))
        layout.addRow(download_btn)
        back_btn = QPushButton("Voltar")
        back_btn.clicked.connect(self.init_options_ui)
        layout.addRow(back_btn)
        container = QWidget()
        container.setLayout(layout)
        self.stacked_widget.addWidget(container)
        self.stacked_widget.setCurrentWidget(container)

    def start_specialization_download(self, specialization_url: str):
        spec = specialization_url[specialization_url.rindex("/") + 1:]
        res = [Resolution.SD, Resolution.HD, Resolution.FULLHD][self.resolution_selector.currentIndex()]
        subtitle = [(Subtitle.english), (Subtitle.portuguese), (Subtitle.english, Subtitle.portuguese)][self.substitles.currentIndex()]
        self.downloader.__download_parameters = DownloadParameters(
            resolution=res,
            subtitles=subtitle,
            output_path=self.path_input.text(),
            download_notebooks = self.download_notebooks.isChecked(),
            download_quizzes = self.download_quizzes.isChecked()
        )


        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Downloading {spec}..."))
        layout.addWidget(self.progress_bar)
        container = QWidget()
        container.setLayout(layout)
        self.stacked_widget.addWidget(container)
        self.stacked_widget.setCurrentWidget(container)

        self.downloader.download_specialization(spec)
        QMessageBox.information(self, "Download", f"Download for {spec} started.")
        self.init_options_ui()