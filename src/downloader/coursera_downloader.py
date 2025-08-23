from subprocess import run, Popen, CREATE_NEW_CONSOLE
import os
from data_type import DownloadParameters

class CourseraDownloader:
    def __init__(self, cauth: str, download_parameters: DownloadParameters = DownloadParameters(), output_path: str = "./"):
        self.__cauth = cauth
        self.__download_parameters = download_parameters
        self.__output_path = output_path
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
        param = self.__download_parameters
        parsed = [
            "coursera-helper",
            "--ignore-formats", "html mspx",
            "--resume",
            "--cauth", self.__cauth,
            "--video-resolution", param.resolution.value,
            "--download-delay", str(param.download_delay),
            "-sl", ",".join(sub.value for sub in param.subtitles),
            "--download-notebooks" if param.download_notebooks else None,
            "--download-quizzes" if param.download_quizzes else None
        ]
        return list(filter(lambda x: x != None, parsed))
     
    def get_courses(self) -> list[str]:
        result = run(["coursera-helper", "--cauth", self.__cauth, "--list-courses"], capture_output=True)
        return result.stderr.decode().splitlines()[3:]

    def download_course(self, name: str):
        parameters = self.__parse_parameters()
        parameters.extend(["--path", self.__output_path, name])
        print(parameters)
        return Popen(parameters, creationflags=CREATE_NEW_CONSOLE)

    def download_specialization(self, name: str):
        path = os.path.join(self.__output_path, f"./{name}/")
        os.makedirs(path, exist_ok=True)
        parameters = self.__parse_parameters()
        parameters.extend(["--path", path, "--specialization", name])
        print(parameters)
        return Popen(parameters, creationflags=CREATE_NEW_CONSOLE)