# 天然药材系统命名法算法 (Systematic Nomenclature for Natural Medicinal Materials Algorithm, SNNMMA)

SNNMMA的输入可以是一个JSON对象。为了阐明这一点，我们以一个常见的天然药材蜜麻黄为例进行说明。

```json
{
    "nmm_type": "processed",
    "species_origins": [["Ephedra sinica", "草麻黄"], "or", ["Ephedra intermedia", "中麻黄"], "or", ["Ephedra equisetina", "木贼麻黄"]],
    "medicinal_parts": [["stem herbaceous", "草质茎"]],
    "special_descriptions": [],
    "processing_methods": [["segmented", "段制"], "and", ["aquafried honey", "蜜炙制"]]
}
```

在上述输入数据结构中，SNNMMA的用户需要提供与NMM类型相关的信息以及四种命名元素的相关细节。值得注意的是，这四种类型的命名元素是共同使用名为`NmmNeData`的数据结构进行存储的。

基本结构如下，以`species_origins`为例：

```json
[
    ["Ephedra sinica", "草麻黄"], 
    "or",
    ["Ephedra intermedia", "中麻黄"], 
    "or", 
    ["Ephedra equisetina", "木贼麻黄"]
]
```

The list encompassed in `NmmNeData` permits the incorporation of multiple name element pairs, each with a data substructure: `["name element in English or Latin", "name element in Chinese"]`, which can be interconnected by the logical operator strings `"or"` or `"and"`.

Subsequently, when `NmmNeData` is conveyed to SNNMMA, the algorithm autonomously executes a series of processes for each name element type of NmmNeData. This includes string data verification, deduplication, sorting, character transformation, and more. Ultimately, the algorithm calculates and derives the NMM Systematic Name (NMMSN) and NMM Systematic Chinese Name (NMMSN-zh), presenting the results as another JSON Object:

`NmmNeData`中的列表允许加入多个命名元素对，每个对都有一个数据子结构：`["英文或拉丁文元素", "中文元素"]`，它们可以通过逻辑操作符字符串`"or"`或`"and"`连接起来。

随后，当`NmmNeData`传递给SNNMMA时，算法会自动执行一系列处理NmmNeData每种命名元素类型的过程。这包括字符串数据验证、去重、排序、字符转换等。最终，算法计算并推导出NMM系统名称 (NMM Systematic Name, NMMSN) 和NMM系统中文名称 (NMMSN-zh)，并以另一个JSON对象的形式展示结果：

```json
{
    "success": true,
    "error_msg": "Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.", 
    "error_msg_en_zh": {
        "en": "Multiple species origins detected.",
        "zh": "检测到多个物种基源。"
    },
    "nmmsn": {
        "nmmsn": "Ephedra equisetina vel intermedia vel sinica Stem-herbaceous Segmented and Aquafried-honey",
        "nmmsn_zh": {
            "zh": "蜜炙制段制木贼麻黄或中麻黄或草麻黄草质茎",
            "pinyin": "mì zhì zhì duàn zhì mù zéi má huáng huò zhōng má huáng huò cǎo má huáng cǎo zhì jīng"
        },
        "nmmsn_name_element": { 
            "nmm_type": "processed",
            "species_origins": [["Ephedra equisetina", "木贼麻黄"], "or", ["Ephedra intermedia", "中麻黄"], "or", ["Ephedra sinica", "草麻黄"]],
            "medicinal_parts": [["stem herbaceous", "草质茎"]],
            "special_descriptions": [],
            "processing_methods": [["segmented", "段制"], "and", ["aquafried honey", "蜜炙制"]]
        },
        "nmmsn_seq": [["Ephedra equisetina vel intermedia vel sinica", "木贼麻黄或中麻黄或草麻黄"], ["Stem-herbaceous", "草质茎"], ["", ""], ["Segmented and Aquafried-honey", "蜜炙制段制"]] 
    }
}
```

SNNMMA的输出显示如下特点：

一旦用户数据被SNNMMA成功处理以构建NMMSN，`success`的值将设为`true`。此外，由SNNMMA构建的NMMSN结果信息将存储在`nmmsn`键下。

SNNMMA输出中每个层级键的具体含义如下描述：

- `error_msg`：在SNNMM框架中，存在某些有效但非首选的规则。例如，不推荐使用多个物种基源进行NMM的系统命名。SNNMMA可以在NMMSN构建过程中自动检测到此类异常。因此，可能存在NMMSN成功构建，但`error_msg`仍然填充了在过程中遇到的任何问题的情况。这些错误消息遵循标准格式：`Pipe: xxx. Status: xxx. Reason: xxx.`并存储在`error_msg`中。
- `error_msg_en_zh`：为了增强英文和中文用户的使用体验，SNNMMA中的错误消息已进行本地化处理。`error_msg`中的`Reason`信息被处理并分别存储在`error_msg_en_zh.en`和`error_msg_en_zh.zh`中。这确保了即使是有编程或语言障碍的用户也能清楚地理解在SNNMMA构建NMMSN过程中遇到的任何问题。
- `nmmsn`：此键包含所有直接相关的NMMSN信息。
- `nmmsn.nmmsn`：代表成功构建的NMM系统名称。
- `nmmsn.nmmsn_zh`：`nmmsn.nmmsn_zh.zh`表示成功构建的NMM系统中文名称，而`nmmsn.nmmsn_zh.pinyin`代表相应的拼音转写。
- `nmmsn.nmmsn_name_element`：此键的数据结构镜像输入数据的结构。然而，基于SNNMM规则，`NmmNeData`数据结构内的元素顺序可能会被调整或重新排序。例如，`species_origins`的顺序可能由`[["Ephedra sinica", "草麻黄"], "or", ["Ephedra intermedia", "中麻黄"], "or", ["Ephedra equisetina", "木贼麻黄"]]`变更为`[["Ephedra equisetina", "木贼麻黄"], "or", ["Ephedra intermedia", "中麻黄"], "or", ["Ephedra sinica", "草麻黄"]]`，因为这三个物种基源之间的字母顺序为`e -> i -> s`。
- `nmmsn.nmmsn_seq`：鉴于NMMSN包含四个命名元素，此键存储与每个命名元素相对应的NMMSN。在ShennongName中，可以利用这个序列化的NMMSN独特地用不同颜色显示每个命名元素，增强用户友好性。

如果SNNMMA在NMMSN构建过程中遇到问题并失败，SNNMMA的输出将非常相似：

```json
{
    "success": false,
    "error_msg": "...", 
    "error_msg_en_zh": {
        "en": "...",
        "zh": "..."
    }
}
```

然而，`success`的值将被设为`false`，并且结果JSON对象将不包括`nmmsn`键及其对应的值。
