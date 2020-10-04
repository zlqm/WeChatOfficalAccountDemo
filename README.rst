###############
公众号开发Demo
###############

基于[OpenWeChat]()开发的公众号后台Demo

功能
###########

1. 关注回复
2. 关键字回复
3. 渠道码(事件二维码)


使用方法
#########


服务端配置
*************

1. 初始化数据库，管理员账户

   .. code::

    $: python manage.py makemigrations
    $: python manage.py migrate
    $: python manage.py createsuperuser


2. 配置公众号账户

   1. 在管理员界面创建公众号帐号配置 

      .. image:: docs/wechat_setup.jpg
          :alt: 公众帐号配置

   2. 在微信后台添加回调接口

      .. image:: docs/wechat_server_setup.jpg
         :alt: 公众号配置
     
   3. 更新微信token(可以添加为crontab，每隔一个半小时更新一次)

       .. code::

           $: python manage.py update_wechat_credential

3. 创建回复模板, 这里可以适用jinja2语法，例如下图的 ``{{ nickname }}`` 会被替换为用户名

   * .. image:: docs/create_reply_template_1.jpg
       :alt: 创建回复模板1


   * .. image:: docs/create_reply_template_2.jpg
       :alt: 创建回复模板2


4. 创建回复规则，我们在这里创建三种不同的回复规则： 关注回复、事件二维码、文本

   * .. image:: docs/create_reply_rule.jpg
       :alt: 创建回复规则


   * .. image:: docs/create_reply_rule_1.jpg
       :alt: 创建回复规则1
   

   * .. image:: docs/create_reply_rule_2.jpg
       :alt: 创建回复规则2
   

   * .. image:: docs/create_reply_rule_3.jpg
       :alt: 创建回复规则3
   

5. 创建事件二维码, 只需要输入二维码的参数，系统会自动创建二维码

   * .. image:: docs/create_qrcode_1.jpg
       :alt: 创建事件二维码
       
   * .. image:: docs/create_qrcode.jpg
       :alt: 创建事件二维码


客户端效果
**************

1. 关注公众号
2. 输入关键字 ``help``
3. 扫描事件二维码

   .. image:: docs/wechat_client.jpg
      :alt: 微信客户端
      :width: 300px 