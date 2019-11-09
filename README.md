# CloudClout_YouTubeAPI
To run, provide one of the following guide category IDs:

- Best of Youtube: GCQmVzdCBvZiBZb3VUdWJl
- Creator on the Rise: GCQ3JlYXRvciBvbiB0aGUgUmlzZQ
- Music: GCTXVzaWM
- Comedy: GCQ29tZWR5
- Film & Entertainment: GCRmlsbSAmIEVudGVydGFpbm1lbnQ
- Gaming: GCR2FtaW5n
- Beauty and Fashion: GCQmVhdXR5ICYgRmFzaGlvbg
- Sports: GCU3BvcnRz
- Tech: GCVGVjaA
- Cooking and Health: GCQ29va2luZyAmIEhlYWx0aA
- News and Politics: GCTmV3cyAmIFBvbGl0aWNz

Note that you should only run the YouTubeAPI script a few times a day, as
the YouTube
data API has a 10,000 query cutoff that resets every day at 3 AM.  To
populate the S3 bucket, this script should be run over a few days, with a
couple of guide category IDs run each day.

Each time the YouTubeAPI script is run with a guide category, the results
are converted to JSON and dumped into a txt file with the same name as the
category ID.  When you're ready to create the CSV files needed to load data
into the graph, these txt files should be compiled into a single JSON txt
file.

## Loading Data
After the guide categories have all been run through the YouTubeAPI script
and the resulting JSON has been compiled into a SINGLE txt file, to create
the CSV files, you must run the DataLoader script, providing an argument of
the name of the txt file.