import sqlite3

# 连接数据库（如果没有会自动创建 orders.db 文件）
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# 建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    status TEXT,
    logistics TEXT
)
''')

# 插入两条假数据测试
cursor.execute("INSERT OR IGNORE INTO orders VALUES ('123456', '已发货', '顺丰速运 SF123456789')")
cursor.execute("INSERT OR IGNORE INTO orders VALUES ('888888', '待发货', '仓库配货中')")

conn.commit()
conn.close()
print("数据库初始化成功，已生成 orders.db")
