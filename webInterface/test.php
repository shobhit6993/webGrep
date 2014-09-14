<?php 
include 'simple_html_dom.php';

$html = file_get_html('http://localhost/IR/dataset/0/0');
$ret = $html->find('title',0);
echo "<pre>";
var_dump($ret->plaintext);
echo "</pre>";

 ?>