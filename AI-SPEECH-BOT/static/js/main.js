//REGISTER ERROR
function registerError() {
    var result = 0; //Flag to Track status of DB querry(success/failed)

    //var querry = $("#querryInput").val();

    $.get("/registerError", { querryInput: document.getElementById("querryInput").value }).done(function (data) {  //data is the output or the response you got from the page    
        result = 1; // 1 Indicating Success!
        //$('#myModal1').modal('hide');
        alert(data);
        //var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> '+data+' </div></div>';
        //$("#chatbox").append(botHtml);
        //var chatHistory = document.getElementById("chatbox");
        //chatHistory.scrollTop = chatHistory.scrollHeight;

    }).fail(function (data) {
        result = 2; // 2 Indicating server is restarting/shutdown!
        //$('#myModal1').modal('hide');
        alert("Server Under Update! Retrying in 5 Seconds");
        //var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> Server Under Update! Retrying in 5 Seconds. </div></div>';
        //$("#chatbox").append(botHtml);
        //var chatHistory = document.getElementById("chatbox");
        //chatHistory.scrollTop = chatHistory.scrollHeight;

    });

    setTimeout(function () {
        if (result == 2) {
            //Code to Handle when Server is restarting/shutdown
            $.get("/registerError", { querryInput: querry }).done(function (data) {  //data is the output or the response you got from the page    
                result = 1; // 1 Indicating Success!

                //var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> Successfully Updated Database! </div></div>';
                //$("#chatbox").append(botHtml);
                //var chatHistory = document.getElementById("chatbox");
                //chatHistory.scrollTop = chatHistory.scrollHeight;
                alert("Data added Successfully!")
            }).fail(function (data) {
                result = 2; // 2 Indicating server is restarting/shutdown!

                //var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> Please Try again later! </div></div>';
                //$("#chatbox").append(botHtml);
                //var chatHistory = document.getElementById("chatbox");
                //chatHistory.scrollTop = chatHistory.scrollHeight;
            });
        }
    }, 10000);

}

//ADD ERROR
function addEntryServer() {
    //Perform any needed validations here before calling server [LATER WORK!]
    $.get("/addRow", {
        tag: document.getElementById("inputTag").value,
        patterns: document.getElementById("inputPatterns").value,
        responses: document.getElementById("inputResponses").value,
        context_set: document.getElementById("inputContext_set").value,
        status: document.getElementById("inputStatus").value
    }).done(function (data) {
        //$('#myModal').modal('hide');
        //var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> '+data+' </div></div>';
        //$("#chatbox").append(botHtml);
        //var chatHistory = document.getElementById("chatbox");
        //chatHistory.scrollTop = chatHistory.scrollHeight;
        alert(data);
    }).fail(function (data) {
        //$('#myModal').modal('hide');
        //var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> '+data+' </div></div>';
        //$("#chatbox").append(botHtml);
        //var chatHistory = document.getElementById("chatbox");
        //chatHistory.scrollTop = chatHistory.scrollHeight;
        alert(data);
    });
}

//Admin Tables :

function deleterow(id) {
    $.get("/deleteRow", { idInput: id }).done(function (data) {
        alert(data);
        location.reload();
    }).fail(function (data) {
        alert(data);
        location.reload();
    });
}
function editrow(id) {
    //Function to set Values of the edit popup form
    document.getElementById("inputId").value = id;
    document.getElementById("inputTag").value = document.getElementById("tag" + id).innerHTML;
    document.getElementById("inputPatterns").value = document.getElementById("patterns" + id).innerHTML;
    document.getElementById("inputResponses").value = document.getElementById("responses" + id).innerHTML;
    document.getElementById("inputContext_set").value = document.getElementById("context_set" + id).innerHTML;
    document.getElementById("inputStatus").value = document.getElementById("status" + id).innerHTML;
}
function editEntryServer() {
    //Perform any needed validations here before calling server [LATER WORK!]
    $.get("/editRow", {
        id: document.getElementById("inputId").value,
        tag: document.getElementById("inputTag").value,
        patterns: document.getElementById("inputPatterns").value,
        responses: document.getElementById("inputResponses").value,
        context_set: document.getElementById("inputContext_set").value,
        status: document.getElementById("inputStatus").value
    }).done(function (data) {
        alert(data);
        //console.log(data);
        location.reload();
    }).fail(function (data) {
        alert(data);
        //console.log(data);
        location.reload();
    });
}

//Train Bot 
function invokeBotTraining() {
    $.get("/trainBot").done(function (data) {
        alert(data);
        //var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> '+data+' </div></div>';
        //$("#chatbox").append(botHtml);
        //var chatHistory = document.getElementById("chatbox");
        //chatHistory.scrollTop = chatHistory.scrollHeight;
    }).fail(function (data) {
        alert(data);
        //var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> '+data+' </div></div>';
        //$("#chatbox").append(botHtml);
        //var chatHistory = document.getElementById("chatbox");
        //chatHistory.scrollTop = chatHistory.scrollHeight;
    });
}

//Chat Bot 
function getBotResponse(flag) {
    var rawText = $("#textInput").val();
    var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send"> ' + rawText + ' </div><div class="img_cont_msg"><img src="https://png.pngtree.com/png-clipart/20190924/original/pngtree-businessman-user-avatar-free-vector-png-image_4827807.jpg" class="rounded-circle user_img_msg"></div></div>';
    $("#textInput").val("");
    $("#chatbox").append(userHtml);

    var chatHistory = document.getElementById("chatbox");
    chatHistory.scrollTop = chatHistory.scrollHeight;

    var messageStatus = 0; //To check if server returns message successfully!
    console.log("At 1 statement before /get");
    $.get("/get", { msg: rawText }).done(function (data) {         //data is the output or the response you got from the page
        messageStatus = 1 //Data received successfully!!
        //console.log("Inside /get method")
        var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> ' + data + ' </div></div>';
        $("#chatbox").append(botHtml);
        var chatHistory = document.getElementById("chatbox");
        chatHistory.scrollTop = chatHistory.scrollHeight;
    });
    setTimeout(function () {
        if (messageStatus == 0) {
            var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> Server under update! </div></div>';
            $("#chatbox").append(botHtml);
            var chatHistory = document.getElementById("chatbox");
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    }, 2000);
    //console.log("outside /get");

}
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getBotResponse(1);
    }
});

function voiceResponse() {
    $.get("/voice").done(function (data) {         //data is the output or the response you got from the page
        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send"> ' + data + ' </div><div class="img_cont_msg"><img src="https://png.pngtree.com/png-clipart/20190924/original/pngtree-businessman-user-avatar-free-vector-png-image_4827807.jpg" class="rounded-circle user_img_msg"></div></div>';
        $("#chatbox").append(userHtml);
        $("#textInput").val("");

        var chatHistory = document.getElementById("chatbox");
        chatHistory.scrollTop = chatHistory.scrollHeight;

        $.get("/get", { msg: data }).done(function (data) {         //data is the output or the response you got from the page
            var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.pinimg.com/originals/17/f6/8e/17f68e401b36b8b87346557940a40970.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"> ' + data + ' </div></div>';
            $("#chatbox").append(botHtml);

            var chatHistory = document.getElementById("chatbox");
            chatHistory.scrollTop = chatHistory.scrollHeight;
        });

    });

    i = 0;
    while (i < 300000000) {
        i++;
    }

    $("#textInput").val("Listening ... ");

}