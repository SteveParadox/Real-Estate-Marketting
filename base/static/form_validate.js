$(document).ready(function() {
  $("#submit").click(function() {
    var name = $("#name").val();
    var email = $("#email").val();
    var pass = $("#password").val();
    var phone_no = $("#phone_no").val();

    if(name.length == "")
      {
        $("#p1").text("Please enter your              name");
        $("#name").focus();
        return false;
      }
    else if(email.length == "")
      {
        $("#p2").text("Please enter your              email address");
        $("#email").focus();
        return false;
      }
    else if(pass.length == "")
      {
        $("#p3").text("Please enter your              password");
        $("#Password").focus();
        return false;
      }
      else if(phone_no.length == "")
      {
        $("#p4").text("Please enter your              phone number");
            $("#phone_no").focus();
        return false;
      }
    else
      {
        var con = confirm("Are you done?");
        if(con == true)
          {
            alert("Welcome to our website");
            return true;
          }
        else
          {
            return false;
          }
      }
  });

});

