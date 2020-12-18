$(function() {
    // hiding survey id form
    $("#to_hide").css('display', 'none');

    // hiding remove button if number of questions is 1
    number_questions = $("#questionnaire").children().length-2
    if (number_questions==1){
        $("#removeQuestion").css('display', 'none');
    }

    // emptying 1º question and storing as variable
    $("#question1").children("ol").children().last().css('display', 'none');
    question_model = $("#question1").clone();
    question_model.children()[0].value = "";

    // hiding options if the question type is not multichoice one
    for (var i=0; i<number_questions; i++){
        var question = $("#questionnaire").children().eq(i);
        var q_select_type = question.children().eq(1);
        var options = question.children().eq(2);
        var opt_textarea = options.children().eq(0).eq(0).children()[0];
        console.log(opt_textarea.className)
        q_select_type.val(opt_textarea.className)
        if (["1", "2"].includes(opt_textarea.className)){
            options.css('display', 'none');
        }
    }
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

    // insert the new question form
    question.attr("id","question"+question_number);
    question.children("ol").css('display', 'none')
    console.log(question.children("ol"))
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
    var option = prev_option.clone();
    // changing the ids and names as it corresponds 
    var option_number = parseInt(prev_option.children()[0].name.slice(-1))+1;
    console.log(option_number)
    
    var option_name = "option"+question_number+"_"+option_number;
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
        if(options.children().length-2===1){
            options.children().last().css('display', 'none');
        }
    }else{
        // hidding if it is not a multichoice type question
        options.css('display', 'none');
    }
};