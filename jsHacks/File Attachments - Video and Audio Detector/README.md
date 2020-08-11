# About Video and Audio Detector

This jsHack will monitor file attachments or file embeds which contain one of a list of file extensions.  if a media file is ddetected, a lightbox will display prompting the user to use the "proper" method for embedding videos.

# Contents

- file_uload.1.2.zip is version 1.2 of the Video and Audio Detector
- email.php is a template to use if you wish to send email to support (etc)

# Customizations

There are a number of elements which should be customized in this jsHack

## media_extensions

In the cscc-file_upload.js file on line 1, you will find the list of file extensions.  These are pipe delimited.  Add or remove extensions as you see fit.  This list is for file attachments.

In the cscc-file_embed.js file on line 1, you will find the list of file extensions.  These are pipe delimited.  Add or remove extensions as you see fit.  This list is for file embeds.

## Message to End User

In the cscc-file_upload.js file on line 105, you will find the message which displays to the user when a media file is detected.  This message is for file attachments.  It accepts HTML (don't forget to use escape characters on single quotes).  You may also update line 103 (the title of the lightbox).

In the cscc-file_embed.js file on line 35, you will find the message which displays to the user when a media file is detected.  This message is for file embeds.  It accepts HTML (don't forget to use escape characters on single quotes). You may also update line 33 (the title of the lightbox).

## Email Options

If you wish for an email to be sent when someone is "caught" uploading media files, you will need to have some server-side code running on an external server to relay the email.  The file email.php provides a handy template using PHP.

Once the email relay is set-up on your server, update the following:
- In the cscc-file_upload.js file on line 118, replace [email_url] with the URL to the mail relay
- In the cscc-file_embed.js file on line 48, replace [email_url] with the URL to the mail relay
- In the cscc-file_upload.js file, uncomment line 70 and line 90
- In the cscc-file_embed.js file, uncomment line 19
