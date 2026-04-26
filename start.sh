#!/bin/bash

echo "=========================================="
echo "   CodeGuide - AI软件开发助手"
echo "=========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "[1/3] 检查依赖..."
if [ ! -d "venv" ]; then
    echo "[信息] 创建虚拟环境..."
    python3 -m venv venv
fi

echo "[2/3] 激活虚拟环境..."
source venv/bin/activate

echo "[3/3] 安装依赖..."
pip install -q -r requirements.txt

echo ""
echo "=========================================="
echo "   启动应用..."
echo "=========================================="
echo ""
echo "应用将在浏览器中打开"
echo "如未自动打开，请访问: http://localhost:8501"
echo ""

streamlit run app.py