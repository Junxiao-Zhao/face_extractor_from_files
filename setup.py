from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='face_extractor',
      packages=find_packages(),
      version='0.0.1',
      author="Junxiao Zhao",
      description="A script to extract face images from pdf/MS WORD files",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/Junxiao-Zhao/face_extractor_from_files",
      license="MIT",
      install_requires=['opencv-contrib-python', 'pymupdf', 'python-docx'],
      py_modules=['face_extractor'],
      package_data={
          "file_face_extract": ["logconfig.json"],
          ".": ["haarcascade_frontalface_default.xml"]
      },
      python_requires='>=3.8')
