<?php

	if(isset($_POST["recording_id"]) && isset($_POST["user_id"])) {
		require_once("Collab.Rest.class.php");
		require_once("Token.class.php");
		
		$rest = new Collab_Rest();
		$token = new Token();

		$token = $rest->authorize();
		$access_token = $token->access_token;
		
		$recording_data = $rest->get_recording_data($access_token, $_POST["recording_id"], "recording_url");		
		
		print_r($recording_data);
		
	} else {
		echo "failure";
	}

?>