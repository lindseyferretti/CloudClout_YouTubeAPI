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

    load_data(channels_to_tags)


def load_data(channels_to_tags):
    # TODO: create files in CSV format for Gremlin, dump in S3 bucket 
    i = 1
    write = open("verticies.csv", "a")
    write.write("~id, videoID:string, tags:string[]\n")
    for key in channels_to_tags:
        string_to_write = str(i) + ", " + key + ", \""
        for tag in channels_to_tags[key]:
            string_to_write += tag + "; "
        string_to_write += "\"\n"
        write.write(string_to_write)
        i += 1
    write.close()

if __name__ == "__main__":
    main()
