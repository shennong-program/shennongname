# 天然药材系统命名法

## 规则1：两名一ID规则

每个天然药材（Natural Medicinal Material, NMM）均被赋予一个**天然药材系统名（NMM Systematic Name, NMMSN）**、一个**天然药材通用名（NMM Generic Name, NMMGN）**和一个**天然药材ID（NMM Identity, NMM ID；也称“天然药材编号”）**。

## 规则2：唯一规则

在 SNNMM 下产生的 NMMSN、NMMGN 和 NMM ID 均唯一。

## 规则3：ANMM/PNMM不同名规则

SNNMM 将 NMMs 分为 3 类：**原始天然药材（Raw NMMs, RNMMs）**、**农产天然药材（Agricultural NMMs, ANMMs）**和**炮制天然药材（Processed NMMs, PNMMs）**（图1）。RNMMs 一般按照农产品进行管理，PNMMs 一般按照药品进行管理。

![天然药材类型](../images/nmm.svg ':size=50%')

> **图1：天然药材类型**
> 原始天然药材在产地经过初步加工后可制得农产天然药材；农产天然药材通常会进一步加工，制备成炮制天然药材。在天然药材系统命名法中，不同类型的天然药材（如农产天然药材和炮制天然药材）被分配不同且唯一的系统名、通用名和天然药材ID。

## 规则4：合法字符规则

为便于世界上任何一个国家的人们都能够通过他们国家的标准键盘简单地输入 NMMSN 或 NMMGN，NMMSN 和 NMMGN 的命名只允许使用以下字符：大小写拉丁字母 `a-zA-Z`、连词符 `-`。

## 规则5：大小写不敏感规则

在 NMMSN 或 NMMGN 中，尽管会有大小写字母同时使用的情况，但这仅仅是为了便于 NMMSN 和 NMMGN 的阅读便利。SNNMM 中，不得通过采用不同大小写的方式以区分不同的 NMM。

## 规则6：正体规则

NMMSN 或 NMMGN 采用正体书写。

## 规则7：NMMSN规则

### 规则7.1：NMMSN标准中文对应名规则

为便于中文语境下的交流，每个 NMM 在命名 NMMSN 的同时，SNNMM 也会给出 NMMSN 的对应的标准中文对应名，即**天然药材系统中文名（NMMSN-zh）**。

### 规则7.2：NMMSN构词规则

NMMSN 由以下 4 种命名组件构成（图9）：

1. **I. 物种基源（Species origin）**
2. **II. 药用部位（Medicinal part）**
3. **III. 特殊形容（Special description）**
4. **IV. 炮制方法（Processing method）**

### 规则7.3：NMMSN语法分析规则

根据自然语言处理和计算语言学原理，NMMSN 的语法分析（Parsing）结构如图2所示。

![天然药材系统名的语法解析结构](../images/ne.svg ':size=50%')

> **图2：天然药材系统名的语法解析结构**
> 一个有效的天然药材系统名的解析结构由四个命名要素的合法组合构成。天然药材系统名至少应包含组件 I 和组件 II。对于农产天然药材，天然药材系统名可包含组件 I、II 和 III；对于炮制天然药材，则可包含组件 I、II、III 和 IV。图中实线表示该类型天然药材所必需包含的组件，虚线表示组件 III 为可选项。

### 规则7.4：NMMSN最小构词规则

- ANMM 的 NMMSN 至少包含以下 2 种命名组件：**I 和 II**；
- PNMM 的 NMMSN 至少包含以下 3 种命名组件：**I、II 和 IV**（图2）。

### 规则7.5：NMMSN语序规则

- NMMSN 命名组件的语序不可改变，语序为：**I-II-III-IV**；
- 对于 NMMSN-zh，命名组件为符合中文习惯，语序为：**IV-III-I-II**。

### 规则7.6：物种基源命名规则

#### 规则7.6.1：完整物种学名规则

