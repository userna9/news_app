import bcrypt

# [修复] 移除已停止维护的 passlib（与 bcrypt 5.0 不兼容，注册/登录时必然崩溃），
# 改为直接使用 bcrypt 官方库，生成的 $2b$ 哈希格式与原 passlib 完全兼容，
# 数据库里已有的用户密码无需迁移。

#密码加密
def get_hash_password(password:str):
    # [修复] bcrypt 要求 bytes 类型输入，返回值转成 str 方便存库
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password,hashed_password):
    # [修复] 同样按 bytes 校验
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
