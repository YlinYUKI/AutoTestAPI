import pymysql
from common.handle_conf import conf
import requests
"""
python3中操作mysql数据库
1、pymysql

2、mysql-client模块 ：Windows下通过pip安装不了（了解即可， 操作和使用都是一样的）

"""

class HandleDB:
    def __init__(self):
        #1、连接数据库
        self.connect = pymysql.connect(host=conf.get('mysql','host'),
                        port=int(conf.get('mysql','port')),
                        user=conf.get('mysql','user'),
                        password=conf.get('mysql','password'),
                        charset="utf8")

        #2、创建游标对象
    def find_one(self,sql):
        """查询一条数据"""
        cur = self.connect.cursor()
        #3、执行sql语句
        # execute方法执行完sql， 返回的是查询到的数据条数
        cur.execute(sql)
        res =cur.fetchone()
        # 提交事务（如果涉及到增删改查操作的sql执行完之后，一定要提交事务才会生效）
        self.connect.commit()
        #关闭游标对象
        cur.close()
        return res

    def find_all(self,sql):
        """查询到的所有数据"""
        cur = self.connect.cursor()
        #3、执行sql语句
        # execute方法执行完sql， 返回的是查询到的数据条数
        cur.execute(sql)
        res = cur.fetchall()
        # 提交事务（如果涉及到增删改查操作的sql执行完之后，一定要提交事务才会生效）
        self.connect.commit()
        #关闭游标对象
        cur.close()
        return res

    def find(self,sql):
        """查询数据条数"""
        cur = self.connect.cursor()
        #3、执行sql语句
        # execute方法执行完sql， 返回的是查询到的数据条数
        res = cur.execute(sql)
        # 提交事务（如果涉及到增删改查操作的sql执行完之后，一定要提交事务才会生效）
        self.connect.commit()
        #关闭游标对象
        cur.close()
        return res

    def __del__(self):
        # 关闭数据库
        self.connect.close()

if __name__ == '__main__':
    sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone = '13799490082'"
    db = HandleDB()
    res = db.find_all(sql)
    print(res)
    headers = {
        "X-Lemonban-Media-Type" :"lemonban.v2",
        "Authorization":"Bearer "+"eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjExMDMxNDk1LCJleHAiOjE2NTk1NDM5NDJ9.jl-qpToxhPQE2Ws0R3dXee6TWYWYShEmqqoI9OKlzq3GL9ZGnYk1aiu1D4dUqK85ukV7YpwK_yOchaVv30ElGg"
    }
    url = 'http://api.lemonban.com/futureloan/member/recharge'
    params = {
            "member_id": "11031495",
            "amount": 50000
    }
    res = requests.post(url=url, json=params, headers=headers)
    print(res.json())
    res2 = db.find_all(sql)
    print(res)
    print('-----------')
    print(res2)