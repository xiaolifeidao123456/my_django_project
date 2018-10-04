
import random


def get_verify_code():
    """
    生成短信验证码
    """
    code = ''
    s='1234567890'
    for i in range(6):
        code += random.choice(s)
    return code

