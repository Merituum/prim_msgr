<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="login.css">
    <title>Prim - messenger: REJESTRACJA</title>
</head>
<body>

    <div class="register_window">
        <form method='post'>


            <input type="submit" name="return_login" id="return_login" onclick="return_login()" value="Powrót do logowania"><br>

            <label for="login_form">Login: </label><br>
            <input type="text" id="login_form" name="login_register"><br> 

            <label for="password_form">Hasło: </label><br>
            <input type="password" id="password_form" name="password_register"><br>

            <label for="password_conf" id="password_conf" name="pass_conf">Powtórz hasło</label><br>
            <input type="password"  id="password_form_conf" name="password_conf_register"><br>

            <label for="sec_quest" id="sec_quest" name="sec_quest">Pytanie Pomocnicze</label><br>
            <input type="text" id="sec_quest" name="sec_quest_register"><br>

            <label for="sec_ans" id="sec_ans" name="sec_ans">Odpowiedz na pytanie</label><br>
            <input type="password" id="sec_ans" name="sec_ans_register"><br>    

            
            <!-- <input type="submit" value="Zaloguj się" id="login_butt"> -->
            <!-- <button  -->
            <input type="submit" value="Zarejestruj się" name="register" onclick="register()">

        </form>
    </div>



<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['return_login'])) {
        header("Location: login.php");
        exit();
    }
    
    if (isset($_POST['register'])) {
        register();
    }
}

function register() {
    $login_register = $_POST["login_register"];
    $password_register = $_POST["password_register"];
    $password_conf_register = $_POST["password_conf_register"];
    $question_register = $_POST["sec_quest_register"]; 
    $answer_register = $_POST["sec_ans_register"];

    if ($password_register !== $password_conf_register) {
        echo "Passwords do not match!";
        return;
    }

    $db_host = "localhost";
    $db_user = "root";
    $db_pass = "";    
    $db_name = "prim_msgr";

    $conn = new mysqli($db_host, $db_user, $db_pass, $db_name);
    if ($conn->connect_error) {
        die("Nie można połączyć się z bazą danych: " . $conn->connect_error);
    }

    $login_register = $conn->real_escape_string($login_register);
    $password_register = $conn->real_escape_string($password_register);
    $question_register = $conn->real_escape_string($question_register);
    $answer_register = $conn->real_escape_string($answer_register);

    $query_check = "SELECT * FROM Users WHERE Login = '$login_register'";
    $result_check = $conn->query($query_check);
    if ($result_check->num_rows > 0) {
        echo "Taki użytkownik już istnieje";
    } else {
        $query_register = "INSERT INTO Users (Login, Haslo, PytaniePomocnicze, OdpowiedzNaPytanie) 
                VALUES ('$login_register', '$password_register', '$question_register', '$answer_register')";
        if ($conn->query($query_register) === TRUE) {
            $_SESSION['login'] = $login_register;
            header("Location: index.php");
            exit();
        } else {
            echo "Błąd: " . $conn->error;
        }
    }
    $conn->close();
}
?>

</body>
</html>