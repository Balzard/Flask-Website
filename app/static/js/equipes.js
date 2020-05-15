   // Function to add a player line according to a team
    function addPlayerline(playerJS){
      // take info back
      var pseudo = playerJS.pseudo;
      var id = playerJS.id;
      var admin = playerJS.admin;
      // First add a row
      var tmp = "<tr class='playerRow' id="+id+"></tr>";
      $("#playersTable").append(tmp);
      // Add a cell for the name
      tmp = "<td>"+pseudo+"</td>";
      $("#"+id).append(tmp);
      // Add a cell if the current_user is admin to delete a player
      if(admin){
        var url = "/deleteFromTeam/id="+id;
        var confirmDel = "return confirm('Delete the player "+pseudo+" from his team ?')";
        var del = '<a class="deleteBtn btn btn-danger" href="'+url+'" onclick="'+confirmDel+'">Delete</a>';
        tmp = '<td class="options">'+del+'</td>';
        $("#"+id).append(tmp);
      }
    }
    // Function to modify a player table according to a team
    function playersTeam(idList, name_team){
      // Case with no players
      if(idList.length == 0){
        // Add a row for information
        var tmp = "<tr class='info'></tr>";
        $("#playersTable").append(tmp);
        // Add a cell to say there is no player
        tmp = "<td>There is no player in team "+name_team+".</td>"
        $("tr.info").append(tmp);
      // Case with players
      }else{
        $.each(idList, function(index, value){
          $.ajax({
            data : {
              id : value
            },
            type : "POST",
            url : "/askPlayerInfo",
            success : function(data){
              // playerJS has all the information of the player
              playerJS = JSON.parse(data);
              addPlayerline(playerJS);
            }
          })
        })
      }
    }
    // main function
    $(document).ready(function(){
      // Fonction to take the players in a team
      $("button.teamView").click(function(){
        // Step 1 : remove the current rows of the table player
        $("#playersTable").find("tr:gt(0)").remove();
        // Step 2 : get back the name of the team
        var name_team = $(this).attr("id");
        $("#teamName").empty();
        var txt = "Players for the team "+name_team;
        $("#teamName").append(txt);
        // Step 3 : get the id list of the players in this team under JSON format
        $.ajax({
          data : {
            name : name_team
          },
          type : "POST",
          url : "playersInTeam",
          success : function(data){
            // We have the ids in a string array
            var idList = JSON.parse(data);
            playersTeam(idList, name_team);
          }
        })
      })
    })