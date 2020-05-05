import argparse
import pathlib
from collections import defaultdict

from main_logger import logger

# Argument parser.
parser = argparse.ArgumentParser()
parser.add_argument("--primary", type=str, help="the primary hashes file, the one that we are going to enter")
parser.add_argument("--files", nargs='+', type=str, help="the other files")

args = parser.parse_args()


class HashesFile:
    """
    This class represent hashes file
    """
    # this is the default space that have between hash and path inside hashes file.
    # <sha256sum> SPACE_BETWEEN_HASH_AND_PATH <path>
    SPACE_BETWEEN_HASH_AND_PATH = "  "

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.data = self._create_data_from_file()

    def _create_data_from_file(self):
        data = defaultdict()
        with open(self.path, 'r') as f:
            for line in f.readlines():
                hash_val, path = line.split(self.SPACE_BETWEEN_HASH_AND_PATH)
                data[path] = hash_val

        return data

    def compare(self, other):
        comparing_details = defaultdict()
        comparing_details["not_equal_hashes"] = list()
        comparing_details["paths_only_in_self"] = list()
        comparing_details["equal_hashes"] = list()

        for (path, hash_val) in self.data.items():
            if path in other.data:
                if self.data[path] != other.data[path]:
                    comparing_details["not_equal_hashes"].append(path)
                else:
                    comparing_details["equal_hashes"].append(path)
            else:
                comparing_details["paths_only_in_self"].append(path)

        comparing_details["paths_only_in_other"] = [p for p in other.data.keys() if p not in self.data]

        return comparing_details


def main():
    primary_file = HashesFile(args.primary)
    other_files = [HashesFile(path) for path in args.files]

    SPLIT_BETWEEN_MSG_SIGN = "##############################\n\n\n"
    for another_file in other_files:
        comparing_details = primary_file.compare(another_file)

        logger.info("Changes between file {} and file {}".format(primary_file.path, another_file.path))
        logger.info(SPLIT_BETWEEN_MSG_SIGN)

        logger.info("NOT EQUAL HASHES:")
        logger.info(comparing_details["not_equal_hashes"])

        logger.info(SPLIT_BETWEEN_MSG_SIGN)

        logger.info("PATHS ONLY IN SELF:")
        logger.info(comparing_details["paths_only_in_self"])
        logger.info(SPLIT_BETWEEN_MSG_SIGN)

        logger.info("PATHS ONLY IN OTHER:")
        logger.info(comparing_details["paths_only_in_other"])
        logger.info(SPLIT_BETWEEN_MSG_SIGN)

        logger.info("EQUAL HASHES:")
        logger.info(comparing_details["equal_hashes"])
        logger.info(SPLIT_BETWEEN_MSG_SIGN)

        logger.info("Summary: ")
        logger.info("Number of files that they hashes is not equal: {}".format(len(comparing_details["not_equal_hashes"])))
        logger.info("Number of files that they hashes is equal: {}".format(len(comparing_details["equal_hashes"])))
        logger.info("Number of files that found only in primary file is: {}".format(len(comparing_details["paths_only_in_self"])))
        logger.info("Number of files that found only in second file is: {}".format(len(comparing_details["paths_only_in_other"])))



if __name__ == '__main__':
    main()

