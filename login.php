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
            <input type="password" id="password_form" name="password"><br>
            <input type="submit" value="Zaloguj się" id="login_butt">
            <!-- <button  -->
            <!-- <input type="submit" value="Zarejestruj się"> -->
            <?php 
            // echo "hello world!";
            
            
            // $db_name = "localhost";
            // // $db_host="root";
            // $db_user= "root";
            // $db_pass="";    
            // $db_name_db="prim_msgr";
            // $conn = new mysqli($db_name, $db_user, $db_pass, $db_name_db);
            // if ($conn->connect_error) {
            //     die("nie dziala". $conn->connect_error);
            //     // echo "nie dziala";
            // }
            // echo "</br>polaczone</br>";
            login();
        
        function login (){
            // print("testtesttest");
            
            $login_username = $_POST["login"];
            // print($login_username);
            $password_username = $_POST["password"];
            // print($password_username);
            $db_name = "localhost";
            // $db_host="root";
            $db_user= "root";
            $db_pass="";    
            $db_name_db="prim_msgr";
            $conn = new mysqli($db_name, $db_user, $db_pass, $db_name_db);
            if ($conn->connect_error) {
                die("nie dziala". $conn->connect_error);
                // echo "nie dziala";
            }
            else {
                print("</br>dziala</br>");
            }
            $query_check = "SELECT * FROM users WHERE 'Login' = {$login_username} AND 'Haslo' = {$password_username}";
            $result_check = mysqli_query($conn,$query_check);
            print($result_check);
            if ($result_check) {
                print("Zalogowano");
        }
    }
            ?>
        </form>
    </div>    
</body>
</html>