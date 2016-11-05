"use strict";

function showActivities(results) {
    console.log(results);
    // var activities = results;
    // var [a1, a2, a3, a4, a5] = activities

    // $("#c1, #c2, #c3, #c4, #c5").html(a1, a2, a3, a4, a5);
    // $("#c1, #c2, #c3, #c4, #c5").attr('value', "a1, a2, a3, a4, a5");
   
}

function getActivities() {
    evt.preventDefault();
    
    // var url = "/activities.json?category=" + $("category").val();

    $.get('/activities', showActivities);
    console.log("Sent AJAX");
}

$("#cat-form").on('submit', getActivities);
 