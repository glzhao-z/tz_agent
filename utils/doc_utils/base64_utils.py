import base64

def encode_file(img_path):
    with open(img_path,'rb') as f:
        img = f.read()
    # 编码成字符串
    encoded_str = base64.b64encode(img).decode('utf-8')
    return encoded_str

#解码
def decode_file(encoded_str,output_path):
    # 解码成图片
    data = base64.b64decode(encoded_str)
    with open(output_path,'wb') as f:
        f.write(data)


# 把base64字符串加上表示图片的前缀
def get_base64_uri(img_path):
    encoded_str = encode_file(img_path)
    return "data:image/png;base64," + encoded_str


