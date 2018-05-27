<html>

Hi
<br>
Good  

<?php
$hour = date('G');
$date = date('G:i:s');

if ($hour > 6 and $hour < 13)  {echo "morning";} 
elseif ($hour > 13) {echo "afternoon";}
else {echo "evening";}

echo "</br>";
echo $date;
?>

</br>
<b>The end</b>


</html>