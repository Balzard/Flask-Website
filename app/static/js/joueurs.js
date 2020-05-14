  // main function
  $(document).ready(function(){
    // changer le status d'un joueur
    $("#playerTable").on("click", ".status", function(){
      // récupérer l'id du jouer
      var tmp = $(this).attr("id").replace("status", "")
      // Ajax pour changer le joueur avec 3 retours selon le nouveau statut du joueur
      // 1 : admin -- 0 : membre -- 2 : le joueur est lui-même
      $.ajax({
        data : {
          id : tmp
        },
        type : "POST",
        url : "/changeStatus",
        success : function(data){
          var res = JSON.parse(data)
          // changer son status
          if(res == 2){
            alert("Vous ne pouvez pas changer votre propre status.")
          }else{
            $("#status"+tmp).empty()
            if(res == 1){
              $("#status"+tmp).append("ADMIN")
            }else if(res == 0){
              $("#status"+tmp).append("MEMBRE")
            }
          }
        }
      })
    })
  })