SweatShop
=========


根据 git commit 提交时间，计算自己的加班时长。
计算结果为根据
[中华人民共和国劳动法](http://www.npc.gov.cn/wxzl/gongbao/2000-12/05/content_5004622.htm)
第四十四条对应策略换算后的时长


统计精确度有效时间为2015年11月之后


## 使用限制

* 仅支持 中华人民共和国 假日作息
* 时间范围为2015年11月起，早于的时间只会按普通双休处理，有需求的用户请自行 PR 完善假日
* 在项目目录中执行

## 关于精度

* 默认时间朝十晚七，简化为计算上午下午，各4小时
* 统计结果约等于实际加班时长，目前暂时忽略了以下问题：
    - 对于法定假日如国庆、春节的补偿算法，统一按200%而不是300%计算
    - 目前0-4点的 commit 会归为第二天，取决于开发者习惯，多数情况为少于实际时长
        - 前一天晚上加班时间没有任何 commit 入库
        - 开发者节假日加班至凌晨（应该比较少见）


## 相关法律法规

[中华人民共和国劳动法](http://www.npc.gov.cn/wxzl/gongbao/2000-12/05/content_5004622.htm)
* 第四十三条
* 第四十四条
* 第四十五条


[中华人民共和国劳动合同法](http://www.gov.cn/flfg/2007-06/29/content_669394.htm)

* 第四十七条
* 第四十八条
* 第六十二条
* 第八十七条


[中华人民共和国合同法](http://www.npc.gov.cn/wxzl/wxzl/2000-12/06/content_4732.htm)

* 第一百二十四条 合同法适用于劳动合同


[中华人民共和国著作权法](http://www.npc.gov.cn/npc/xinwen/2010-02/26/content_1544852.htm)

* 第四条  著作权不能违法
* 第十六条 职务作品 以及 物质奖励依据




## 准备工作


首先生成 git log。可参考 `demo/mp.prepare.sh`

```
cd <需要统计的代码仓库路径>
git log --format='%ae;%aD' > <输出路径>
cd -

```


## 开始执行

```
export SWEATSHOP_EMAIL='<commit提交时的email-01>,<commit提交时的email-02>' # 默认为作者邮箱
export SWEATSHOP_WEEKDAY='6,7' # 默认为周日休息一天
export SWEATSHOP_WORKING_TIME='9-18'  #  默认为10-19
export SWEATSHOP_DEBUG='yes'  # 查看明细工时
export SWEATSHOP_HOURS='yes'  # 只计算小时，用于评估单周是否超44小时


cat <输出路径> | python ./mapper.py | sort | python ./reducer.py
```


具体可参考 demo 中的范例
