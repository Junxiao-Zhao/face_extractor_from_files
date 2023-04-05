import argparse
from file_face_extract import face_from_files

descrip = "This is a script to extract face images from pdf/MS WORD files"

parser = argparse.ArgumentParser(description=descrip)

# config
parser.add_argument("-lc",
                    "--logconfig",
                    nargs=1,
                    type=str,
                    const=None,
                    help="load the configuration file for the logger")
# paths
parser.add_argument("-r",
                    "--read",
                    type=str,
                    nargs=1,
                    required=True,
                    help="path of the folder contains files")
parser.add_argument("-s",
                    "--save",
                    type=str,
                    nargs=1,
                    required=True,
                    help="path of the folder to save face images")

# parse args
args = parser.parse_args()

if args.logconfig:
    args.logconfig = args.logconfig[0]

extractor = face_from_files(args.read[0], args.save[0], args.logconfig)
extractor.process()
