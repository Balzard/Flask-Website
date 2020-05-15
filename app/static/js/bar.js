
// Function to add a product row
function addProd(prodJS){
      //
      var id = prodJS.id;
      var nom = prodJS.nom;
      var quantite = prodJS.quantite;
      var type = prodJS.type;
      var tarif = prodJS.tarif;
      // Add a row
      var tmp = "<tr id=prod"+id+"></tr>"
      $("#barTable").append(tmp)
      // add the cells
      tmp = "<td>"+nom+"</td>"
      $("#prod"+id).append(tmp)
      tmp = "<td>"+type+"</td>"
      $("#prod"+id).append(tmp)
      tmp = "<td>"+tarif+"</td>"
      $("#prod"+id).append(tmp)
    }
    // main fonction
    $(document).ready(function(){
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
  							$("#barTable").find("tr:gt(0)").remove();
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
  										// Take the info about the prod
  										$.ajax({
  											data :{
  												id : value
  											},
  											type : "POST",
  											url : "/infoProd",
  											success : function(data){
  												prodJS = JSON.parse(data);
  												addProd(prodJS);
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
  		$("#all").click(function(){
  			// Step 1 : remove the current rows of the table prod
  			$("#barTable").find("tr:gt(0)").remove();
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
  						// Take the info about the prod
  						$.ajax({
  							data :{
  								id : value
  							},
  							type : "POST",
  							url : "/infoProd",
  							success : function(data){
  								prodJS = JSON.parse(data);
  								addProd(prodJS);
  							}
  						})
  					})
  				}
  			})
  		})
  	})