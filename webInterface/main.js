var apiUrl = "http://"+window.location.hostname+"/IR/api.php";
var datasetUrl = "http://"+window.location.hostname+"/IR/dataset/";
var test;
function populate(list,data){
	if(data.length == 0){
		$(list).append("NO RESULTS");
		return;
	}
	for(key in data){
		var entry = $('<li></li>');
		var flrNum = parseInt(parseInt(data[key][0])/10000);
		var link = $('<a></a>').attr('href',datasetUrl+flrNum+"/"+data[key][0]).attr('target','_blank');
		link.append(data[key][0]);
		entry.append(link);
		$(entry).append(" - "+data[key][1]);
		$(list).append(entry);
		// $(list).append(" - "+data[key][1]);
	}
}
$("#tf").click(function(a){
	var query = $("#query").val();
	var type = 'tf';
	var params = { 'query':query, 'type':type };
	$.get(apiUrl,params,function(data) {

	list = $("#tf_result").children()[0];
	list.innerHTML = "";
	populate(list,data);

	});
});

$("#tfidf").click(function(a){
	var query = $("#query").val();
	var type = 'tfidf';
	var params = { 'query':query, 'type':type };
	
	$.get(apiUrl,params,function(data) {
		list = $("#tfidf_result").children()[0];
		list.innerHTML = "";
		populate(list,data);
	});
});

$("#bm25").click(function(a){
	var query = $("#query").val();
	var type = 'bm25';
	var params = { 'query':query, 'type':type };

	$.get(apiUrl,params,function(data) {
		list = $("#bm25_result").children()[0];
		list.innerHTML = "";
		populate(list,data);
	});
});

$("#reset").click(function(a){
	$("#bm25_result").children()[0].innerHTML = "";
	$("#tf_result").children()[0].innerHTML = "";
	$("#tfidf_result").children()[0].innerHTML = "";
});

