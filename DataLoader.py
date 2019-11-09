# Takes JSON files with YouTube Data API data and creates CSV files in the
# Gremlin format to be added to the S3 bucket

import sys
import json


def main():
    file_name = sys.argv[1]
    json_file = open(file_name, "r")
    json_text = json_file.read()
    json_file.close()
    channels_to_tags = json.loads(json_text)

    print(channels_to_tags)
    load_data(channels_to_tags)


def load_data(channels_to_tags):
    # TODO: create files in CSV format for Gremlin, dump in S3 bucket
    pass


if __name__ == "__main__":
    main()