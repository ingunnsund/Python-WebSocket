/**
 * Created by Knut on 27.04.2017.
 */
$(document).ready(function() {
    var webSocket = new WebSocket("ws://localhost:3001");
    console.log("Connecting to server...");

    webSocket.onerror = (error) => {
        console.log("Error");
        console.log(error);
    }

    webSocket.onopen = (message) => {
        console.log("Connection is open");
        //console.log(message);
        webSocket.send("This is a test message");
    }

    webSocket.onmessage = (event) => {
        console.log("You received a message");
        alert(event.data)
    }

    webSocket.onclose = (message) => {
        console.log("Connection is closed");
        console.log(message);
    }

    $("#send-message").click(function() {
        webSocket.send($("#input-text").val());
    });
});