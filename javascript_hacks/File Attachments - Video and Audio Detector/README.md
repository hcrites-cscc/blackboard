# About Video and Audio Detector

This jsHack will monitor file attachments or file embeds which contain one of a list of file extensions.  If a media file is ddetected, a lightbox will display prompting the user to use the "proper" method for embedding videos.

This works in numerous places, including announcements, content, forums, blogs, journals, and assessments.  It will let instructor attachments to an assignment through, but will generate an email if it is enabled.  Users can still upload directly into the content collection.  We have not had issues with attachments/embeds in Grade Center feedback, so this does not address this spot.

# Contents

- file_upload.1.2.zip is version 1.2 of the Video and Audio Detector which is used with the pre-3900.0.0 content editor
- file_upload.1.3.zip is version 1.3 of the Video and Audio Detector which is used with the 3900.0.0+ content editor
- file_upload.1.3-ubn.zip is an Ultra Base Nav version of 1.3 with "Learning System Page" selected for the rendering hook (many thanks to Chris Bray for making the modifications)
- email.php is a template to use if you wish to send email to support (etc)

# Customizations

There are a number of elements which should be customized in this jsHack.

## Scope
This hack is focused on non-student roles.  If you want to use this on students as well, you can make the change in the Javascript Hacks Manager.

## Media Extensions

file_upload.1.2.zip
In the cscc-file_upload.js file on line 1, you will find the list of file extensions.  These are pipe delimited.  Add or remove extensions as you see fit.  This list is for file attachments.

In the cscc-file_embed.js file on line 1, you will find the list of file extensions.  These are pipe delimited.  Add or remove extensions as you see fit.  This list is for file embeds.

file_upload.1.3.zip

In the cscc-file_upload.js file on line 1, you will find the list of file extensions.  These are pipe delimited.  Add or remove extensions as you see fit.  This list is for file attachments.

## Message to End User

file_upload.1.2.zip

In the cscc-file_upload.js file on line 105, you will find the message which displays to the user when a media file is detected.  This message is for file attachments.  It accepts HTML (don't forget to use escape characters on single quotes).  You may also update line 103 (the title of the lightbox).

In the cscc-file_embed.js file on line 35, you will find the message which displays to the user when a media file is detected.  This message is for file embeds.  It accepts HTML (don't forget to use escape characters on single quotes). You may also update line 33 (the title of the lightbox).

file_upload.1.3.zip

In the cscc-file_upload.js file on line 114, you will find the message which displays to the user when a media file is detected.  This message is for file attachments.  It accepts HTML (don't forget to use escape characters on single quotes).  You may also update line 123 (the title of the lightbox).


## Email Options

If you wish for an email to be sent when someone is "caught" uploading media files, you will need to have some server-side code running on an external server to relay the email.  The file email.php provides a handy template using PHP.

Once the email relay is set-up on your server, update the following:

file_upload.1.2.zip

- In the cscc-file_upload.js file on line 118, replace [email_url] with the URL to the mail relay
- In the cscc-file_embed.js file on line 48, replace [email_url] with the URL to the mail relay
- In the cscc-file_upload.js file, uncomment line 70 and line 90
- In the cscc-file_embed.js file, uncomment line 19

file_upload.1.3.zip
- In the cscc-file_upload.js file on line 127, replace [email_url] with the URL to the mail relay
- In the cscc-file_upload.js file, uncomment line 79 and line 99


## Email.php
Within the email template, you will need to change the following:
- On line 8, change [domain] to your Blackboard DNS.  This is optional, but you can include a link to the Course Home Directory in your email if you like.
- On line 30, change the email address of the recipent
- On line 31, change the email subject
- On lines 32-37, customize the message
- On line 40, change the email address of the recipient (this one goes in the email's Headers)
- On line 41, change who the email is from (default is the end user who attempted to upload the file(s))
- On line 42, change the cc: email(s) and/or uncomment it; separate more than one with a comma
- On line 43, change the bcc: email(s) and/or uncomment it; separate more than one with a comma
