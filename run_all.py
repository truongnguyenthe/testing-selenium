"""
Chạy toàn bộ test một lượt và sinh báo cáo HTML:
    python run_all.py
"""
import subprocess, sys

subprocess.run(
    [sys.executable, "-m", "pytest", "tests/",
     "--html=report.html", "--self-contained-html", "-v"],
    check=False
)
