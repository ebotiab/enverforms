$(function() {
    // hiding options of the 1º questions and remove buttons by default 
    $("#question1").children().last().css('display', 'none');
    $("#removeQuestion").css('display', 'none');
    $("#removeOption1").css('display', 'none');

    // emptying 1º question and storing as variable
    $("#question1").children()[0].value = "";
    question_model = $("#question1").clone();

    // emptying 1º option and storing in a list
    option_model_list = [];
    option1_1 = $("textarea[name='option1_1']")
    option1_1.value = ""
    option_model_list.push(option1_1.parent());

    // setting the first question type as text answer by default
    $("select[name='questiontype1']").val("1");
});


function appendQuestion(elmnt) {
    var question = question_model.clone();

    // getting the name of the last question form
    var prev_question = $(elmnt).prev();
    var prev_question_name = prev_question.children()[0].name

    // changing and names as it corresponds
    var question_number = parseInt(prev_question_name.slice(-1))+1;
    for (var i=0; i<2; i++){
        var e = question.children()[i]
        e.name = e.name.substring(0,e.name.length-1)+question_number;
    }
    var e = question.children()[2]
    e.id = e.id.substring(0,e.id.length-1)+question_number;
    $(e).children()[0].firstElementChild.name = "option"+question_number+"_1"
    e.lastElementChild.id = "removeOption"+question_number

    // storing created option in the option models list
    option_model_list.push($(e.firstElementChild));

    // insert the new question form
    question.attr("id","question"+question_number);
    question.insertAfter(prev_question);

    // unhidding the button for remove a question
    $("#removeQuestion").css('display', 'inline');
};


function popQuestion(elmnt) {
    // getting the last question
    var prev_q = $(elmnt).prev().prev();

    if (prev_q.children()[0].name==="statement2"){
        // hidding button if one question after remove 
        $(elmnt).css('display', 'none');
    }

    // removing the last question
    prev_q.remove();
};


function appendOption(elmnt) {
    // unhidding the button for remove a question
    question_number = $(elmnt).parent().parent().attr("id").slice(-1)
    $("#removeOption"+question_number).css('display', 'inline');

    // getting and copying the last option 
    var prev_option = $(elmnt).prev();

    // changing the ids and names as it corresponds
    var prev_option_name = prev_option.children()[0].name;
    var option_number = parseInt(prev_option_name.slice(-1))+1;
    var option_name = prev_option_name.substring(0, prev_option_name.length-1)+option_number;
    var option = option_model_list[parseInt(question_number)-1].clone();
    option.children()[0].value = ""
    option.children()[0].name = option_name;

    
    // insert the new option form
    option.insertAfter(prev_option);
};


function popOption(elmnt) {
    // getting the last option 
    var prev_option = $(elmnt).prev().prev();
    if (prev_option.children()[0].name.slice(-1)==="2"){
        // hidding button if one question after remove 
        $(elmnt).css('display', 'none');
    }

    // removing the last question
    prev_option.remove();
};


function showOptions(form) {
    // getting options id of the changed question type
    var options = $(form).siblings(":last")
    if(form.value == "3" || form.value == "4") {
        // unhidding if it is a multichoice type question
        options.css('display', 'block');
    }else{
        // hidding if it is not a multichoice type question
        console.log("hola")
        options.css('display', 'none');
    }
};