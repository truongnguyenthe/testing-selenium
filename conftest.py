# conftest.py — pytest tự động load file này
# Đảm bảo thư mục gốc (TestingSelemium/) luôn có trong sys.path
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
