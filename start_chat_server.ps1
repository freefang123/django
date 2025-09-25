# Django聊天服务器启动脚本
Write-Host "🚀 启动Django聊天服务器..." -ForegroundColor Green
Write-Host "📡 支持HTTP API和WebSocket连接" -ForegroundColor Cyan
Write-Host "🌐 服务器地址: http://localhost:8000" -ForegroundColor Yellow
Write-Host "🔌 WebSocket地址: ws://localhost:8000/ws/chat/{room_id}/" -ForegroundColor Yellow
Write-Host "⏹️  按 Ctrl+C 停止服务器" -ForegroundColor Red
Write-Host "--------------------------------------------------" -ForegroundColor Gray

try {
    python -m daphne -b 127.0.0.1 -p 8000 myproject.asgi:application
}
catch {
    Write-Host "❌ 启动失败: $_" -ForegroundColor Red
    Write-Host "💡 请检查依赖是否正确安装" -ForegroundColor Yellow
    Read-Host "按任意键退出"
}
