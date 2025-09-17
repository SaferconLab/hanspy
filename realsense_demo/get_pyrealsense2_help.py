import pyrealsense2
import contextlib
import io

# 重定向标准输出到一个字符串缓冲区
with contextlib.redirect_stdout(io.StringIO()) as f:
    help(pyrealsense2)

# 获取帮助文档的文本内容
help_text = f.getvalue()

# 将帮助文档写入文件
with open('pyrealsense2_help.txt', 'w') as file:
    file.write(help_text)

print("帮助文档已保存到 pyrealsense2_help.txt")
