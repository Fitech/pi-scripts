<!DOCTYPE HTML>
<html>
<head>
</head>
<body>
<span>
<?php

$username="root";
$password="WatchTheOilBurner451";
$database="temperatures";

if ($_POST["date-range-select"] == "1day")
{
  $dateRange = '-1 day';
}
else if ($_POST["date-range-select"] == "2day")
{
    $dateRange = "-2 day";
}
else if ($_POST["date-range-select"] == "3day")
{
    $dateRange = "-3 day";
}
else if ($_POST["date-range-select"] == "week")
{
    $dateRange = "-7 day";
}
else
{
    $dateRange = "-2 day";
}

$currenttime= date("Y-m-d H:i:s");
$startOfRange = date('Y-m-d H:i:s', strtotime($dateRange, strtotime($currenttime)));

mysql_connect(localhost,$username,$password);
@mysql_select_db($database) or die( "Unable to select database");

$query="SELECT * FROM tempLog WHERE datetime >'" . $startOfRange . "'";
$result=mysql_query($query);

$num=mysql_numrows($result);

mysql_close();

$tempValues = array();
$burner = array();

$i=0;

$readingAB = "A";
$tempA = 0;
$tempB = 0;

while ($i < $num)
{
	$dateAndTemps = array();
	$dateAndBurner = array();
	$datetime=mysql_result($result,$i,"datetime");
	$temp=mysql_result($result,$i,"temperature");
	$burnerOn=mysql_result($result,$i,"burner_on");

	$tempInt=intval($temp);

	$dateAndTemps[x] = (strtotime($datetime))*1000;
	$dateAndTemps[y] = $tempInt;

	$dateAndBurner[x] = (strtotime($datetime))*1000;
  
  if ( $readingAB == "A" )
  {
    $tempA = $tempInt;
    $tempB = $tempB + .5;
    if ( $tempA > $tempB)
    {
      $dateAndBurner[y] = 200;
    }
    else
    {
      $dateAndBurner[y] = 0;
    }
    $nextRead = "B";
  }
  else
  {
    $tempB = $tempInt;
    $tempA = $tempA + .5;
    if ( $tempB > $tempA)
    {
      $dateAndBurner[y] = 200;
    }
    else
    {
      $dateAndBurner[y] = 0;
    }
    $nextRead = "A";
  }
  
  $readingAB = $nextRead;
  $burner[$i]=$dateAndBurner;
	$tempValues[$i]=$dateAndTemps;
	$i++;
}

$tempsjson = json_encode($tempValues);
$burnerjson = json_encode($burner);
?>
</span>
<div class="date-range">
  <form method="post">
    <label for="date-range-select">Date Range:</label>
    <select name="date-range-select">
      <option <?php if ($dateRange == '-1 day') echo 'selected'; ?> value="1day">Last 24 Hours</option>
      <option <?php if ($dateRange == '-2 day') echo 'selected'; ?> value="2day">Last 2 Days</option>
      <option <?php if ($dateRange == '-3 day') echo 'selected'; ?> value="3day">Last 3 Days</option>
      <option <?php if ($dateRange == '-7 day') echo 'selected'; ?> value="week">Last Week</option>
    </select>
    <button type="submit">Go</button>
  </form>
</div>
<div id="tempChart" style="height: 700px; width: 100%;"></div>
</body>
<footer>
  <script type="text/javascript">
  window.onload = function () {
    var chart1 = new CanvasJS.Chart("tempChart",
      {
        zoomEnabled: true,
        title:{
          text: "Temperature Over Time"
        },
        axisX:{  
          title: "time",
          labelAngle: -35,
          valueFormatString: "DDD - H:mm",
    labelFormatter: function (e) {
                  return CanvasJS.formatDate( e.value, "DDD H:mm");
              },
  },
  axisY:{
    maximum: 200,
    gridThickness: 2
  },
  dataPointWidth: 2,
         data: [
                {
            toolTipContent: null,
            type: "column",
            xValueType: "dateTime",
            color: "rgba(255,0,0,.5)",
            dataPoints: <?php echo $burnerjson ?>
          },
          {
            xValueFormatString: "DDD H:mm",
            type: "area",
            color: "rgba(0,0,255,.5)",
            xValueType: "dateTime",
            dataPoints: <?php echo $tempsjson; ?>
          }
        ]
      });
    chart1.render();
  }
</script>
<script type="text/javascript" src="/alt-canvasjs/canvasjs-1.8.0/canvasjs.min.js"></script>
</footer>
</html>
