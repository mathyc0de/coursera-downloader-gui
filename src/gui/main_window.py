from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox,
    QStackedWidget, QLineEdit, QFormLayout, QScrollArea, QCheckBox, QComboBox, QFileDialog, QProgressBar, QTextBrowser
)
from src.utils.data_type import DownloadParameters, Resolution, Subtitle
from src.downloader.coursera_downloader import CourseraDownloader
import os


DEFAULT_VIDEO_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(DEFAULT_VIDEO_PATH, exist_ok=True)
TUTORIAL_PT = """
            <h1>Como obter o CAUTH (Português)</h1>
            <ol>
                <li>Acesse o website do <a href="https://www.coursera.org/">Coursera</a> e faça login</li>
                <li>Aperte a tecla F12 e vá até a aba application (ou storage, dependendo do navegador)</li>
                <li>Na seção lateral a esquerda pode ser encontrada uma subseção de cookies, expanda e clique na opção que contenha
                o nome do site do coursera </li>
                <li>Clique em CAUTH e copie o valor disponível abaixo, em 'Cookie Value'</li>
                <li>Cole na seção de entrada de texto e prossiga para a próxima tela</li>
            </ol>
        """

TUTORIAL_EN = """
            <h1>How to get your CAUTH (English)</h1>
            <ol>
                <li>Go to the <a href="https://www.coursera.org/">Coursera</a> website and login</li>
                <li>Press F12 and open the Application (or Storage) tab in your browser's developer tools</li>
                <li>On the left sidebar, find the Cookies section, expand it, and click the option containing 'coursera.org'</li>
                <li>Find the CAUTH cookie and copy its value from the 'Cookie Value' field</li>
                <li>Paste it into the text input section and proceed to the next screen</li>
            </ol>
        """

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
        layout.addRow(QLabel("Enter your CAUTH authentication:"))
        self.cauth_input = QLineEdit()
        layout.addRow("CAUTH:", self.cauth_input)
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_cauth)
        layout.addRow(submit_btn)
        self.tutorial_pt_widget = QTextBrowser()
        self.tutorial_pt_widget.setOpenExternalLinks(True)
        self.tutorial_pt_widget.setHtml(TUTORIAL_PT)
        self.tutorial_en_widget = QTextBrowser()
        self.tutorial_en_widget.setOpenExternalLinks(True)
        self.tutorial_en_widget.setHtml(TUTORIAL_EN)
        layout.addWidget(self.tutorial_pt_widget)
        layout.addWidget(self.tutorial_en_widget)
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
        self.pt_label = QLabel("Seja bem vindo ao Coursera Downloader!\n\nSe inscreva em cursos no website Coursera para " \
        "que as opções de download apareçam em 'download course'.\nPara especializações, basta colar o link da especialização.")
        self.en_label = QLabel(
            "Welcome to the Coursera Downloader!\n\n"
            "Enroll in courses on the Coursera website for them to appear in the 'Download Course' option.\n"
            "For specializations, just paste the specialization URL."
        )
        layout.addWidget(self.pt_label)
        layout.addWidget(self.en_label)
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
        self.download_quizzes = QCheckBox("Download Quizzes")
        self.download_quizzes.setChecked(True)
        self.resolution_selector = QComboBox()
        self.resolution_selector.addItems(["480p (SD)", "720p (HD)", "1080p (Full HD)"])
        self.resolution_selector.setCurrentIndex(1)
        self.substitles = QComboBox()
        self.substitles.addItems(["english", "portuguese", "english | portuguese"])
        self.substitles.setCurrentIndex(2)
        self.path_input = QLineEdit(DEFAULT_VIDEO_PATH)
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
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", directory=DEFAULT_VIDEO_PATH)
        if folder:
            self.path_input.setText(folder)

    def start_course_download(self, course_name):
        res = [Resolution.SD, Resolution.HD, Resolution.FULLHD][self.resolution_selector.currentIndex()]
        subtitle = [Subtitle.english, Subtitle.portuguese, f"{Subtitle.english.value}, {Subtitle.portuguese.value}"][self.substitles.currentIndex()]
        self.downloader.download_parameters = DownloadParameters(
            resolution=res,
            subtitles=subtitle,
            download_notebooks = self.download_notebooks.isChecked(),
            download_quizzes = self.download_quizzes.isChecked()
        )
        self.downloader.output_path = self.path_input.text()

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
        self.path_input = QLineEdit(DEFAULT_VIDEO_PATH)
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
        parameters_idx = spec.find("?")
        if (parameters_idx != -1):
            spec = spec[:parameters_idx]
        res = [Resolution.SD, Resolution.HD, Resolution.FULLHD][self.resolution_selector.currentIndex()]
        subtitle = [Subtitle.english, Subtitle.portuguese, f"{Subtitle.english.value}, {Subtitle.portuguese.value}"][self.substitles.currentIndex()]
        self.downloader.download_parameters = DownloadParameters(
            resolution=res,
            subtitles=subtitle,
            download_notebooks = self.download_notebooks.isChecked(),
            download_quizzes = self.download_quizzes.isChecked()
        )

        self.downloader.output_path = self.path_input.text()

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