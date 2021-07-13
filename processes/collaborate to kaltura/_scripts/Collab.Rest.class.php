<?php
require_once 'Collab.Constants.class.php';

class Collab_Rest {

	public $constants = '';
	
	public function authorize() {
		
		$constants = new Collab_Constants();
		$token = new Token();
		
		$expiration = new DateTime("+5 minutes");
		$expiration = $expiration->getTimestamp();
		#$expiration->setTimezone(new DateTimeZone("UTC"));
		#$expiration = $expiration->format("Y-m-d H:i:s");
		
		$header = json_encode([
			"typ" => "JWT",
			"alg" => "HS256"   
		]);
			
		$claims = json_encode([
			"iss"=>$constants->KEY ,
			"sub"=>$constants->KEY ,
			"exp"=>$expiration
		]);
						
		$encoded_header = trim(str_replace(['+','/','='], ['-','_',''], base64_encode($header)), "=");
		$encoded_claims = trim(str_replace(['+','/','='], ['-','_',''], base64_encode($claims)), "=");
	
		$signature = hash_hmac("sha256", $encoded_header.".".$encoded_claims, $constants->SECRET, true);
		$encoded_signature = trim(str_replace(['+','/','='], ['-','_',''], base64_encode($signature)), "=");
		
		$assertion = $encoded_header.".".$encoded_claims.".".$encoded_signature;
			
		$payload = array(
			"grant_type" => "urn:ietf:params:oauth:grant-type:jwt-bearer",
			"assertion" => $assertion
		);
		
		$request = curl_init($constants->HOSTNAME.$constants->AUTH_PATH);
		curl_setopt($request, CURLOPT_POST, true);								// Performs a regular HTTP POST		
		curl_setopt($request, CURLOPT_POSTFIELDS, http_build_query($payload));	//The full data being posted in HTTP POST
		curl_setopt($request, CURLOPT_RETURNTRANSFER, 1); 						// Pass TRUE or 1 if you want to wait for and catch the response against the request made
		curl_setopt($request, CURLOPT_VERBOSE, 1);								// For Debug mode; shows up any error encountered during the operation

				
		try {
			$response["VER"] = curl_version();
			$response["EXE"] = curl_exec($request);
			$response["INF"] = curl_getinfo($request);
			$response["ERR"] = curl_error($request);	
			
			if(!$response["EXE"]){die("Connection Failure");}
									
			if (200 == $response["INF"]["http_code"]) {
				$token = json_decode($response["EXE"]);
			} else {
				print "Unexpected HTTP status: ".$response["INF"]["http_code"]." ".$response["INF"];
				$BbRestException = json_decode($response["EXE"]);
				var_dump($BbRestException);
			}
			
			curl_close($request);
			
		} catch (Exception $e) {
			print 'Error: ' . $e->getMessage();
		}
		
		return $token;
	}	
	
	public function get_recording($access_token, $course_uuid) {
		$constants = new Collab_Constants();
		$recording = "";
		
		$payload = array(
			"contextExtId" => $course_uuid,
			"limit" => 200
		);
		
		$url = $constants->HOSTNAME.$constants->RECORDING_PATH."?".http_build_query($payload);
		
		$request = curl_init($url);
		curl_setopt($request, CURLOPT_HTTPHEADER, array("Authorization: Bearer ".$access_token, "Content-Type: application/json", "Accept: application/json"));
		curl_setopt($request, CURLOPT_URL, $url);					
		curl_setopt($request, CURLOPT_CUSTOMREQUEST, "GET");		
		curl_setopt($request, CURLOPT_RETURNTRANSFER, 1); 			
		curl_setopt($request, CURLOPT_VERBOSE, 1);
			
		try {
			$response["VER"] = curl_version();
			$response["EXE"] = curl_exec($request);
			$response["INF"] = curl_getinfo($request);
			$response["ERR"] = curl_error($request);	
			
			if(!$response["EXE"]){die("Connection Failure");}
									
			if (200 == $response["INF"]["http_code"]) {
				$recording = $response["EXE"];
			} else {
				print "Unexpected HTTP status: ".$response["INF"]["http_code"]." ";
				print_r($response["INF"]);
				$BbRestException = json_decode($response["EXE"]);
				var_dump($BbRestException);
			}
			
			curl_close($request);
			
		} catch (Exception $e) {
			print 'Error: ' . $e->getMessage();
		}
	
		return $recording;
	}
		
	public function get_recording_data($access_token, $recording_uuid, $info) {
		$constants = new Collab_Constants();
		$recording_data = "";
				
		$url = $constants->HOSTNAME.$constants->RECORDING_PATH."/".$recording_uuid."/data";
		//$url = $constants->HOSTNAME.$constants->RECORDING_PATH."/".$recording_uuid."/url";
		
		$request = curl_init($url);
		curl_setopt($request, CURLOPT_HTTPHEADER, array("Authorization: Bearer ".$access_token, "Content-Type: application/json", "Accept: application/json"));
		curl_setopt($request, CURLOPT_URL, $url);					
		curl_setopt($request, CURLOPT_CUSTOMREQUEST, "GET");		
		curl_setopt($request, CURLOPT_RETURNTRANSFER, 1); 			
		curl_setopt($request, CURLOPT_VERBOSE, 1);
			
		try {
			$response["VER"] = curl_version();
			$response["EXE"] = curl_exec($request);
			$response["INF"] = curl_getinfo($request);
			$response["ERR"] = curl_error($request);	
			
			if(!$response["EXE"]){die("Connection Failure");}
									
			if (200 == $response["INF"]["http_code"]) {
				$response = json_decode($response["EXE"], true);
				if($info=="recording_url") {
					//$recording_data = $response["mediaDownloadUrl"];
					//$recording_data = $response["streams"]["WEB"];
					//$recording_data = $response["url"];
					$recording_data = $response["extStreams"][0]["streamUrl"];
				} else if($info=="chat_url") {
					$recording_data = $response["chats"];
				}
				
			} else {
				#print "Unexpected HTTP status: ".$response["INF"]["http_code"]." ";
				#print_r($response["INF"]);
				$response = json_decode($response["EXE"], true);
				$recording_data = $response["errorKey"];

			}
			
			curl_close($request);
			
		} catch (Exception $e) {
			print 'Error: ' . $e->getMessage();
		}
	
		return $recording_data;
	}

}
