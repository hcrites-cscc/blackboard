<?php

	if(isset($_GET["recording_id"]) && isset($_GET["recording_name"])) {
		require_once("Collab.Rest.class.php");
		require_once("Token.class.php");
		
		$rest = new Collab_Rest();
		$token = new Token();

		$token = $rest->authorize();
		$access_token = $token->access_token;
		
		$get_recording_chat = $rest->get_recording_data($access_token, $_GET["recording_id"], "chat_url");
		
		header("Content-type: text/plain");
		header("Content-Disposition: attachment; filename=chat_".$_GET["recording_name"].".txt");
		
		echo "Comment Time\tRecording Time\tUser\tComment\tAudience\tGroup (if applicable)\n";
		
		foreach($get_recording_chat as $chat) {
			$chat_url = $chat["url"];
			$chat_contents = file_get_contents($chat_url);
			$chat_json = json_decode($chat_contents, true);	
								
			foreach($chat_json as $chat_entry) {
				echo date("n/j/Y g:i:s A", $chat_entry["eventTime"]/1000)."\t".
					$chat_entry["relativeEventTime"]."\t".
					$chat_entry["userName"]."\t".
					$chat_entry["body"]."\t".
					$chat_entry["targetType"]."\t".
					$chat_entry["groupName"]."\n";			
			}
		}
		
	} else {
		echo "failure";
	}

?>