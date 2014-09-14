<?php 

include 'simple_html_dom.php';
header('Content-Type: application/json');
$url = "http://localhost:8000";
$datasetUrl = "http://localhost/IR/dataset/";

$slash = "/";

$selected = "selected='selected'";

function httpPost($url,$params)
{
  $postData = '';
   //create name value pairs seperated by &
   foreach($params as $k => $v) 
   { 
      $postData .= $k . '='.$v.'&'; 
   }
   rtrim($postData, '&');
 
    $ch = curl_init();  
 
    curl_setopt($ch,CURLOPT_URL,$url);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
    curl_setopt($ch,CURLOPT_HEADER, false); 
    curl_setopt($ch, CURLOPT_POST, count($postData));
        curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);    
 
    $output=curl_exec($ch);
 	
    curl_close($ch);
    return $output;
 }

 if(isset($_GET['query']) && isset($_GET['type'])){
 	$params = array('query' => $_GET['query'],
 					'type' => $_GET['type'] );
 	echo httpPost($url,$params);
 }
 ?>


