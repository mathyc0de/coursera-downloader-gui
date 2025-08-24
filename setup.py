from setuptools import setup, find_packages

setup(
    name='coursera-downloader-gui',  # Um nome único para o seu pacote
    version='0.1.0',
    packages=find_packages(),
    author='Matheus Silveira',
    author_email='matheuspsilveira0@gmail.com',
    description='Coursera downloader with GUI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'PyQt6',
        'coursera-helper @ git+https://github.com/mathyc0de/coursera-helper-py3.13.git',
        'packaging',
        'shutil'
    ],
    
    entry_points={
        'console_scripts': [
            'coursera-downloader-gui = src.main:main',
        ],
    },
    # -------------------------
    
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)