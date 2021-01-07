<?php  

	$varEmailBody = "";
	
	$course = "";
	if(isset($_POST["course"])) {
		$course = $_POST["course"];
		$url = "https://[domain]/webapps/cmsmain/webui/courses/".$course;
	}
	$role = "";
	if(isset($_POST["role"])) {
		$role = $_POST["role"];
	}
	$email = "";
	if(isset($_POST["email"])) {
		$email = $_POST["email"];
	}
	$name = "";
	if(isset($_POST["name"])) {
		$name = $_POST["name"];
	}
	$files = "";
	if(isset($_POST["files"])) {
		$files = $_POST["files"];
	}
	
	$varNow = new DateTime;
	
	if($email != "") {
		$varTo = "IT Support Center <user@school.edu>";
		$varSubject = "Kaltura Assistance";
		$varMessage = "<p>Name: ".$name."</p>
			<p>Email: ".$email."</p>
			<p>Course: ".$course."</p>
			<p>Role: ".$role."</p>
			<p>Time: ".$varNow->format("n/j/Y g:i A")."</p>
			<ul>".$files."</ul>";
				
		$varHeaders = 'Content-type: text/html; charset=iso-8859-1' . "\r\n";
		$varHeaders .= 'To: IT Support Center <user@school.edu>'. "\r\n";
		$varHeaders .= 'From: '.$name.' <'.$email.'>' . "\r\n";
//		$varHeaders .= 'Cc: user@school.edu'."\r\n";		
		$varHeaders .= 'Bcc: user@school.edu'."\r\n";		
	
		if(mail($varTo, $varSubject, $varMessage, $varHeaders)) {
			echo "success";
		} else {
			echo "failure";
		}
	}

?>
