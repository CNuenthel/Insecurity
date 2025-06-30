<!DOCTYPE html>
<html>
<head>
    <title>Simulated WebShell</title>
</head>
<body style="background-color: black; color: lime; font-family: monospace;">
    <h2>Welcome to your WebShell</h2>
    <form method="GET">
        <label for="cmd">Enter command:</label><br>
        <input type="text" name="cmd" id="cmd" autofocus>
        <input type="submit" value="Execute">
    </form>

    <hr>

    <?php
    if (isset($_GET['cmd'])) {
        echo "<pre>Simulated execution: " . htmlspecialchars($_GET['cmd']) . "</pre>";
    }
    ?>
</body>
</html>
