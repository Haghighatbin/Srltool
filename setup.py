from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
    
setup(
    name = 'srltool',
    version = '0.0.1',
    author = 'Amin Haghighatbin',
    author_email = 'aminhb@tutanota.com',
    license = 'MIT License',
    description = 'A serial tool for Micropython devices',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/haghighatbin/Srltool.git',
    py_modules = ['src', 'cli'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: Linux",
    ],
    entry_points = '''
        [console_scripts]
        srltool=cli:main
    '''
)