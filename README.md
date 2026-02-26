# FastAPI WebSocket Messages

Web application built with FastAPI that uses WebSocket for real-time messaging with sequential numbering.

## Features

- Form with text input for sending messages
- Numbered message list (starting from 1)
- WebSocket connection to server
- Server accepts message and assigns sequential number
- Numbered message sent back to page and displayed in list
- Message numbering resets on page reload (starts from 1)
- Fully dynamic page - no page reloads on message send
- JSON-based WebSocket communication

## Installation

```bash
git clone https://github.com/agronom28-crypto/fastapi-websocket-messages.git
cd fastapi-websocket-messages
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## Tech Stack

- Python 3.10+
- FastAPI
- WebSocket
- Uvicorn
- HTML/CSS/JavaScript
