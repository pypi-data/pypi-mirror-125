from setuptools import setup

VERSION = '0.0.3'
DESCRIPTION = 'String validation and sanitization'
LONG_DESCRIPTION = 'Package that allows for validate and sanitize of string values. For example to check if a string is an ascii string etc.'

# Setting up
setup(
    name="py.validator",
    version=VERSION,
    author="theteladras",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['validator'],
    install_requires=['opencv-python', 'pyautogui', 'pyaudio'],
    keywords=['python', 'validation', 'sanitization', 'javascript'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    license='MIT'
)
