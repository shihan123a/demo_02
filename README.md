# demo_02
#scrapy借助搜狗微信爬取微信文章
1.目标站点分析；2.项目创建，spider创建；3.设置items、编写爬虫核心代码；4.设置HttpProxyMiddleware、MongoPipeline，设置settings，

首先分析其URL，利用快捷键F12打开开发者工具，点击Network,勾选Preserve log,然后刷新页面，在最左侧列表选择以weixin开头的网址，点击Headers,拉倒最下面便能看到Query String Parameters,这里面便是URL的参数

接下来分析文章详情页：文章详情页网址由程序解析获得，详情页中可以获得：文章标题、文章内容、文章发送时间、文章内图片链接、编辑、文章链接等内容。
微信文章网页结构也较为规整，我们通过以下代码即可获取以下信息

item['article_title'] = response.xpath('//*[@id="activity-name"]/text()').extract_first(default='').strip()
item['article_content'] = response.xpath('string(//*[@id="js_content"])').extract_first(default='').strip()
item['article_pubtime'] = response.xpath('//*[@id="post-date"]/text()').extract_first(default='').strip()
item['article_savetime'] = response.xpath('//*[@id="post-date"]/text()').extract_first(default='').strip()
item['article_source'] = response.xpath('//*[@id="post-user"]/text()').extract_first(default='').strip()
item['article_editor'] = response.xpath('//*[@id="meta_content"]/em[2]/text()').extract_first(default='').strip()

然后创建spider项目
设置代理IP同样是在中间件中，当获取到的IP是保存在txt文件中的，并不利于代理IP的实时获取，删除以及新增，所以最好时保存在数据库中，数据库可以用MySQL、MongoDB等。之所以需要频繁的删除新增是因为，这些公开的高匿IP很多人都在用，所以有可能很快就被封了，所以在项目中使用的话尽量购买代理ip。



