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

Note that you should only run this script a few times a day, as the YouTube
data API has a 10,000 query cutoff that resets every day at 3 AM.  To
populate the S3 bucket, this script should be run over a few days, with a
couple of guide category IDs run each day.