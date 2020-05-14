//  fonction pour vérifer si ancien mot de passe écrit
    function verif(){
      // Vérifier si un nouveau mdp est écrit
      var tmp = $("#new_password_1").val()
      if(tmp == ""){
        return true;
      }else{
        var old = $("#old_password").val()
        if(old == ""){
          alert("Vous devez mentionner l'ancien mot de passe.")
          return false;
        }
      }
    }
    $(document).ready(function(){
      // ajout d'un paramètre a submit
      $("#submit").attr("onclick", "return verif()")
    })