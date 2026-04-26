@echo off
chcp 65001 >nul
echo ==========================================
echo   CodeGuide - AI软件开发助手
echo ==========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
if not exist "venv" (
    echo [信息] 创建虚拟环境...
    python -m venv venv
)

echo [2/3] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [3/3] 安装依赖...
pip install -q -r requirements.txt

echo.
echo ==========================================
echo   启动应用...
echo ==========================================
echo.
echo 应用将在浏览器中打开
echo 如未自动打开，请访问: http://localhost:8501
echo.

streamlit run app.py

pause