命名时尽可能优先使用物种的完整的拉丁文物种学名。在可以明确具体物种时，不得仅采用物种的属名或种加词进行命名。

- ✅ NMMSN: [Solidago decurrens Herb](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0020)；NMMSN-zh: 一枝黄花全草（物种基源：*Solidago decurrens*）  
  ❌ Solidago Herb

- ✅ NMMSN: [Panax ginseng Rhizome and Root](https://shennongalpha.westlake.edu.cn/knowledge/nmm-001l)；NMMSN-zh: 人参根茎与根（物种基源：*Panax ginseng*）  
  ❌ Ginseng Rhizome and Root

#### 规则7.6.2：标准物种学名规则

NMMSN 命名时优先使用现行的标准物种学名。标准物种学名优先参考以下数据库：[Catalogue of Life](https://www.catalogueoflife.org/)、[物种2000中国节点](http://sp2000.org.cn)

**示例：**  
在《中国药典·2020年版·一部》（下简称“ChP”）中记载 NMM“吴茱萸”为多物种基源 NMM：基于 *Euodia rutaecarpa* 或 *Evodia ruticarpa var. officinalis* 或 *Evodia ruticarpa var. bodinieri*。然而，这三个物种学名均非标准物种学名，其正名均为 *Tetradium ruticarpum*。因此，“吴茱萸”实际仍然为单物种基源 NMM。其正确 NMMSN 为：  

NMMSN: [Tetradium ruticarpum Fruit](https://shennongalpha.westlake.edu.cn/knowledge/nmm-012w)；NMMSN-zh: 吴茱萸果实

#### 规则7.6.3：多物种基源命名规则

多种物种的相同部位用作一个 NMM 的药用部位，且这些物种互为可替代关系（即“或”关系）时，为了明确 NMM 的具体物种基源，NMMSN 命名时要完整列出所有的物种基源。物种学名并列，中间采用 “vel”（拉丁文连词，意为“或”）连接（NMMSN-zh 中使用“或”连接），排序时以拉丁字母为顺序。当多物种中出现重复的属名时，属名第二次出现时可省略。

- **多物种基源来自相同属物种（麻黄）：**  
  ChP 中，“麻黄”有 3 种物种基源：*Ephedra sinica* 或 *Ephedra intermedia* 或 *Ephedra equisetina*。因此应当命名为：  
  - Ephedra equisetina vel Ephedra intermedia vel Ephedra sinica Stem-herbaceous  
  但由于属名一致，须进一步缩写为：  
  - NMMSN: [Ephedra equisetina vel intermedia vel sinica Stem-herbaceous](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0006)；NMMSN-zh: 木贼麻黄或中麻黄或草麻黄草质茎

- **多物种基源来自不同属物种：**  
  - Cremastra appendiculata vel Pleione bulbocodioides vel Pleione yunnanensis Pseudobulb  
  须进一步缩写后两种物种的属名：  
  - NMMSN: [Cremastra appendiculata vel Pleione bulbocodioides vel yunnanensis Pseudobulb](https://shennongalpha.westlake.edu.cn/knowledge/nmm-00ac)；NMMSN-zh: 杜鹃兰或独蒜兰或云南独蒜兰假鳞茎

#### 规则7.6.4：细化物种基源规则

当能够明确更细化的物种基源时，我们应当优先使用更细化的物种基源对 NMM 进行指代。

- NMMSN: [Ephedra sinica Stem-herbaceous](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0003)；NMMSN-zh: 草麻黄草质茎  
- NMMSN: [Ephedra intermedia Stem-herbaceous](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0004)；NMMSN-zh: 中麻黄草质茎  
- NMMSN: [Ephedra equisetina Stem-herbaceous](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0005)；NMMSN-zh: 木贼麻黄草质茎

#### 规则7.6.5：物种包含规则

对于一个多物种基源 NMM，若其物种基源的物种分类等级存在包含关系，则仅使用具有最高包含等级的物种进行命名。

**示例（山楂）：**  
ChP 记载“山楂”的物种基源为 *Crataegus pinnatifida* 和 *Crataegus pinnatifida var. major*。但由于后者为前者的变种，存在包含关系，因此命名时不应同时包含变种作为“山楂”的物种基源。  

- ✅ NMMSN: [Crataegus pinnatifida Fruit](https://shennongalpha.westlake.edu.cn/knowledge/nmm-009x)；NMMSN-zh: 山楂果实  
  ❌ Crataegus pinnatifida vel pinnatifida var major Fruit

具有更细化物种基源的 NMM 可以单列，以明确：  

- ✅ NMMSN: [Crataegus pinnatifida var major Fruit](https://shennongalpha.westlake.edu.cn/knowledge/nmm-009y)；NMMSN-zh: 山里红果实

#### 规则7.6.6：具体物种信息不确定的NMM的命名规则

对于具体物种信息不确定的 NMM，可以仅用属名进行命名，并在属名后加 `unspecified`（NMMSN-zh 中添加“未定种”）以提示物种信息尚未被明确。

**示例：**  
蒲公英属下有数千种物种（见 [Catalogue of Life: Taraxacum](https://www.catalogueoflife.org/data/taxon/7SSF)），均可潜在用作 NMM：  

- NMMSN: [Taraxacum unspecified Herb](https://shennongalpha.westlake.edu.cn/knowledge/nmm-01yf)；NMMSN-zh: 蒲公英属未定种全草

#### 规则7.6.7：物种学名非合法字符省略规则

如果 NMM 的物种基源的物种学名含有非合法字符，则省略。

- ✅ NMMSN: [Ziziphus jujuba var spinosa Seed](https://shennongalpha.westlake.edu.cn/knowledge/nmm-005x)；NMMSN-zh: 酸枣种子  
  ❌ Ziziphus jujuba var spinosa Seed

### 规则7.7：药用部位命名规则

#### 规则7.7.1：语法规则

NMMSN 药用部位使用英文单数名词或名词短语进行命名。

- ✅ NMMSN: [Panax ginseng Leaf](https://shennongalpha.westlake.edu.cn/knowledge/nmm-001s)；NMMSN-zh: 人参叶  
  ❌ Panax ginseng Leaves

#### 规则7.7.2：首字母大写和连词符规则

为便于阅读，药用部位的首字母应当大写；药用部位由多个词组成时，中间需要使用连词符 `-` 连接。

- NMMSN: [Solidago decurrens Herb](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0020)；NMMSN-zh: 一枝黄花全草  
- NMMSN: [Ephedra sinica Stem-herbaceous](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0003)；NMMSN-zh: 草麻黄草质茎

#### 规则7.7.3：多药用部位命名规则

如果一个 NMM 同时使用同一物种的多种不同的药用部位入药，药用部位间可以使用 `and`（“与”）连接。如果一个 NMM 可以使用同一物种的多种不同的药用部位入药，且互为可替代关系，则药用部位间可以使用 `or`（“或”）连接。药用部位的排序根据拉丁字母顺序。

- NMMSN: [Vincetoxicum pycnostelma Rhizome and Root](https://shennongalpha.westlake.edu.cn/knowledge/nmm-01mz)；NMMSN-zh: 徐长卿根茎与根

#### 规则7.7.4：细化药用部位规则

当能够明确更细化的药用部位时，我们应当优先使用更细化的药用部位对 NMM 进行指代。

**示例：**  
“*Vincetoxicum pycnostelma* Rhizome and Root” 可进一步细化为：  

- NMMSN: [Vincetoxicum pycnostelma Rhizome](https://shennongalpha.westlake.edu.cn/knowledge/nmm-01mx)；NMMSN-zh: 徐长卿根茎  
- NMMSN: [Vincetoxicum pycnostelma Root](https://shennongalpha.westlake.edu.cn/knowledge/nmm-01my)；NMMSN-zh: 徐长卿根

### 规则7.8：特殊形容命名规则

#### 规则7.8.1：语法规则

一些 NMM 须具有某种特有的性状特征或经过某些特殊的产地初加工后方可入药，对于这些 NMM，可以在命名组件 III 中构词部分使用英文形容词、形容词短语、名词或同位语进行命名。

#### 规则7.8.2：首字母大写和连词符规则

为便于阅读，特殊形容的首字母应当大写；特殊形容由多个词组成时，中间需要使用连词符 `-` 连接。

- NMMSN: [Zingiber officinale Rhizome](https://shennongalpha.westlake.edu.cn/knowledge/nmm-003g)；NMMSN-zh: 姜根茎  
- NMMSN: [Zingiber officinale Rhizome Fresh](https://shennongalpha.westlake.edu.cn/knowledge/nmm-003m)；NMMSN-zh: 鲜姜根茎  

- NMMSN: [Curcuma wenyujin Rhizome](https://shennongalpha.westlake.edu.cn/knowledge/nmm-000t)；NMMSN-zh: 温郁金根茎  
- NMMSN: [Curcuma wenyujin Rhizome Freshly-sliced](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0015)；NMMSN-zh: 鲜切片温郁金根茎

#### 规则7.8.3：道地药材规则

某些 NMM 需要特别明确道地产区时，可以使用地理名词作为特殊形容。中国产道地 NMM 的产地名通常使用中华人民共和国省会名称的标准英文名，NMMSN-zh 中使用“省会标准缩写+产”作为其中文对应词。

- NMMSN: [Fritillaria thunbergii Bulb Zhejiang](https://shennongalpha.westlake.edu.cn/knowledge/nmm-024c)；NMMSN-zh: 浙产浙贝母鳞茎

### 规则7.9：炮制方法命名规则

#### 规则7.9.1：语法规则

PNMM 必须包含炮制方法。PNMM 基于其对应的 ANMM 进行命名，通过在命名组件 IV 额外添加炮制方法所对应的英文形容词、形容词短语、同位语或炮制方法的英文缩写词（词组）进行命名。炮制方法的中文对应词必须以“制”结尾。

**示例：**  

- ANMM: NMMSN: [Artemisia annua Part-aerial](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0001)；NMMSN-zh: 黄花蒿地上部  
- PNMM: NMMSN: [Artemisia annua Part-aerial Segmented](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0002)；NMMSN-zh: 段制黄花蒿地上部

#### 规则7.9.2：首字母大写和连词符规则

为便于阅读，炮制方法的首字母应当大写；炮制方法由多个词组成时，中间需要使用连词符 `-` 连接。

#### 规则7.9.3：多重炮制的NMM命名规则

如果是多重炮制的 PNMM，需要使用多个炮制方法，其炮制方法间使用 `and` 连接，居于更晚炮制过程的炮制方法的词序居后（NMMSN-zh 的炮制方法由于有“制”作为词尾，因而无须使用逻辑连词；居于更晚炮制过程的炮制方法的词序居前）。炮制方法和炮制顺序相关，因此炮制方法的词序不可随意改变。

- ✅ NMMSN: [Ephedra sinica Stem-herbaceous Segmented and Aquafried-honey](https://shennongalpha.westlake.edu.cn/knowledge/nmm-000b)；NMMSN-zh: 蜜炙制段制草麻黄草质茎  
  ❌ *Ephedra sinica* Stem-herbaceous Aquafried-honey and Segmented

#### 规则7.9.4：中国天然药材（中药材）炮制方法命名规则

中药材的炮制方法以《中国药典·2020年版·四部》“0231 炮制通则”为基础。炮制方法命名时，如果能明确炮制细类，则优先采用炮制细类进行命名；在不能明确炮制细类时，可以采用炮制大类进行命名。

- NMMSN: [Crataegus pinnatifida Fruit Cleaned and Stirfried-golden](https://shennongalpha.westlake.edu.cn/knowledge/nmm-00a1)；NMMSN-zh: 炒黄制净制山楂果实  
- NMMSN: [Crataegus pinnatifida Fruit Cleaned and Stirfried-charred](https://shennongalpha.westlake.edu.cn/knowledge/nmm-00a3)；NMMSN-zh: 炒焦制净制山楂果实

#### 规则7.9.5：中药材炮制分类规则

中药材炮制（natural medicinal processing）分 3 大类：  

1. 净制（processing by cleaning）  
2. 切制（processing by cutting）  
3. 备制（processing by preparing）

经过切制的中药材默认已经经过净制。凡需要备制的，其必须首先经过净制或切制。

- ✅ NMMSN: [Ephedra sinica Stem-herbaceous Segmented and Aquafried-honey](https://shennongalpha.westlake.edu.cn/knowledge/nmm-000b)；NMMSN-zh: 蜜炙制段制草麻黄草质茎  
  ❌ Ephedra sinica Stem-herbaceous Aquafried-honey

- ✅ NMMSN: [Zingiber officinale Rhizome Cleaned and Stirfried-sand](https://shennongalpha.westlake.edu.cn/knowledge/nmm-003l)；NMMSN-zh: 砂炒制净制姜根茎  
  ❌ Zingiber officinale Rhizome Stirfried-sand

### 规则7.10：非物种类或物种基源难以确定的NMM的命名规则

若待命名 NMM 为非物种类或物种基源难以明确，其 NMMSN 可采用英语习称进行命名。

- NMMSN: [Talc](https://shennongalpha.westlake.edu.cn/knowledge/nmm-01xx)；NMMSN-zh: 滑石  
- NMMSN: [Talc Pulverized](https://shennongalpha.westlake.edu.cn/knowledge/nmm-01xz)；NMMSN-zh: 粉制滑石

## 规则8：NMMGN规则

### 规则8.1：简洁规则

NMMSN 由于命名时需要明确 NMM 的物种基源、药用部位、特殊描述、炮制方法等信息，因此 NMMSN 通常较长。为了便于日常使用和临床处方时的便利，每个 NMM 也均有一个对应的较简短的 NMMGN。

### 规则8.2：中药材NMMGN-zh的惯常规则

中药材的 NMMGN-zh 优先采用已经惯用的中药材名。如果中药材出自 ChP，ChP 收录的中药材的中文名通常即为 NMMGN-zh。对于细化物种基源后的单物种基源中药材，为了防止命名冲突，个别中药材的 NMMGN-zh 开头添加“单”/“独”以区分。

### 规则8.3：中药材NMMGN的拼音名优先规则

为了使得中药材的 NMMGN 和 NMMGN-zh 呼应，我们在命名中药材的 NMMGN 时，优先使用中药材 NMMGN-zh 的拼音名。拼音名不使用声调和空格，使用连词符 `-` 连接不同汉字的拼音，首字母大写，并使用 `v` 代替 `ü`。

- NMMSN: [Erycibe obtusifolia Stem](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0022)；NMMSN-zh: 丁公藤茎；  
  NMMGN: Dan-ding-gong-teng；NMMGN-zh: 单丁公藤（为和“丁工藤”区分，添加“单”字。）  

- NMMSN: [Erycibe obtusifolia vel schmidtii Stem](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0024)；NMMSN-zh: 丁公藤或光叶丁公藤茎；  
  NMMGN: Ding-gong-teng；NMMGN-zh: 丁公藤

- NMMSN: [Ligustrum lucidum Fruit](https://shennongalpha.westlake.edu.cn/knowledge/nmm-00d7)；NMMSN-zh: 女贞果实；  
  NMMGN: Nv-zhen-zi；NMMGN-zh: 女贞子

### 规则8.4：最短NMMGN-zh规则

NMMGN-zh 必须使用 2 个及以上的汉字进行命名。

- NMMSN: [Prunus mume Fruit](https://shennongalpha.westlake.edu.cn/knowledge/nmm-008w)；NMMSN-zh: 梅果实  
  NMMGN-zh：✅ 乌梅；❌ 梅

### 规则8.5：先到先得规则

由于 NMMGN 较短，在其命名时，难免遇到命名冲突的情况。在这种情况下，我们需要遵循先到的 NMMGN 优先，对于后到的 NMMGN，其须加一些额外信息以区分。

**示例：**  
假设我们已经对以下 NMM 进行命名：  

- NMMSN: [Ephedra sinica Stem-herbaceous](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0003)；NMMSN-zh: 草麻黄草质茎；  
  NMMGN: Cao-ma-huang；NMMGN-zh: 草麻黄

上述案例中该 NMM 的 NMMGN-zh 并未提及其药用部位信息，因为其是优先命名的，所以省略。但假设我们要进一步将 *Ephedra sinica* 的根用药，其 NMMGN 和 NMMGN-zh 就要适当做出区分：  

- NMMSN: [Ephedra sinica Root](https://shennongalpha.westlake.edu.cn/knowledge/nmm-000g)；NMMSN-zh: 草麻黄根；  
  NMMGN: Cao-ma-huang-gen；NMMGN-zh: 草麻黄根

## 规则9：NMM ID规则

每种 NMM 被赋予唯一的 NMM ID。NMM ID 的编码规则为：`NMM-XXXX`，其中 `XXXX` 为 4 位 36 进制的数字（即 `0-9, A-Z`），从 `0001` 开始递增，止于 `ZZZZ`，至多可编码 `36^4 − 1 = 1,679,615` 种 NMM。NMM ID 大小写不敏感，但在书写时为了方便阅读通常使用全大写。

**示例：**

- NMM-ID: [NMM-0001](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0001)  
  NMMSN: Artemisia annua Part-aerial  
  NMMSN-zh: 黄花蒿地上部  
  NMMGN: Qing-hao  
  NMMGN-zh: 青蒿

- NMM-ID: [NMM-0002](https://shennongalpha.westlake.edu.cn/knowledge/nmm-0002)  
  NMMSN: Artemisia annua Part-aerial Segmented  
  NMMSN-zh: 段制黄花蒿地上部  
  NMMGN: Qing-hao-duan  
  NMMGN-zh: 青蒿段

## 规则10：标准指代规则

### 规则10.1：首次完整出现规则

为了保证科学文本中的 NMM 名称和其实际指代的 NMM 准确对应，推荐在每个独立文本（如一篇论文、百科等）中首次出现某 NMM 时，以 `NMMSN (NMM ID, NMMGN)` 格式给出 NMM 的两名一 ID。在后续文本中 NMM 第二次出现时，允许只使用 NMMSN、NMMGN 或 NMM ID 进行指代。

**示例：**

- Artemisia annua Part-aerial (NMM-0001, Qing-hao) is a commonly used Chinese natural medicinal material. Artemisia annua Part-aerial has the effect of treating malaria.
- Artemisia annua Part-aerial (NMM-0001, Qing-hao) is a commonly used Chinese natural medicinal material. Qing-hao has the effect of treating malaria.
- Artemisia annua Part-aerial (NMM-0001, Qing-hao) is a commonly used Chinese natural medicinal material. NMM-0001 has the effect of treating malaria.
- 黄花蒿地上部（NMM-0001，青蒿）是一种常用的中药材。黄花蒿地上部可用于治疗疟疾。
- 黄花蒿地上部（NMM-0001，青蒿）是一种常用的中药材。青蒿可用于治疗疟疾。
- 黄花蒿地上部（NMM-0001，青蒿）是一种常用的中药材。NMM-0001 可用于治疗疟疾。

### 规则10.2：附录完整信息规则

如果某研究中涉及大量 NMM，在正文文本中一一给出所有的 NMMSN、NMMGN 和 NMM ID 可能导致正文文本过长。这种情况下，可以在正文中仅使用 NMMSN 或 NMMGN 或 NMM ID 中的一种来指代 NMM；但在附录中，需要给出 `NMM ID – NMMSN – NMMGN` 的完整列表。
