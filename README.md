# Coursera Downloader GUI

# Portuguese

Esse projeto visa criar uma interface de usuário para o pacote coursera-helper (fork de coursera-dl), no qual tem como objetivo baixar vídeos, leituras e quizzes, notebooks e recursos em geral, dos cursos e especializações do website coursera. 

## Instruções de instalação (Windows)

Copie o código disponibilizado abaixo, no qual executa o script run.ps1, que se encarregará de instalar as dependências necessárias, moverá os arquivos construídos para a pasta program files do seu disco e criará um atalho na área de trabalho.

**Código:**
```powershell
iex "& { $(curl -useb 'https://raw.githubusercontent.com/mathyc0de/coursera-downloader-gui/refs/heads/main/run.ps1') }"
```

## Instruções de instalação (Linux)

O mesmo processo é feito no linux, copie o link abaixo e cole no terminal.

**Código:**
```bash
curl -useb https://raw.githubusercontent.com/mathyc0de/coursera-downloader-gui/refs/heads/main/run.sh | bash
```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

This will launch the GUI, allowing you to log in to Coursera and manage your course downloads.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.


# English