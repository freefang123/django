@echo off
echo 🚀 启动Django聊天服务器...
echo 📡 支持HTTP API和WebSocket连接
echo 🌐 服务器地址: http://localhost:8000
echo 🔌 WebSocket地址: ws://localhost:8000/ws/chat/{room_id}/
echo ⏹️  按 Ctrl+C 停止服务器
echo --------------------------------------------------

python -m daphne -b 127.0.0.1 -p 8000 myproject.asgi:application

pause
