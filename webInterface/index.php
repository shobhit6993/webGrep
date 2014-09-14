<!DOCTYPE html>
<html>
<head>
	<title>webGrep</title>
	<script src="jquery.js" type="text/javascript" charset="utf-8"></script>		
	</style>
</head>
<body>
<div id="main_div">
	<div id="main_form">
	  webGrep <br>
	  <input type="search" name="query" id="query">
	  <br>
	  <button type="button" id='tf'>TF</button>
	  <button type="button" id='tfidf'>TF-IDF</button>
	  <button type="button" id='bm25'>BM25</button>  
	  <br>
	  <button type="reset" id='reset'>Reset</button>  
	</div>

	<div id='wrapper'>
		<div class="row">
			<div class='table_heads'>
				TF
			</div>
			<div class='table_heads'>
				TF - IDF
			</div>
			<div class='table_heads'>
				BM-25
			</div>
		</div>
		<div class="row">
	  		<div id='tf_result' >
	  			<ol>
	  				
	  			</ol>
	  		</div>
	  		<div id='tfidf_result'>
	  			<ol>
	  				
	  			</ol>
	  		</div>
	  		<div id='bm25_result'>
	  			<ol>
	  				
	  			</ol>
	  		</div>
	  	</div>
	</div>
</div>
<script src="main.js" type="text/javascript" charset="utf-8" ></script>
<link rel="stylesheet" type="text/css" href="style.css">
</body>

</html>