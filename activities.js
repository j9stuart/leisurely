
function showActivities(result) {
    console.log(result)
    var activities = result;
    var [a1, a2, a3, a4, a5] = activities

    // $("#c1, #c2, #c3, #c4, #c5").html(a1, a2, a3, a4, a5);
    // $("#c1, #c2, #c3, #c4, #c5").attr('value', "a1, a2, a3, a4, a5");
   
}
function getActivities() {
    event.preventDefault();

    var formInputs = {
        "name": $(".category").val()
    };

    $.post('/activities', formInputs, showActivities);
    console.log("Sent AJAX");
}

$("#cat-form").on('submit', getActivities);
 