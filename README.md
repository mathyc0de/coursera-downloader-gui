# Coursera Downloader GUI

# Portuguese

Esse projeto visa criar uma interface de usuário para o pacote coursera-helper (fork de coursera-dl), no qual tem como objetivo baixar vídeos, leituras e quizzes, notebooks e recursos em geral, dos cursos e especializações do website coursera. 

## Requerimentos

É necessário Python (3.9 ou superior) instalado no computador.

## Instruções de instalação Windows

Copie o código disponibilizado abaixo, no qual executa o script run.ps1, que se encarregará de instalar as dependências necessárias e colocará o executável na área de trabalho do pc.

**Script:**
```powershell
iex "& { $(curl -useb 'https://raw.githubusercontent.com/mathyc0de/coursera-downloader-gui/refs/heads/main/run.ps1') }"
```

## Instruções de instalação Windows / Linux (avançado)

Para usuários de Linux e usuários avançados do Windows, é possível instalar o downloader via pip:

**Script:**
```bash
pip install git+https://github.com/mathyc0de/coursera-downloader-gui.git
```

Execute o programa com:

**Alias:**
```bash
coursera-downloader-gui
```

## Contribuir

Contribuições são bem-vindas, fique a vontade para fazer um fork e melhorar/adicionar novas features ao código. 

## Observação

O UI do código foi feito com vibe coding e, todo o programa foi feito em 2 dias, logo a estrutura do código não estará totalmente profissional, havendo repetições de código e vários outros problemas de engenharia de software. O intuito desse projeto, inicialmente, foi apenas disponibilizar uma ferramenta para democratizar o acesso a informação, na qual pode ser feita solicitando um teste gratuito no coursera plus e baixando todos os cursos e especializações que o usuário desejar.

## License

This project is licensed under the GPL License. See the LICENSE file for more details.


# English
This project aims to create a user interface for the coursera-helper package (a fork of coursera-dl), which is designed to download videos, readings, quizzes, notebooks, and general resources from courses and specializations on the Coursera website.

## Requeriments

The installation of Python (3.9 or higher).

## Windows Installation Instructions
Copy the code provided below, which executes the run.ps1 script. This script will handle the installation of necessary dependencies and copy the executable file to desktop.

**Script:**
```powershell
iex "& { $(curl -useb 'https://raw.githubusercontent.com/mathyc0de/coursera-downloader-gui/refs/heads/main/run.ps1') }"
```

## Windows / Linux Installation Instructions (Advanced)
For Linux users and advanced Windows users, it is possible to install the downloader via pip:

**Script:**
```bash
pip install git+https://github.com/mathyc0de/coursera-downloader-gui.git
```

Run the program with:

**Alias:**
```bash
coursera-downloader-gui
```

## Contributing
Contributions are welcome. Feel free to fork the repository and improve/add new features to the code.

## Note
The UI of the code was developed through "vibe coding," and the entire program was created in 2 days. Therefore, the code structure may not be entirely professional, containing code repetitions and various other software engineering issues. The initial goal of this project was simply to provide a tool to democratize access to information, which can be achieved by signing up for a Coursera Plus free trial and downloading all the courses and specializations the user desires.

## License
This project is licensed under the GPL License. See the LICENSE file for more details.
