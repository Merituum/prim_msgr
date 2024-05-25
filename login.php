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
    function register(){
        header("Location: register.php");
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
            $_SESSION['login']=$login_username;
            header("Location: index.php");
        } else {
            echo "Nieprawidłowy login lub hasło.";
        }
        mysqli_close($conn);
    }
    ?>

</body>
</html>
