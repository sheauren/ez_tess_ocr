import setuptools
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ez_tess_ocr",
    version="0.0.1",
    author="Sheauren Wang",
    author_email="sheauren@gmail.com",
    description="OCR by tesseract c++ library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    url="https://github.com/sheauren/ez_tess_ocr",
    packages=setuptools.find_packages(),
    data_files=[("tesslib",glob.glob("tesslib/*.dll")),("tesslib/tessdata",["tesslib/tessdata/eng.traineddata"])],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License"        
    ],
    python_requires='>=3.5',
)