import tmp as trans
import setting as setting

data = {"message":[], "table":[[[] for _ in range(8)] for _ in range(18)], "user":{}}

trans.reset_storage(setting.storage, data)