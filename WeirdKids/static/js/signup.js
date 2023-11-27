$(document).ready(function(){

    //--------- change color value of the form text/password inputs -----
    
      const textInputs =  $("input[type='textbox']");
      const passwordsInputs =  $("input[type='password']");
      //--------- Login screen swicth -----
    
        $("button").click(function(event){  //  prevent buttons in form to reload
            event.preventDefault();
        });
        
        $("a").click(function(event){  //  prevent 'a' links in form to reload
            event.preventDefault();
        });
    
        $("#sign_up").click(function(){ // when click Sign Up button, hide the Log In elements, and display the Sign Up elements
            $("#title-login").toggleClass("hidden",true);
            $("#login-fieldset").toggleClass("hidden",true);
            $("#login-form-submit").toggleClass("hidden",true);
            $("#lost-password-link").toggleClass("hidden",true);
            $("#sign_up").toggleClass("active-button",false);
            $("#log_in").removeAttr("disabled");
            
            $("#title-signup").toggleClass("hidden",false);
            $("#signup-fieldset").toggleClass("hidden",false);
            $("#signup-form-submit").toggleClass("hidden",false);
            $("#log_in").toggleClass("active-button",true);
            $("#sign_up").prop('disabled', true);
                // Redirect to /signup page
                window.location.href = "/signup";
        });
        
    });