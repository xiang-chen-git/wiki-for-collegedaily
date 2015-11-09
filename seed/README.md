词条：
- 创建者，贡献者，内容，title，标签们，

词条页面展现：
- 词条本身（title, 内容, 标签们）+ 创建者 + 三个贡献者 - 详见前端模版

词条编辑页面：
- 词条审核(通过与否) + 展现Diff功能
- ^^添加附件（评估中）

词条标签：
- 标签名


用户管理：
- 超级管理员权限管理用户的激活/关闭状态

管理员：
- 词条管理员：管理版本（reversion）及revert
- 用户管理员：添加删除用户
- 超级管理员：任意管理权限

=========================================================================
Tag:
1. add_tag
    url: http://root.com/wiki/add_tag/entry_id/
    method: POST
    request.POST.get('tag') = '标签'

    服务器端如果在现有Tag表里没找到对应的标签,将会创建一个.
2. remove_tag
    url: http://root.com/wiki/reomve_tag/entry_id/
    method: POST
    request.POST.get('tag') = '标签'

邮箱验证：
    目前未对未验证的用户作出限制。在WikiUser的model里有一个checked field,boolean类型，    表示是否通过验证。

    在Personal_edit.html页面下面加入了“点击验证”的entry point，由account.views.forget_password处理

密码重设、找回：
    在login界面加入了“忘记密码”的entry_point
    在personal_edit界面加入“重设密码”的entry_point
    两个入口由同一个view account.views.reset_password处理
