# 定义字符串列表
Sect_pos= [
["p101", "云剑·探云", "斗转星移", "木灵印", "崩拳·戳", ],
["p102", "云剑·飞刺", "星罗棋布", "木灵·芽", "崩拳·封", "云剑·飞", "云剑·飞制", ],
["p103", "云剑·厚土", "星弈·挡", "火灵印", "崩拳·弹", "星奔·挡", "云剑·厚", "云剑·厚十", "云剑·厚+", ],
["p104", "轻剑", "星弈·夹", "火灵·窜", "锻拳", "星奔·夹", ],
["p105", "护身灵气", "震卦", "土灵印", "劈山掌", "身灵气", ],
["p106", "灵气灌注", "坤卦", "土灵·碎", "抱气法", ],
["p107", "巨虎灵剑", "巽卦", "金灵印", "罗刹扑", ],
["p108", "震雷剑", "掌心雷", "金灵·针", "破空爪", ],
["p109", "剑劈", "白鹤亮翅", "水灵印", "千斤坠", ],
["p110", "剑挡", "揽雀尾", "水灵·涛","起势", ],
["p111", "飞牙剑", "野马分鬃", "五行刺", "野马分鬓",  "朝气蓬勃", "野马分禁" ],
["p112", "骤风剑", "藕断丝连", "血气方刚", ],
["p201", "云剑·回守", "飞星刺", "木灵·复苏", "崩拳·撼", ],
["p202", "云剑·极意", "星弈·点", "木灵·疏影", "崩拳·缠", "星奔·点", ],
["p203", "云剑·无锋", "星弈·立", "火灵·聚炎", "崩拳·突", "星奔·立", ],
["p204", "化灵诀", "艮卦", "火灵·赤焰", "锻筋", ],
["p205", "引气剑", "坎卦", "土灵阵", "探马掌", ],
["p206", "巨鲸灵剑", "落雷术", "土灵·群山", "风冥爪", ],
["p207", "凝意诀", "斩草除根", "金灵阵", "夜鬼啸", "凝意", ],
["p208", "灵犀剑阵", "金鸡独立", "金灵·穿心", "岿然不动", ],
["p209", "地煞剑", "静气心法", "水灵·波澜", "势大力沉", ],
["p210", "形意剑", "落花有意", "水灵·汹涌", "气沉丹田", ],
["p211", "狂剑·一式", "气贯长虹", "浑天印", "浩然正气", "狂剑·一", ],
["p301", "云剑·柔心", "众星拱月", "木灵阵", "崩天步", ],
["p302", "云剑·无妄", "星弈·打", "木灵·巡林", "崩拳·截脉", "星·打", "星奔·打", ],
["p303", "云剑·点星", "兑卦", "火灵阵", "崩拳·降龙", ],
["p304", "云剑·汇灵", "白蛇吐信", "火灵·轰爆", "锻骨", "白蛇吐", "剑·汇灵", ],
["p305", "云舞诀", "御雷卦诀", "土灵·扬尘", "荷重前行", ],
["p306", "暗鸦灵剑", "两仪阵", "土灵·断崖", "迎风掌", ],
["p307", "破气剑", "流水无情", "金灵·蓄锐", "饿虎扑食", ],
["p308", "巨鹏灵剑", "气疗术", "金灵·锋芒", "双鬼拍门", ],
["p309", "反身剑", "枯木逢春", "水灵阵", "气若悬河", ],
["p310", "镜花剑阵", "螳螂捕蝉", "水灵·泉涌", "踏破九霄", "踏破九宵", ],
["p311", "三峰剑", "海底捞月", "五行流转", "势如破竹", "二峰剑", ],
["p401", "云剑·闪风", "星弈·飞", "木灵·暗香", "崩灭心法", "星奔·飞", ],
["p402", "云剑·月影", "星弈·虎", "木灵·玫刺", "崩拳·寸劲", "星奔·虎", ],
["p403", "聚灵心法", "六爻绝阵", "火灵·瞬燃", "崩拳·连崩", "六交绝阵", ],
["p404", "百鸟灵剑诀", "离卦", "火灵·灼心", "锻髓", ],
["p405", "白鹭灵剑", "星轨推衍", "土灵·绝壁", "鹤步", "星轨推行", ],
["p406", "巨鲲灵剑", "蜻蜓点水", "土灵·流沙", "灵玄迷踪步", "③巨鲲灵剑", ],
["p407", "灵感剑", "轰雷掣电", "金灵·飞梭", "冥影身法", "轰雷电", "轰雷梨电", "轰雷制电", ],
["p408", "流云乱剑", "反震心法", "金灵·铁骨", "玄手夺魂", ],
["p409", "水月剑阵", "金蝉脱壳", "水灵·腾浪", "冲霄破浪", ],
["p410", "狂剑·二式", "杯弓蛇影", "水灵·潜遁", "磅礴之势", ],
["p411", "混元碎击", ],
["p501", "云剑·游龙", "天元心法", "木灵·柳纷飞", "崩拳·闪击", ],
["p502", "云剑·凌波", "星弈·断", "火灵·烈燎原", "崩拳·惊触", "星奔·断", ],
["p503", "飞灵闪影剑", "乾卦", "土灵·合八荒", "锻神开海", ],
["p504", "万法归灵剑", "五雷轰顶", "金灵·巨鼎落", "百杀破境掌", ],
["p505", "剑意激荡", "梅开二度", "水灵·纳百川", "修罗吼", ],
["p506", "御空剑阵", "气吞山河", "混元无极阵", "玄心斩魄", ],
["p507", "连环剑阵", "黄雀在后", "五行天髓诀", "威震四方", ],
["p508", "狂剑·零式", "紫气东来", "天地浩荡", ],
]
Sidjob_type=[
["Elixir", "地灵丹", "培元丹", "小还丹", "锻体丹", "飞云丹", "驱邪丹", "还魂丹", "疗伤丹", "神力丹", "大还丹", "聚灵丹", "洗髓丹", "冰灵护体丹", "锻体玄丹", "悟道丹", ],
["Fulu", "奔雷符", "护灵符", "锐金符", "火云符", "清心咒", "水气符", "寒冰咒", "吸灵符", "瘴气符", "聚气咒", "扰心符", "弱体符", "万邪入体咒", "镇魂封元符", "千里神行符", ],
["Music", "破音", "土行曲", "逍遥曲", "慈念曲", "幻音曲", "天灵曲", "断肠曲", "轮指连音", "狂舞曲", "九煞破灵曲", "回春曲", "同心曲", "天音困仙曲", "幽绪乱心曲", "转弦合调", ],
["Paint", "调色", "练笔", "研墨", "笔走龙蛇", "画饼充饥", "画蛇添足", "挥毫泼墨", "灵感迸发", "以画入道", "触类旁通", "神来之笔", "落纸云烟", "运笔如飞", "画龙点晴", "妙笔生花", "灵感进发", ],
["Formation", "冲击阵纹", "引雷阵", "碎杀阵", "疗愈阵纹", "龟甲阵", "邪蛊阵", "周天剑阵", "辟邪阵纹", "聚灵阵", "天罡聚力阵", "八门金锁阵", "不动金刚阵", "万花迷魂阵", "回响阵纹", "须弥阵纹", ],
["Plant", "归元草", "金梭兰", "剑枝竹", "神力草", "神秘种子", "叶盾花", "愈甘菊", "灵植浇灌", "向灵葵", "飞枭灵芝", "穿肠紫蕨", "冰封雪莲", "玄韵道果", "空间灵田", "缚仙古藤", ],
["Fortune", "天谕·守", "天谕·攻", "卜命", "察体", "天运·避凶", "天运·趋吉", "探灵", "凶象", "天命·重现", "天命·飞逝", "吉运初显", "血光之灾", "诸事不宜", "天星·牵引", "天星·御心", "万事如意", "天机·顺应", "天机·逆施", "厄劫缠身", "命运轮回", "天运·避", "上命", "星·牵引", ],
]
Sidejob_pos=[
["sp11", "地灵丹", "奔雷符", "破音", "调色", "引雷阵", "归元草", "卜命", "上命", ],
["sp12", "培元丹", "护灵符", "土行曲", "练笔", "碎杀阵", "金梭兰", "察体", "护灵", ],
["sp13", "小还丹", "锐金符", "逍遥曲", "研墨", "冲击阵纹", "剑枝竹", "天谕·守", "天谕·攻", ],
["sp21", "锻体丹", "火云符", "慈念曲", "笔走龙蛇", "龟甲阵", "神力草", "探灵", ],
["sp22", "飞云丹", "清心咒", "幻音曲", "画饼充饥", "邪蛊阵", "神秘种子", "凶象", ],
["sp23", "驱邪丹", "水气符", "天灵曲", "画蛇添足", "疗愈阵纹", "叶盾花", "天运·避凶", "天运·趋吉", "天运·避", ],
["sp31", "还魂丹", "寒冰咒", "断肠曲", "挥毫泼墨", "聚灵阵", "愈甘菊", "吉运初显", ],
["sp32", "疗伤丹", "吸灵符", "狂舞曲", "灵感迸发", "周天剑阵", "灵植浇灌", "血光之灾", "灵感进发", ],
["sp33", "神力丹", "瘴气符", "轮指连音", "以画入道", "辟邪阵纹", "向灵葵", "天命·飞逝", "天命·重现", ],
["sp41", "大还丹", "聚气咒", "回春曲", "触类旁通", "天罡聚力阵", "飞枭灵芝", "万事如意", ],
["sp42", "聚灵丹", "扰心符", "九煞破灵曲", "神来之笔", "八门金锁阵", "穿肠紫蕨", "诸事不宜", ],
["sp43", "洗髓丹", "弱体符", "同心曲", "落纸云烟", "不动金刚阵", "冰封雪莲", "天星·牵引", "天星·御心", "星·牵引", ],
["sp51", "冰灵护体丹", "万邪入体咒", "天音困仙曲", "运笔如飞", "万花迷魂阵", "玄韵道果", "厄劫缠身", ],
["sp52", "锻体玄丹", "镇魂封元符", "转弦合调", "画龙点晴", "回响阵纹", "空间灵田", "命运轮回", ],
["sp53", "悟道丹", "千里神行符", "幽绪乱心曲", "妙笔生花", "须弥阵纹", "缚仙古藤", "天机·顺应", "天机·逆施", ],
]

def Match(cardname):
    typ = ""
    pos = ""
    for lst in Sidjob_type:
        if any(item in cardname for item in lst):
            typ = lst[0]
            for lst in Sidejob_pos:
                if any(item in cardname for item in lst):
                    pos = lst[0]
                    break
            break
    if not pos:
        for lst in Sect_pos:
            if any(item in cardname for item in lst):
                typ = "Sect"
                pos = lst[0]
                break
    if not pos:
        typ = "err"
        pos = cardname
    # print("typ:", typ, "pos:", pos)
    return typ, pos