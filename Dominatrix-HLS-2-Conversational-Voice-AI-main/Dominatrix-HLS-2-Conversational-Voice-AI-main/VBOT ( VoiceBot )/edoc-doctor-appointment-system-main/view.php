$sql = "SELECT * FROM edoc";
$result = $database->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "Column1: " . $row["column1"]. " - Column2: " . $row["column2"]. " - Column3: " . $row["column3"]. "<br>";
    }
} else {
    echo "0 results";
}
