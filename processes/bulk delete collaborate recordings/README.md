# Bulk delete of Collaborate Recordings
This is a multi-part process:
1. Pull a list of recordings from the Collaborate REST API
2. Pull a list of recordings from Bb Data
3. Compare the two
4. Identify recording IDs to delete
5. Use the Collaborate REST API to delete the specific recording IDs

# Preparation
You will need to have Python 3 installed and the following modules:
- [jwt](https://pyjwt.readthedocs.io/en/stable/)
- [requests](https://pypi.org/project/requests/)

You will need these files saved to your computer in the same folder:
- get_recording_ids_by_date.py
- delete_recordings.py
- recordings.xlsx

In each file, edit the following:
 - Replace [your_lti_key] with your institution's LTI key
 - Replace [your_lti_secret] with your institution's LTI secret
 
Using your institution's key/secret allows the python scripts to access your institution's Collaborate content.

I recommend using [Notepad++](https://notepad-plus-plus.org/downloads/) to eliminate potential duplicates returned from the REST API and for general text editing.  Notepad++ is free (and awesome).  

I also recommend using an IDE for Python such as IDLE rather than using the command line to execute a script. You will want to screen scrape the returned values and this is easier outside of a command line.  Of course, you can add code to write these values to a text file but I was too lazy and felt it just as easy to copy and paste.

# 1. Pull a list of recordings from the Collaborate REST API
First, we are going to use the REST API to gather a list of all recordings between two dates.  There are other ways of filtering recordings. You can go to [https://docs.blackboard.com/collaborate/api](https://docs.blackboard.com/collaborate/api). 

Note: the API will only return 1000 recordings per day.  If you think you have more than 1000 recordings on a single day, you may need to use the "offset" parameter to obtain the remaining recordings. 

1. Open the file **get_recording_ids_by_date.py**
2. Edit the **start_date** and **end_date** variables

> Note: `datetime.datetime(2021, 5, 4)` will pull May 4, 2021.  `datetime.datetime(2021, 12, 4)` will pull December 4, 2021.

3. Save the file
4. Run the script

A lengthy list of recordings will display. Values returned are:
```
[recording_id] <tab> [session_name - recording_name] <tab> [recording_date] <tab> [public_status]
```

For example:
```
9125a93c8272418f8bfc86fdc3aa1e99	Office Hours - recording_2	5/6/2021 15:13	not public
```

It takes about 5 minutes to list about 18,000 recordings.

5. Launch Notepad++
6. Copy the contents returned by the script and paste into an empty Notepad++ file
7. If necessary, remove any starting/ending text that is irrelevant (e.g. any line which doesn't follow the values returned example listed above)
8. Remove any duplicate entries: in Notepad++, go to Edit > Line Operations > Remove Duplicate Lines
9. Copy the remaining entries
10. Open the file **recordings.xlsx**
11. Paste entries into line 2 of worksheet called "rest"
12. Sort worksheet "rest" by "recording_name" and then by "recording_date"
13. Save the file **recordings.xlsx**

# 2. Pull a list of recordings from Bb Data
We run this step for two main reasons:
1. REST doesn't contain any course information, but Bb Data does. For course rooms, we can get the course_id and term.  Unfortunately, Group Collaborate sessions have no mapping in Bb Data and will return empty for the course_id and term. Group-based Collaborate recordings have to be handled differently and that is outside the scope of this discussion.
2. Validate the list from REST.  Using two sources for data helps ensure that you have everything.

1. Log in to your Bb data instance
2. Open **bb_data_recordings_query.txt** 
3. Execute the query
4. Download the results (click the download button, select tab delimited)
5. Open the file **recordings.xlsx**
6. Paste entries (including header) into line 1 of worksheet called "bb data"
7. Sort worksheet "bb data" by "FULL_NAME" and then by "START_TIME"
8. Save the file **recordings.xlsx**

# 3. Compare the two
We do this part to associate the recording IDs from Step 1 with the courses we have identified from Step 2. This step is also good for catching recordings that may not have been consumed by Bb Data or that Bb Data may not have flagged as having already been deleted. In comparing, we want to look at the FULL_NAME and compare it to the recording_name from REST.  We also want to compare the dates.  The recording_date from REST should associate with START_TIME from Bb Data but they don't perfect align. Usuaully, the name and date are "good enough" for a positive match.

1. Copy columns A, B, C, and D from worksheet "rest"
2. Paste into columns N, O, P, and Q of worksheet "bb data"
3. Go to cell M2 in worksheet "bb data"
4. Paste this formula into cell M2 (include the equals sign): `=IF(AND(TEXT(J2,"MM/DD/YYYY")=TEXT(P2,"MM/DD/YYYY"),L2=O2),"","No Match")`
5. Copy cell M2 all the way to the last entry listed
6. Reconcile differences - a recording might exist in REST but not Bb Data or vice versa. Insert rows and adjust data down as needed. Be careful to keep data together (e.g. don't just copy down one cell, make sure you have all of them)
7. Save the file **recordings.xlsx**

# 4. Identify recording IDs to delete
Once you have the recording IDs in line with the courses and terms, you can sort and manipulate Excel to your heart's content.  Use your own methods for identifying *which* recordings are to be deleted.  Once you know this for certain, you are ready to delete them.

# 5. Use the Collaborate REST API to delete the specific recording IDs

1. Launch Notepad++
2. Open the file **delete_recordings.txt** in Notepad++
3. Paste in a line-delimited list of recording_ids (column N or worksheet "bb data" in the file **recordings.xlsx**)

Example:
```
5d2230c718384d439616a4dccd3d02a7
0532057f2f504578a58d1435e052d6c2
a5d966c7dddf463cbdeb6309a3e44583
18a58e0cfbff42429f7c18da3b6432ec
```

4. Save the file **delete_recordings.txt**
5. Open the file **delete_recordings.py**
6. Run the script

We processed about 18,000 deletions in about 45 minutes.

You can run either Step 1 or Step 2 (or both) to validate deletion.