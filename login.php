<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="login.css">
    <title>Logowanie</title>
</head>
<body>
    <div class="login_window">
         <form method='post'>
            <label for="login_form">Login: </label><br>
            <input type="login" id="login_form" name="login"><br>
            <label for="password_form">Hasło: </label><br>
            <input type="password" id="password_form" name="password">
    
            <?php 
            echo "hello world!"
            ?>
        </form>
    </div>    
</body>
</html>