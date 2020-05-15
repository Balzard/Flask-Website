
  // main
  $(document).ready(function(){
    // fonction pour augmenter la quantité d'un matos
    $(".add").click(function(){
      // Récupérer l'id du matos
      var tmp = $(this).attr("id").replace("add","")
      // ajax pour ajouter une quantité au matos
      $.ajax({
        data : {
          id : tmp,
          case : "matos"
        },
        type : "POST",
        url : "/add",
        success : function(data){
          var quant = JSON.parse(data)
          // changer la quantite affichée
          $("#quant"+tmp).empty()
          $("#quant"+tmp).append(quant)
        }
      })
    })
    // fonction pour diminuer la quantite d'un matos
    $(".minus").click(function(){
      // récupérer l'id
      var tmp = $(this).attr("id").replace("minus","")
      // ajax pour diminuer la quant d'un matos
      $.ajax({
        data : {
          id : tmp,
          case : "matos"
        },
        type : "POST",
        url : "/minus",
        success : function(data){
          var quant = JSON.parse(data)
          // Attention si quantité <= 0
          if(quant <= "0"){
            alert("Ce produit n'est plus en stock. Supprimer le.")
          }
          // changer la quantite affichée
          $("#quant"+tmp).empty()
          $("#quant"+tmp).append(quant)
        }
      })
    })
  })