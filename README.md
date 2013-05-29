关于认证

1. 每个用户可以在网站上设置ip白名单列表，非白名单的请求不予处理
1. 为了保护用户隐私，文本告警使用https发送

监控数据项定义

1. user_id: 用户ID，字符串，从网站上获取
1. hostname: 监控所在机器名字, 字符串，
1. appname: 应用或服务的名字, 字符串
1. name: 监控项的名字, 字符串
1. type: 监控类型, 字符串
1. value: 如果type是num_xxx，则是数值类型，如果是type是text,则是文本类型

监控类型

1. num_avg: 每分钟算出平均值
1. num_sum: 每分钟算出总和
1. text: 文本告警

todo

1. appname, hostname等参数的特殊字符转换，长度限制，等判断
1. collector对每个IP访问频率的限制
1. 每用户监控项数量限制
