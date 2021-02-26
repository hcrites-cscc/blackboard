# Cross-Linked Content
Cross-linked content are files in one course home directory that are being used by other courses or organizations.  Cross-linked files should be avoided.  

If the course with the shared file is deleted and the orphaned content folder is also deleted, then the links in the other courses will be broken and content lost.

## Getting a Broad Overview
In identifying cross-linked content, I begin with the query in "file locations - general.txt".  This query will identify the home directory being used for attachment and embeds in each of tjhe following object types:
- content attachments
- content embeds
- announcement embeds
- assessment embeds
- discussion board embeds
- discussion post embeds
- blog and journal embeds
- blog and journal entry embeds
- course banners

This query will also identify broken embeds (deleted files) as well as courses linking to /institution/ level content.

"file locations - general.txt" aggregates, so you will see the course pk1 value, the course id, the path being linked too, how many links were found, and the object type which contains the link to the file.

## Viewing the Specifics
You can use the results of "file locations - general.txt" to narrow your search.  Take the course pk1 and attachment path values from this query and narrow the search down in the appropriate object type subquery:
- file locations - content attachments.txt
- file locations - content embeds
- file locations - announcements.txt
- file locations - assessments.txt
- file locations - discussion forums.txt
- file locations - discussion posts.txt
- file locations - blogs.txt
- file locations - blog entries.txt
- file locations - course banners.txt

Each of these queries are a little different but each will show the specifics of the object containing file and the individual files found.


