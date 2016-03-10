/**
 * Created by CHAN LIM on 3/7/2016.
 */

$(document).ready(function() {
    $(".puzzle-cell-input").inputmask('9');
    $("#solve-btn").click(function() {
        var data = prepData();

        $.ajax({
            url : "/SudokuSolved",
            type : "POST",
            dataType: "json",
            data : data,

            success : function(json) {
                if(json.success) {
                    setResult(json.solved_puzzle);
                }
                else
                    alert('could not solve');
            },

            error : function(xhr,errmsg,err) {
                alert(xhr.status + ": " + xhr.responseText);
            }
        });
        return false;
    });

});

function setResult(solved) {
    $("#number-input input[name=choice]").each(function(index) {
        $(this).val(solved[0]);
        solved = solved.slice(1, solved.length);
    });
}

function prepData() {
    $("#number-input input[name=choice]").each(function (index) {
        if ($(this).val() != "")
            $(this).addClass('filled');
        else
            $(this).addClass('empty');
    });

    var inputArr = $('#number-input').serialize().split("&choice=");
    var data = {
        'inputNumbers[]': inputArr.slice(1, inputArr.length),
        'csrfmiddlewaretoken': $("#number-input input[name=csrfmiddlewaretoken]").val()
    };
    return data
}