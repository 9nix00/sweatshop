SweatShop
=========


根据 git commit 提交时间，计算自己的加班时长
计算结果为根据[中华人民共和国劳动法](http://www.npc.gov.cn/wxzl/gongbao/2000-12/05/content_5004622.htm)
第四十四条对应策略换算后的时长


统计精确度有效时间为2015年11月之后


## 使用限制

* 仅支持 中华人民共和国 假日作息
* 时间范围为2015年11月起，早于的时间只会按普通双休处理，有需求的用户请自行 PR 完善假日
* 在项目目录中执行

## 关于精度

* 考虑到朝九晚六和朝十晚七，统一计算上午下午，各4小时
* 实际加班时间会多于统计时间，统计时暂时忽略了对分钟的计算，简化实现
* 对于法定假日如国庆、春节的补偿算法，统一按200%而不是300%计算


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


## 准备工作


首先生成 git log。可参考 `demo/mp.prepare.sh`

```
cd <需要统计的代码仓库路径>
git log --format='%ae;%aD' > <输出路径>
cd -

```


## 开始执行

```
export SWEATSHOP_EMAIL='<commit提交时的email-01>,<commit提交时的email-02>'
export SWEATSHOP_WEEKDAY='6,7'

cat <输出路径> | python ./mapper.py | sort | python ./reducer.py
```


具体可参考 demo 中的范例
