import os
import cv2
import fitz
import docx
import json
import logging
import logging.config
import numpy as np


def load_config(config_path: str) -> dict:
    """Load the configuration

    :param config_path: the path of the configuration file
    :return: the configuration
    """

    try:
        with open(config_path, 'r') as cfg:
            config = json.load(cfg)
        print("Success to load file: '%s'" % config_path)
        return config

    except Exception as e:
        print("Error:", e)
        exit()


class face_from_files:

    def __init__(self,
                 read_path: str,
                 save_path: str,
                 logger_config_path: str = None) -> None:
        """This class is used to extract face images from resumes in pdf or word doc format

        :param read_path: the folder stores the resumes
        :param save_path: the folder to save the face images
        :param logger_config_path: the path of logger config file; if not specified, use default
        """

        self.read_path = read_path
        self.save_path = save_path
        self.files = os.listdir(read_path)
        self.face_detector = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")

        # config logger
        config_path = os.path.join(
            os.path.dirname(__file__),
            'logconfig.json') if not logger_config_path else logger_config_path
        logconfig = load_config(config_path)
        logging.config.dictConfig(logconfig)
        logname = list(logconfig["loggers"].keys())[0]
        self.logger = logging.getLogger(logname)
        self.logger.info("Success to load logger '%s'" % logname)

    def doc_imgs(self, file_path: str) -> list:
        """Extract faces from a word doc

        :param file_path: the file path of the doc
        :return: a list of all faces in this doc
        """

        self.logger.debug("Extracting images from '%s'" % file_path)

        doc = docx.Document(file_path)
        faces = list()

        # extract images from each rel
        for rel in doc.part._rels.values():
            if "image" in rel.target_ref:
                # store faces on each image
                img = rel.target_part.blob
                img_array = np.frombuffer(img, dtype=np.uint8)
                faces += self.extract_face(img_array)

        return faces

    def pdf_imgs(self, file_path: str) -> list:
        """Extract faces from a pdf

        :param file_path: the file path of the pdf
        :return: a list of all faces in this pdf
        """

        self.logger.debug("Extracting images from '%s'" % file_path)

        pdf = fitz.open(file_path)
        faces = list()

        # extract images from each page
        for page in pdf:
            for img_info in page.get_images():
                # store faces on each image
                img = pdf.extract_image(img_info[0])
                img_array = np.frombuffer(img["image"], dtype=np.uint8)
                faces += self.extract_face(img_array)

        return faces

    def extract_face(self, img_array: np.ndarray) -> list:
        """Extract faces from a given image

        :param img_array: the binary data of the image
        :return: a list of faces
        """

        img = cv2.imdecode(img_array,
                           flags=cv2.IMREAD_COLOR)  # decode image from binary
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # covert to grayscale
        faces = self.face_detector.detectMultiScale(gray, 1.3,
                                                    5)  # detect faces
        store = list()

        for x1, y1, x2, y2 in faces:
            # store cropped image
            face = cv2.resize(img[y1:y1 + y2, x1:x1 + x2], (128, 128))
            store.append(face)

        return store

    def write_face(self, faces: list, save_path: str, img_name: str) -> None:
        """Write faces to png files

        :param faces: a list of faces
        :param save_path: the folder to save
        :param img_name: the name of the images
        """

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for i, f in enumerate(faces):

            if len(f) > 0:
                try:
                    file_path = os.path.join(save_path, img_name % i)
                    cv2.imwrite(file_path, f)
                except Exception as e:
                    self.logger.exception(e, exc_info=False)
                    continue

    def process(self) -> None:
        """Extract and save faces from all pdf and doc in the given foler"""

        for file in self.files:

            file_ext = file.split(".")[1]
            file_path = os.path.join(self.read_path, file)

            try:
                # determine the file type
                if "do" in file_ext:
                    file_faces = self.doc_imgs(file_path)
                elif "pdf" in file_ext:
                    file_faces = self.pdf_imgs(file_path)
                else:
                    self.logger.error("Not a pdf or word file: '%s'" % file)
                    continue

                if file_faces:  # this pdf contains faces
                    img_name = file.split(".")[0] + "_face-%d.png"
                    self.write_face(file_faces, self.save_path, img_name)
                    self.logger.info("Success to save all faces from '%s'" %
                                     file)
                else:
                    self.logger.warning("No faces contained in '%s'" % file)

            except Exception as e:
                self.logger.exception(e, exc_info=False)
                continue
            except KeyboardInterrupt:
                self.logger.warning("Keyboard Interrupt; Exit")
                exit()

        self.logger.info("Finish!")
