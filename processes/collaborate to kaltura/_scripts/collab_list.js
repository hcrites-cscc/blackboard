$(document).ready(function() {
	$(".publish").on("click", function() {
		var recording_id = $(this).parent().parent().attr("id");
		var recording_name = $("#"+recording_id).find(".recording_name").html();
		var recording_date = new Date($("#"+recording_id).find(".recording_date").html());
		recording_name += " ("+(recording_date.getMonth()+1)+"/"+(recording_date.getDate())+"/"+(recording_date.getFullYear())+")";
		$("#"+recording_id).find(".recording_publish").html("loading...");
		user_id = $("#user_id").val();
		$.ajax({
			type: "POST",
			url : "_scripts/ajax_collab_data.php",
			data: {"recording_id": recording_id, "user_id": user_id},
			success : function (data) {
				if(data=="forbidden") {
					alert("This recording is not public and cannot be transferred to Kaltura.");
					$("#"+recording_id).find(".recording_publish").html("forbidden");
				} else {
					publish_to_kaltura(user_id, recording_name, data, recording_id, recording_date)
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				alert(xhr.status+" - "+thrownError);
			}
		});
	});
	$(".chat").on("click", function() {
		var recording_id = $(this).parent().parent().attr("id");
		document.location = "_scripts/ajax_collab_chat.php?recording_id="+recording_id+"&recording_name="+$("#"+recording_id).find(".recording_name").html();
	});
});
function publish_to_kaltura(user_id, recording_name, recording_url, recording_uuid, recording_date) {
	$.ajax({
		type: "POST",
		url : "_scripts/ajax_kaltura_publish.php",
		data: {"user_id": user_id, "recording_name": recording_name, "recording_url": recording_url, "recording_uuid": recording_uuid, "recording_date": recording_date},
		success : function (data) {
			if(data!="failure") {
				$("#"+recording_uuid).find(".recording_publish").html("Processing");
			} else {
				$("#"+recording_uuid).find(".recording_publish").html("An Error Occurred");
			}
		},
		error: function (xhr, ajaxOptions, thrownError) {
			alert(xhr.status+" - "+thrownError);
		}
	});
}