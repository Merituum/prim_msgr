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
            <input type="text" id="login_form" name="login"><br> <!-- changed type from "login" to "text" -->
            <label for="password_form">Hasło: </label><br>
            <input type="password" id="password_form" name="password"><br>
            <input type="submit" value="Zaloguj się" id="login_butt">
            <!-- <button  -->
            <input type="submit" value="Zarejestruj się" name="register">
            <?php 
                if(isset($_POST["register"])){
                    register(); 
                }
                else if(isset($_POST["login"])){
                    login();
                }
            ?>

        </form>
    </div>

    <?php
    function register() {
        $login_register = $_POST["login"];
        $password_register = $_POST["password"];
        // Assuming you have additional fields for registration like "question" and "answer"
        $question_question = $_POST["question"]; 
        $question_answer = $_POST["answer"];
        
        $db_name = "localhost";
        $db_user = "root";
        $db_pass = "";    
        $db_name_db = "prim_msgr";
        
        $conn = new mysqli($db_name, $db_user, $db_pass, $db_name_db);
        if ($conn->connect_error) {
            die("Nie można połączyć się z bazą danych: " . $conn->connect_error);
        }

        // Zabezpiecz dane przed SQL Injection
        $login_register = mysqli_real_escape_string($conn, $login_register);
        $password_register = mysqli_real_escape_string($conn, $password_register);
        $question = mysqli_real_escape_string($conn, $question_question);
        $answer = mysqli_real_escape_string($conn, $question_answer);

        // Sprawdzenie czy użytkownik o podanym loginie już istnieje
        $query_check = "SELECT * FROM Users WHERE Login = '$login_register'";
        $result_check = mysqli_query($conn, $query_check);
        if ($result_check && mysqli_num_rows($result_check) > 0) {
            echo "Taki użytkownik już istnieje";
        }
        else {
            $query_register = "INSERT INTO Users (Login, Haslo, PytaniePomocnicze, OdpowiedzNaPytanie) 
                    VALUES ('$login_register', '$password_register', '$question', '$answer')";
            $result_register = mysqli_query($conn, $query_register);
            if ($result_register) {
                session_start();
                $_SESSION['login'] = $login_register;
                header("Location: index.php");
                exit();
            }
            else {
                echo "Błąd!";
            }
        }
        mysqli_close($conn);
    }

    function login() {        
        $login_username = $_POST["login"];
        $password_username = $_POST["password"];
        
        $db_name = "localhost";
        $db_user = "root";
        $db_pass = "";    
        $db_name_db = "prim_msgr";
        
        $conn = new mysqli($db_name, $db_user, $db_pass, $db_name_db);
        if ($conn->connect_error) {
            die("Nie można połączyć się z bazą danych: " . $conn->connect_error);
        }
        
        // Zabezpiecz login i hasło przed SQL Injection
        $login_username = mysqli_real_escape_string($conn, $login_username);
        $password_username = mysqli_real_escape_string($conn, $password_username);

        $query_check = "SELECT * FROM Users WHERE Login = '$login_username' AND Haslo = '$password_username'";
        $result_check = mysqli_query($conn, $query_check);

        if ($result_check && mysqli_num_rows($result_check) > 0) {
            echo "Zalogowano pomyślnie.";
        } else {
            echo "Nieprawidłowy login lub hasło.";
        }
        mysqli_close($conn);
    }
    ?>

</body>
</html>
