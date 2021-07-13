<?php

	session_start();
	
	if (isset($_SESSION["collab_course_id"])) {
		
		$course_id = $_SESSION["collab_course_id"];
		$course_name = $_SESSION["collab_course_name"];
		$course_uuid = $_SESSION["collab_course_uuid"];		
		$user_id = $_SESSION["collab_user_id"];
		$return_url = $_SESSION["collab_url"];
		
		$varTitle = "Upload Collaborate Recordings to My Media";
		
		echo "<html>
		<head>
			<title>$varTitle</title>
			<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'></script>
			<script type='text/javascript' src='_scripts/collab_list.js'></script>
		</head>
		<body>
			
		";
	
		require_once("_scripts/Collab.Rest.class.php"); 
		require_once("_scripts/Token.class.php");

		$rest = new Collab_Rest();
		$token = new Token();

		$token = $rest->authorize();
		$access_token = $token->access_token;

		$recordings = $rest->get_recording($access_token, $course_uuid);
			
		echo "<h1>".$varTitle."</h1>
		<h3 style='margin-top:0; padding-top:0;'>$course_id: $course_name</h3>";
		
		function is_json($string) {
			json_decode($string);
			return (json_last_error() == JSON_ERROR_NONE);
		}
		
		function get_kaltura_id($recording_uuid, $user_id) {
			require_once("<PATH TO KALTURA CLIENT>KalturaClient.php");

			$config = new KalturaConfiguration(<PARTNER_ID>);
			$config->serviceUrl = "<SERVICE_URL>";
			$client = new KalturaClient($config);
			
			$ks = $client->session->start(
				"<ADMIN_SECRET>",
				NULL,
				KalturaSessionType::ADMIN,
				<PARTNER_ID>,
				432000,
				"appId:<APP_ID>");
			$client->setKS($ks);
						
			$filter = new KalturaMediaEntryFilter();
			
			$filter->referenceIdIn = "Collaborate_".$recording_uuid;
			$filter->creatorIdEqual = $user_id;
			$filter->statusNotIn = 3;

			$pager = new KalturaFilterPager();

			$result = $client->media->listAction($filter, $pager);
			
			$entry_id = "";
			$entry_status = "";

			foreach($result->objects as $entry) {
				//$entry_id = $entry->id;
				switch($entry->status) {
					case 0: // Uploading
						$entry_id .= "Processing";
						break;
					case 1: // Converting
						$entry_id .= "Processing";
						break;
					case 2: // Ready
						$entry_id .= "Uploaded";
						break;
					case 3: // Deleted
						$entry_id .= "Deleted";
						break;
					default:
						$entry_id .= " (".$entry->status." status)";
						break;
					
				}
			}
			
			return $entry_id;
		}
		
		if(is_json($recordings)) {
			
			echo "<input type='hidden' name='user_id' id='user_id' value='".$user_id."' />
				<table cellspacing='0' cellpadding='0' summary='listing of Collaborate recordings for $course_id' class='tablesorter'>
				<thead>
					<tr>
						<th>Recording Name</th>
						<th>Created</th>
						<th>Duration</th>
						<th>Last Accessed</th>
						<th>My Media Status</th>
						<th>Chat Download</th>
					</tr>
				</thead>
				<tbody>";
			$recording_list = json_decode($recordings, true);
			
			$recording_id = array();
			
			$total_size = 0;
			
			foreach($recording_list["results"] as $recording) {			
				
				echo "<tr id='".$recording["id"]."'>
					<td class='recording_name'>".$recording["name"]."</td>
					<td class='recording_date'>".date("n/j/Y g:i A", strtotime($recording["created"]))."</td>
					<td>".round($recording["duration"] / 1000 / 60, 2)." minutes</td>
					<td>";
					if(array_key_exists("lastPlayback", $recording)) {
						//echo date("n/j/Y g:i A", strtotime($recording["lastPlayback"]))." (".$recording["playbackCount"].")";
						echo date("n/j/Y g:i A", strtotime($recording["lastPlayback"]));
					} else {
						echo "never";
					}
					echo "</td>
						<td class='recording_publish'>";
					if($recording["publicLinkAllowed"]=="1") {
						
						$entry_id = get_kaltura_id($recording["id"], $user_id);
						if($entry_id=="") {
							echo "<a href='#' class='publish'>Upload Now</a>";
						} else {
							echo $entry_id;
						}
						echo "</td>
							<td><a href='#' class='chat'>download</a></td>
						";
					} else {
						echo "N/A <a href='https://help.blackboard.com/api_collaborate/Ultra/Moderator/Moderate_Sessions/Recordings#share-your-recordings_OTP-10' target='_blank'>(how to fix)</a></td>
							<td>&nbsp;</td>";
					}
				echo "</tr>";
				
				$total_size += $recording["storageSize"];
							
			}
				
			echo "</tbody>
			</table>
			<p>Total Storage Size: <strong>";
			if($total_size / 1024 / 1024 > 1024) {
				echo round($total_size / 1024 / 1024 / 1024, 2)." Gb";
			} else {
				echo round($total_size / 1024 / 1024, 2)." Mb";
			}
			echo "</strong></p>";
			
		} else {
			echo "<p>This course has no Collaborate recordings.</p>";
			
		}
		
		echo "<p><a href=\"".$return_url."\" target=\"_parent\" class=\"btn btn-custom\">Return to Blackboard</a></p>
		</body>
		</html>";
							
  	} else {
		print "<p style=\"color:red\">Could not establish context: ".$context->message."<p>\n";
		exit;
	}

?>