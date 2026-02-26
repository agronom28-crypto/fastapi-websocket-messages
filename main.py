from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

message_counter = 0

html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Messages</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }
        #message-form {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        #message-input {
            flex: 1;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        #send-btn {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        #send-btn:hover {
            background-color: #45a049;
        }
        #messages {
            list-style: none;
            padding: 0;
        }
        #messages li {
            padding: 10px;
            margin-bottom: 5px;
            background-color: white;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        .msg-number {
            font-weight: bold;
            color: #4CAF50;
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <h1>WebSocket Messages</h1>
    <div id="message-form">
        <input type="text" id="message-input" placeholder="Type a message..." autocomplete="off">
        <button id="send-btn">Send</button>
    </div>
    <ul id="messages"></ul>

    <script>
        const ws = new WebSocket(`ws://${window.location.host}/ws`);
        const input = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');
        const messagesList = document.getElementById('messages');

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const li = document.createElement('li');
            li.innerHTML = `<span class="msg-number">${data.number}.</span>${data.text}`;
            messagesList.appendChild(li);
        };

        function sendMessage() {
            const text = input.value.trim();
            if (text) {
                ws.send(JSON.stringify({"text": text}));
                input.value = '';
                input.focus();
            }
        }

        sendBtn.addEventListener('click', sendMessage);

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global message_counter
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message_counter += 1
            response = {
                "number": message_counter,
                "text": message_data.get("text", "")
            }
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        pass
