// function to add a comment row
function addComment(commentJS){
		// Take data back
		var id = commentJS.id;
		var auteur = commentJS.auteur;
		var date = commentJS.date;
		var texte = commentJS.texte;
		// add a row to the table
		var tmp = "<tr id=comm"+id+"></tr>";
		$("#commentTable").append(tmp);
		// add the cells
		auteur_td = "<td>"+auteur+"</td>";
		date_td = "<td>"+date+"</td>";
		texte_td = "<td>"+texte+"</td>";
		$("#comm"+id).append(auteur_td);
		$("#comm"+id).append(date_td);
		$("#comm"+id).append(texte_td);

	}
	// main function
	$(document).ready(function(){
		$("#search").click(function(){
			var tmp = $("#searchInput").val();
			if(tmp == ""){
				alert("Nothing to look for.");
			}else{
				// Ajax to see if the author searched wrote comms
				$.ajax({
					data : {
						name : tmp
					},
					type : "POST",
					url : "/confirmAuthor",
					success : function(data){
						var res = JSON.parse(data);
						if(res){
							// Step 1 : remove the current rows of the table comment
							$("#commentTable").find("tr:gt(0)").remove();
							// Step 2 : take the comms id from the author
							$.ajax({
								data : {
									name : tmp
								},
								type : "POST",
								url : "/commsFromAuthor",
								success : function(data){
									var idList = JSON.parse(data);
									// Work for each comm
									$.each(idList, function(index, value){
										// Take the info about the comm
										$.ajax({
											data :{
												id : value
											},
											type : "POST",
											url : "/infoComm",
											success : function(data){
												commJS = JSON.parse(data);
												addComment(commJS);
												$("#allComm").html("Résultats pour " + $("#searchInput").val())
											}
										})
									})
								}
							})
						}else{
							alert("No comment related to this author.")
						}
					}
				})
			}
		})
		$("#all").click(function(){
			// Step 1 : remove the current rows of the table comment
			$("#commentTable").find("tr:gt(0)").remove();
			// Take the id of all the comments
			$.ajax({
				type : "POST",
				url : "/allComm",
				success : function(data){
					var idList = JSON.parse(data);
					$.each(idList, function(index, value){
						// Take the info about the comm
						$.ajax({
							data :{
								id : value
							},
							type : "POST",
							url : "/infoComm",
							success : function(data){
								commJS = JSON.parse(data);
								addComment(commJS);
								$("#allComm").html("All comments")
								$("#searchInput").val("")
							}
						})
					})
				}
			})
		})
	})