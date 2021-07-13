# Publish Collaborate to Kaltura
Code snippets to help with your LTI tool.

#Assumptions
These code snippets do not include the oAuth via the LTI authentication from the LMS (assuming you know how to do that).

These session variables are used from the LTI POST data and need to be set/passed in from the oAuth:
- $_SESSION["collab_course_id"] = $_POST["context_label"];
- $_SESSION["collab_course_name"] = $_POST["context_title"];
- $_SESSION["collab_course_uuid"] = $_POST["context_id"];
- $_SESSION["collab_user_id"] = str_replace("@student.cscc.edu", "", str_replace("@cscc.edu", "", $_POST["lis_person_contact_email_primary"]));
- $_SESSION["collab_url"] = parse_url($_POST["launch_presentation_return_url"]);

# Before you Begin
1. Download the [Kaltura Client Library for PHP](https://developer.kaltura.com/api-docs/Client_Libraries) and place in the /_scripts/ folder.
2. Update the following files:

## _scripts/Collab.Constants.class.php
Enter your LTI credentials for your Collaborate LMS integration:
```
public $HOSTNAME = "";
public $KEY = "";
public $SECRET = "";
```
## _scripts/ajax_kaltura_publish.php
1. Ensure path to the client libraries is correct.
```
require_once("<PATH TO KALTURA CLIENT>KalturaClient.php");
```
2. Replace the appropriate placeholders with the Kaltura configuration data:
- <PARTNER_ID>
- <SERVICE_URL>
- <ADMIN_SECRET>
- <TIMEOUT_MS>
- <APP_ID>
```
		$config = new KalturaConfiguration(<PARTNER_ID>);
		$config->serviceUrl = "<SERVICE_URL>";
		$client = new KalturaClient($config);
		
		$ks = $client->session->start(
			"<ADMIN_SECRET>",
			NULL,
			KalturaSessionType::ADMIN,
			<PARTNER_ID>,
			<TIMEOUT_MS>,
			"appId:<APP_ID>");
		$client->setKS($ks);
```


## collab_list.php
1. Ensure path to the client libraries is correct.
```
require_once("<PATH TO KALTURA CLIENT>KalturaClient.php");
```
2. Replace the appropriate placeholders with the Kaltura configuration data:
- <PARTNER_ID>
- <SERVICE_URL>
- <ADMIN_SECRET>
- <TIMEOUT_MS>
- <APP_ID>
```
$config = new KalturaConfiguration(<PARTNER_ID>);
$config->serviceUrl = "<SERVICE_URL>";
$client = new KalturaClient($config);

$ks = $client->session->start(
	"<ADMIN_SECRET>",
	NULL,
	KalturaSessionType::ADMIN,
	<PARTNER_ID>,
	<TIMEOUT_MS>,
	"appId:<APP_ID>");
$client->setKS($ks);
```
# General Flow
1. collab_list.php uses the course_uuid to pull a list of recordings using Collaborate REST
2. Each recording's privacy status is reviewed to insure it is public
   - If private, then it cannot be published. "N/A" with a link to instructions on how to change privacy status are displayed.
   - If public, then it can be published. Additionally, chat transcripts may be downloaded.
3. Each recording makes a call to Kaltura to seek an existing upload the the recording_id that is owned by the contextual user
   - If an entry does exist, it displayed "Uploaded" and does not allow a publish
   - If an entry does not exist, then "Upload Now" links are provided
4. When a user clicks "Upload Now" the following occurs:
   - jQuery makes an AJAX call to ajax_collab_data.php
   - ajax_collab_data.php uses Collaborate REST to return the recording URL
   - jQuery calls publish_to_kaltura function which makes an AJAX call to ajax_kaltura_publish.php
   - ajax_kaltura_publish.php uses the Kaltura Client library to create an entry and load the recording URL into the entry
   - If the upload is successful, then the status on collab_list.php changes to "Processing"
5. When a user clicks "download" for a Chat transcript, the following occurs:
   - the recording ID is passed into ajax_collab_chat.php
   - ajax_collab_chat.php uses Collaborate REST to return the chat URL
   - the chat URL is consumed and formatted
   - a .txt file is returned for download
   
