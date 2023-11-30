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
        
        $("#log_in").click(function(){ // when click Log In button, hide the Sign Up elements, and display the Log In elements
            $("#title-login").toggleClass("hidden",false);
            $("#login-fieldset").toggleClass("hidden",false);
            $("#login-form-submit").toggleClass("hidden",false);
            $("#lost-password-link").toggleClass("hidden",false);
            $("#sign_up").toggleClass("active-button",true);
            $("#log_in").prop('disabled', true);
            
            $("#title-signup").toggleClass("hidden",true);
            $("#signup-fieldset").toggleClass("hidden",true);
            $("#signup-form-submit").toggleClass("hidden",true);
            $("#log_in").toggleClass("active-button",false);
            $("#sign_up").removeAttr("disabled");
                // Redirect to /login page
                window.location.href = "/login";
            
        });
    });