# ThinkSQL 类似ThinkPHP的数据库引擎

## 安装
```
pip install think-sql
```

## 使用

### 1. simple demo

> Database: `test` Table: `user`

```
from think-sql.database import DB

config = {
    'database': 'test',
    'host': '127.0.0.1',
    'port': 3306,
    'username': 'root',
    'password': 'root',
}

with DB(**config) as db:
    data = db.table('user').where('id',1).find()
    print(data)
```
result
```
{
    "id":1,
    "username":"hbh112233abc",
    "age":"36",
    "address":"FUJIAN.XIAMEN"
}
```

## 开发

- `poetry` [Python包管理之poetry的使用](https://blog.csdn.net/zhoubihui0000/article/details/104937285)

```
# 配置虚拟环境在项目目录下
poetry config virtualenvs.path true
# 安装依赖
poetry install
# 进入虚拟环境
poetry shell
```
### poetry命令

|名称| 功能|
|-|-|
|new|创建一个项目脚手架，包含基本结构、pyproject.toml 文件|
|init|基于已有的项目代码创建 pyproject.toml 文件，支持交互式填写|
|install|安装依赖库|
|update|更新依赖库|
|add|添加依赖库|
|remove|移除依赖库|
|show|查看具体依赖库信息，支持显示树形依赖链|
|build|构建 tar.gz 或 wheel 包|
|publish|发布到 PyPI|
|run|运行脚本和代码|

## 单元测试
```
pytest --cov --cov-report=html
```
