# File Faces Extractor

This is a script to extract face images from PDF/MS WORD files.

### Usage
    usage: face_extractor.py [-h] [-lc LOGCONFIG] -r READ -s SAVE

    This is a script to extract face images from pdf/MS WORD files

    optional arguments:
    -h, --help            show this help message and exit
    -lc LOGCONFIG, --logconfig LOGCONFIG
                          load the configuration file for the logger
    -r READ, --read READ  path of the folder contains files
    -s SAVE, --save SAVE  path of the folder to save face images

### Note
- [haarcascade_frontalface_default.xml](./haarcascade_frontalface_default.xml) must be put in the same folder as [face_extractor.py](./face_extractor.py)

### Reference
- [haarcascade_frontalface_default.xml](./haarcascade_frontalface_default.xml) is from https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml