## 博客项目架构(持续修改)

理解：

* RESTful架构 [Restful](https://www.ruanyifeng.com/blog/2011/09/restful.html)
* DRF (djangorestframework)：后端的数据序列化，采用规范的REST模式
* httpie：测试
* vue-cli：搭建规范的Vue应用
* npm install axios：解决跨域请求问题
* jwt
* vue add bootstrap-vue
* elementui
* sass

基本功能：

* 账号注册登录，修改基本信息等
* 发表文章
* 管理已经发表的文章（修改，删除）
* 文章正文的编辑支持markdown组件(Markdown库)
* 评论区
* 文章可以有多个标签，每次创建文章的时候手动添加
* 条件式检索（按照标签， 按照文章标题，作者，内容等）

进阶功能

* 评论区的加强：评论的评论
* 用户的管理：用户的增删改查
* 实现单点登录，用户的token验证

表设计
用户表(User)：
* username:
* password:
* email:
* profile\_photo
* registration\_time

文章表(Article):
* user\_id: 外键
* title
* body
* created
* updated
* visit\_count
* like\_count
* tag\_id(many to many)


评论表(Comment):
* user\_id: 外键
* article\_id: 外键
* like\_count
* comment\_date
* content
* comment\_id: 外键

标签表(Tag):
* name

注: 文章和标签表为多对多关系

1. 根据搜索内容返回相应的文章
2. 用户使用jwt认证，规范方法
3. 数据库保存密码用hash码保存，而不是明文保存
4. 用户和用户信息表分开, 用户表存储用户名邮箱密码等，用于权限管理，然后关联用户信息表用于处理数据