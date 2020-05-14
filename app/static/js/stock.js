 // Function to add a product row
    function addStock(prodJS){
      //
      var id = prodJS.id;
      var nom = prodJS.nom;
      var quantite = prodJS.quantite;
      var type = prodJS.type;
      var tarif = prodJS.tarif;
      // Add a row
      var tmp = "<tr id=prod"+id+"></tr>"
      $("#stockTable").append(tmp)
      // add the cells
      tmp = "<td>"+nom+"</td>"
      $("#prod"+id).append(tmp)
      tmp = "<td>"+type+"</td>"
      $("#prod"+id).append(tmp)
      var id_quant = "quant"+id
      tmp = "<td id="+id_quant+">"+quantite+"</td>"
      $("#prod"+id).append(tmp)
      // option delete
      var url = "/deleteProd/id="+id
      var tempo_del = "<a class='btn btn-danger' href="+url+">Delete</a>"
      // option edit
      url = "/editProduct/id="+id
      var tempo_edit = "<a class='btn btn-primary' href="+url+">Edit</a>"
      // add option
      var id_add = "add"+id
      tempo_add = "<a href='#+' class='add btn btn-secondary' id="+id_add+">+</a>"
      // minus option
      var id_minus = "minus"+id
      tempo_minus = "<a href='#-' class='minus btn btn-secondary' id="+id_minus+">-</a>"
      // ajout de la cellule complete
      // Cell for options
      tmp = "<td>"+tempo_del+" "+tempo_edit+" "+tempo_add+" "+tempo_minus+"</td>"
      $("#prod"+id).append(tmp)
    }
    // main fonction
    $(document).ready(function(){
      // function to look for a type of products
      $("#search").click(function(){
        var tmp = $("#searchInput").val();
        if(tmp == ""){
          alert("Nothing to look for.");
        }else{
          // Ajax to see if the type searched exists
          $.ajax({
            data : {
              name : tmp
            },
            type : "POST",
            url : "/confirmType",
            success : function(data){
              var res = JSON.parse(data);
              if(res){
                // Step 1 : remove the current rows of the table comment
                $("#stockTable").find("tr:gt(0)").remove();
                // Step 2 : take the comms id from the type
                $.ajax({
                  data : {
                    name : tmp
                  },
                  type : "POST",
                  url : "/prodsFromType",
                  success : function(data){
                    var idList = JSON.parse(data);
                    // Change the type
                    $("h3").empty()
                    $("h3").append("Produits du type "+tmp)
                    // Work for each comm
                    $.each(idList, function(index, value){
                      // Take the info about the comm
                      $.ajax({
                        data :{
                          id : value
                        },
                        type : "POST",
                        url : "/infoProd",
                        success : function(data){
                          prodJS = JSON.parse(data);
                          addStock(prodJS);
                        }
                      })
                    })
                  }
                })
              }else{
                alert("No products related to this type.")
              }
            }
          })
        }
      })
      // function to look for all the products
      $("#all").click(function(){
        // Step 1 : remove the current rows of the table comment
        $("#stockTable").find("tr:gt(0)").remove();
        // Take the id of all the comments
        $.ajax({
          type : "POST",
          url : "/allProd",
          success : function(data){
            // Change the type
            $("h3").empty()
            $("h3").append("Tous les produits.")
            var idList = JSON.parse(data);
            $.each(idList, function(index, value){
              // Take the info about the comm
              $.ajax({
                data :{
                  id : value
                },
                type : "POST",
                url : "/infoProd",
                success : function(data){
                  prodJS = JSON.parse(data);
                  addStock(prodJS);
                }
              })
            })
          }
        })
      })
      // function to add a quantity of a product
      $("#stockTable").on("click", ".add", function(){
        var tmp = $(this).attr("id").replace("add", "")
        // ajax to add a quantite and return the total
        $.ajax({
          data : {
            id : tmp,
            case : "stock"
          },
          type : "POST",
          url : "/add",
          success : function(data){
            var res = JSON.parse(data)
            $("#quant"+tmp).empty()
            $("#quant"+tmp).append(res)
          }
        })
      })
      // function to minus a quantity of a product
      $("#stockTable").on("click", ".minus", function(){
        var tmp = $(this).attr("id").replace("minus", "")
        // ajax
        $.ajax({
          data : {
            id : tmp,
            case : "stock"
          },
          type : "POST",
          url : "/minus",
          success : function(data){
            var res = JSON.parse(data)
            // Attention si quantité <= 0
            if(res <= "0"){
              alert("Ce produit n'est plus en stock. Supprimer le.")
            }
            $("#quant"+tmp).empty()
            $("#quant"+tmp).append(res)
          }
        })
      })
    })