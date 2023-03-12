添加GPT2接口的真寻AI插件 原项目: https://github.com/OVOU4/plugins_zhenxun_bot/blob/main/ai/ 在原版的基础之上修改以能够在最新版的zhenxun_bot中使用。

使用前需要先删除zhenxun_bot/plugins/ai自带的ai，再使用此项目。

项目需要调用本地的GPT-2接口。原项目地址来自https://github.com/OVOU4/zhenxunbot_GPT-2 未搭建本地GPT2的情况下也可以正常使用。 以下仅记录我的搭建过程。

将GPT-2的项目下载到zhenxun_bot/extensive_plugin 在项目中新建model/model_epoch40_50w，将模型放入其中

QQ图片20230304134119

在 poetry shell 中执行以下命令

pip install -r requirements.txt -i https://pypi.douban.com/simple

安装相关依赖

安装完毕之后，运行

python interact.py --model_path /mnt/zhenxun_bot/extensive_plugin/zhenxunbot_GPT-2-main/model/model_epoch40_50w

运行成功后会有如下提示

QQ图片20230304134255

然后就可以愉快的聊天了，效果图如下

QQ图片20230304134442

QQ图片20230304134505
