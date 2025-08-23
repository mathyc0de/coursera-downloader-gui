from dataclasses import dataclass
from enum import Enum

class Subtitle(Enum):
    portuguese = "pt-BR"
    english = "en"

class Resolution(Enum):
    SD = "480p"
    HD = "720p"
    FULLHD = "1080p"

@dataclass
class DownloadParameters:
    resolution: Resolution = Resolution.HD
    subtitles: tuple[Subtitle] = (Subtitle.portuguese, Subtitle.english)
    download_delay: int = 10
    download_notebooks: bool = True
    download_quizzes: bool = False
    output_path: str = "./"