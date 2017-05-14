/**
 * Created by Knut and Ingunn on 27.04.2017.
 */


$(document).ready(function() {
    //a websocket object and its functions for handling new messages etc.
    let webSocket = new WebSocket("ws://localhost:3001");
    console.log("Connecting to server...");

    webSocket.onerror = (error) => {
        console.log("Error");
        console.log(error);
    };

    webSocket.onopen = (message) => {
        console.log("Connection is open");
        webSocket.send("This is a test message");
    };

    webSocket.onmessage = (event) => {
        console.log("You received a message: " + event.data);

        let jsonMessage = JSON.parse(event.data);
        let username = jsonMessage.username;
        let message = jsonMessage.message;
        let sendDate = jsonMessage.send_date;
        let messageColor = jsonMessage.message_color;

        console.log(myUsername + ", " + username);

        let messageClass = "message ";
        if (username === myUsername) {
            if (username === "Anonymous") {
                messageClass += "message-others";
            } else {
                messageClass += "message-own";
            }
        } else {
            messageClass += "message-others";
        }

        messageClass += " " + messageColor;

        let newElement = '<p class="' + messageClass + '">[' + sendDate + '] ' + message + '</p>';
        $("#messages").append(newElement)
        $("#messages").scrollTop($("#messages")[0].scrollHeight);
        //webSocket.close(1000);
    };

    webSocket.onclose = (message) => {
        console.log("Connection is closed");
        console.log(message);
    };

    var myUsername = "";
    // javascript code for handling click etc.
    $("#send-message").click(()=> {
        if ($("#input-text").val() !== "") {

            let username = $("#username-input").val();
            let now = new Date();
            let sendDate = now.getHours() + ":" + now.getMinutes();
            let messageColor = $("#message-back-color").val().toLowerCase();

            if (username === "") {
                username = "Anonymous";
            }
            myUsername = username;

            let jsonMessage = {
                "username": username,
                "message": $("#input-text").val(),
                "send_date": sendDate,
                "message_color": messageColor
            };

            webSocket.send(JSON.stringify(jsonMessage));
            $("#input-text").val("");
        }
    });

    $("#input-text").keypress(function(event) {
        if (event.keyCode === 13 && $(this).val() !== "") {
            $("#send-message").click();
        }
    });

    $("#upload_file_button").click(function() {
        let fileName = $("#upload_file")[0].files[0];
        //webSocket.binaryData = "blob";
        webSocket.send(fileName)

    })
});