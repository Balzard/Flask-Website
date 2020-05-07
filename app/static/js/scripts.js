// Fonction to take the players in a team
$("button.team").click(function(){
  // Step 1 : remove the current rows of the table player
  $("#playersTable").find("tr:gt(0)").remove();
  // Step 2 : get back the name of the team
  var name_team = $(this).attr("id");
  // Step 3 : get the id list of the players in this team under JSON format
  $.ajax({
    data : {
      name = name_team
    },
    type = "POST",
    url = "playersInTeam",
    success : function(data){
      // We have the ids in a string array
      idList = JSON.parse(data);
      alert(idList);
    }
  })
})
