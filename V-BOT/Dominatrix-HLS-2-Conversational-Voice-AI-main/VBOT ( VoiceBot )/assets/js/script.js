function auth() {
    var email = document.getElementById("username").value;
    var password = document.getElementById("pwd").value;
    if(email === "VBot" && password === "vbot@2023"){
        window.location.assign("index1.html");
        // alert("Welcome !");
    }
    else{
        alert("Invalid Credentials, Please enter correct Username or Password");
        return;
    }
}