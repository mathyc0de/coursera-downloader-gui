from subprocess import run, Popen
import os
from src.utils.data_type import DownloadParameters
import shutil

OS = os.name
if OS == "nt":
    from subprocess import CREATE_NEW_CONSOLE
else:
    CREATE_NEW_CONSOLE = 0

def run_in_new_terminal(command):
    terminals = [
        {'name': 'gnome-terminal', 'args': ['--']},
        {'name': 'konsole', 'args': ['-e']},
        {'name': 'terminator', 'args': ['-x']},
        {'name': 'xterm', 'args': ['-e']}
    ]

    for term in terminals:
        terminal_path = shutil.which(term['name'])
        if terminal_path:
            try:
                full_command = [terminal_path] + term['args'] + command
                return Popen(full_command)
            except Exception as e:
                print(f"Failed to start with {term['name']}: {e}")
                continue
    return None

class CourseraDownloader:
    def __init__(self, cauth: str, download_parameters: DownloadParameters = DownloadParameters(), output_path: str = "./"):
        self.__cauth = cauth
        self.download_parameters = download_parameters
        self.output_path = output_path
        self.__save_cauth()
    


    @staticmethod
    def read_cauth_from_disk():
        OS = os.name
        if (OS == "nt"):
            appdata = os.environ.copy()["LOCALAPPDATA"]
            path = os.path.join(appdata, "coursera-downloader-gui")
        elif OS == "posix":
            home = os.path.expanduser("~")
            path = os.path.join(home, ".coursera-downloader-gui")
        
        file_path = os.path.join(path, "cauth.txt")
        if (os.path.exists(file_path)):
            cauth = open(file_path, 'r').read()
            success = CourseraDownloader.test_cauth(cauth)
            return (success, cauth)
        return (False, "")
    
    @staticmethod
    def test_cauth(cauth: str) -> bool:
        output = run(["coursera-helper", "--cauth", cauth, "--list-courses"], capture_output=True).stderr.decode().splitlines()[2]
        return output.find("Error 403") == -1
    

    def __save_cauth(self):
        OS = os.name
        if (OS == "nt"):
            appdata = os.environ.copy()["LOCALAPPDATA"]
            path = os.path.join(appdata, "coursera-downloader-gui")
        elif OS == "posix":
            home = os.path.expanduser("~")
            path = os.path.join(home, ".coursera-downloader-gui")
            

        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "cauth.txt"), "w") as f:
            f.write(self.__cauth)
            f.close()
        

    def __parse_parameters(self):
        param = self.download_parameters
        parsed = [
            "coursera-helper",
            "--ignore-formats", "html mspx",
            "--resume",
            "--cauth", self.__cauth,
            "--video-resolution", param.resolution.value,
            "--download-delay", str(param.download_delay),
            "-sl", param.subtitles,
            "--download-notebooks" if param.download_notebooks else None,
            "--download-quizzes" if param.download_quizzes else None
        ]
        return list(filter(lambda x: x != None, parsed))
     
    def get_courses(self) -> list[str]:
        result = run(["coursera-helper", "--cauth", self.__cauth, "--list-courses"], capture_output=True)
        return result.stderr.decode().splitlines()[3:]

    def download_course(self, name: str):
        parameters = self.__parse_parameters()
        parameters.extend(["--path", self.output_path, name])
        if (OS == "nt"): return Popen(parameters, creationflags=CREATE_NEW_CONSOLE)
        return run_in_new_terminal(parameters)

    def download_specialization(self, name: str):
        path = os.path.join(self.output_path, f"./{name}/")
        os.makedirs(path, exist_ok=True)
        parameters = self.__parse_parameters()
        parameters.extend(["--path", path, "--specialization", name])
        if (OS == "nt"): return Popen(parameters, creationflags=CREATE_NEW_CONSOLE)
        return run_in_new_terminal(parameters)