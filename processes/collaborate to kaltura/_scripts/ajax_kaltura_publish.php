<?php

	if(isset($_POST["user_id"]) && isset($_POST["recording_name"]) && isset($_POST["recording_url"]) && isset($_POST["recording_uuid"]) && isset($_POST["recording_date"])) {
		require_once("<PATH TO KALTURA CLIENT>KalturaClient.php");

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
		
		$uploadToken = new KalturaUploadToken();
		$token = $client->uploadToken->add($uploadToken);

		$mediaEntry = new KalturaMediaEntry();
		$mediaEntry->mediaType = KalturaMediaType::VIDEO;
		$mediaEntry->name = htmlspecialchars_decode($_POST["recording_name"]);
		$mediaEntry->description = "Collaborate Recording ID: ".$_POST["recording_uuid"]."\nMeeting Time: ".$_POST["recording_date"];
		$mediaEntry->referenceId = "Collaborate_".$_POST["recording_uuid"];
		$mediaEntry->tags = "collaborate_recording";
		$mediaEntry->userId = $_POST["user_id"];

		$entry = $client->media->add($mediaEntry);
		$entryId = $entry->id;

		$resource = new KalturaUrlResource();
		$resource->url = $_POST["recording_url"];
		$result = $client->media->addContent($entryId, $resource);

		print($entryId);
		
	} else {
		echo "failure";
	}

?>