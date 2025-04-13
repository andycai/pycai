import struct
import base64
from typing import Union

def base64_encode(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('utf-8')

def base64_decode(data: str) -> str:
    return base64.b64decode(data).decode('utf-8')

# 写入用户名和密码到二进制文件
def write_to_binary_file(filename, username, password):
    with open(filename, "wb") as file:
        # 将用户名和密码编码为字节
        username_bytes = username.encode('utf-8')
        password_bytes = password.encode('utf-8')

        # 写入长度和内容
        file.write(struct.pack("I", len(username_bytes)))  # 先写用户名长度
        file.write(username_bytes)  # 写用户名
        file.write(struct.pack("I", len(password_bytes)))  # 再写密码长度
        file.write(password_bytes)  # 写密码

# 从二进制文件中读取用户名和密码
def read_from_binary_file(filename):
    with open(filename, "rb") as file:
        # 读取用户名
        username_length = struct.unpack("I", file.read(4))[0]
        username = file.read(username_length).decode('utf-8')

        # 读取密码
        password_length = struct.unpack("I", file.read(4))[0]
        password = file.read(password_length).decode('utf-8')

    return username, password

# 示例
filename = "user_data.bin"
username = "PublisherDQ2"
password = "xingJIAdq12024"

# 写入
write_to_binary_file(filename, base64_encode(username), base64_encode(password))

# 读取
read_username, read_password = read_from_binary_file(filename)
print(f"读取到的用户名: {base64_decode(read_username)} , 密码: {base64_decode(read_password)} , 写入的用户名: {read_username}, 密码: {read_password}")