# Takes JSON files with YouTube Data API data and creates CSV files in the
# Gremlin format to be added to the S3 bucket

import sys
import json

def open_every_file():
    file_list = []
    filenames = ["GCQmVzdCBvZiBZb3VUdWJl", "GCQ3JlYXRvciBvbiB0aGUgUmlzZQ", "GCTXVzaWM", "GCQ29tZWR5", "GCRmlsbSAmIEVudGVydGFpbm1lbnQ", 
        "GCR2FtaW5n", "GCQmVhdXR5ICYgRmFzaGlvbg", "GCU3BvcnRz", "GCVGVjaA", "GCQ29va2luZyAmIEhlYWx0aA", "GCTmV3cyAmIFBvbGl0aWNz"]
    for f in filenames:
        try:
            tmp_file = open(f+".txt", "r")
            data = tmp_file.read()
            tmp_file.close()
            data = json.loads(data)
            file_list.append(data)
        except:
            print("File " + f + " not found.")
    
    return file_list

def main():
    files = open_every_file()
    unique_tags = {}
    # Build the vertices, output to vertices.csv
    pID = tID = eID = 1
    v_csv = open("vertices.csv", "w")
    v_csv.write("~id, ~label, title:string\n")
    e_csv = open("edges.csv", "w")
    e_csv.write("~id, ~from, ~to, ~label, weight:Int\n")
    for f in files:
        for video_id in f:
            title_tags = f[video_id]
            v_csv.write("p" + str(pID) + ", Person, " + title_tags["title"] + "\n")
            tags = title_tags["tags"]
            for key in tags:
                if(key not in unique_tags):
                    unique_tags[key] = tID
                    v_csv.write("t" + str(tID) + ", Tag, " + key + "\n")
                e_csv.write("e" + str(eID) + ", p" + str(pID) + ", t" + str(unique_tags[key]) + ", ok boomer, " + str(tags[key]) + "\n") 
                eID += 1
                e_csv.write("e" + str(eID) + ", t" + str(unique_tags[key]) + ", p" + str(pID) + ", ok boomer, " + str(tags[key]) + "\n")
                eID += 1
                tID += 1
            pID += 1
    e_csv.close()
    v_csv.close()

if __name__ == "__main__":
    main()
