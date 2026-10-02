# B300 多供应商询价清单（2026-10-01）

**目的：** 不只依靠联想（TD SYNNEX / Brain2Store）这一个渠道，同时向西班牙各品牌厂商、分销商和集成商询价 NVIDIA HGX B300（8 GPU）服务器，比较价格和交货期。必要时分几家各买几台。

**询价统一口径：**

- 采购量：首批 2 台，第二批再加 4 台（合计 6 台），之后同型号继续扩张。要求报 2 台、6 台、10 台以上三档单价。
- 冷却：优先液冷，也可报风冷（如果交货更快）。液冷若必须整柜采购或配 CDU，要求单独报价。
- 地点：Montgat 别墅地下机房，每间最多 2 台；每间 100 kW 专线，约 45 kW 留给 IT。
- 报价单：抬头 OZZIE INTERNATIONAL 2019, S.L.，有效期至少 30 天。参考单价 10 月 6 日前给，正式报价 10 月 9 日前给。
- 买方：OZZIE 单独承担，不要第三方担保，也不要集团其他公司担保。付款方式为现金或 60 个月融资租赁。
- 合规：仅限内部使用，签最终用户声明。

## 已发出邮件（2026-10-01）

各发一封独立邮件，抄送 jilong@jilong.es，收件人互相看不到。

| # | 供应商 | 类型 | 城市 | 能供的 B300 品牌 | 收件地址 | 备注 |
|---|---|---|---|---|---|---|
| 1 | Azken Muga | NVIDIA Elite 合作伙伴 | 马德里（Las Rozas） | 多品牌，含 ASUS | comercial@azken.com | 9/4 首次询价未回复，这次是第二次 |
| 2 | Ibertrónica | 集成商 | 马德里 | Supermicro、Gigabyte、ASUS | comercial@ibertronica.es | 9/4 首次询价未回复，这次是第二次 |
| 3 | Flytech | Supermicro 分销商，NVIDIA 合作伙伴 | **巴塞罗那**（C/ Sardenya 286）/ 马德里 | Supermicro、ASUS | info@flytech.es | 巴塞罗那最匹配 |
| 4 | Ingram Micro España | 批发分销商 | **巴塞罗那**（Viladecans）/ 马德里 | Dell、HPE、Lenovo 等 | comercial@ingrammicro.es | 请其转给 AI 团队或经销商 |
| 5 | Arrow ECS España | 批发分销商 | 马德里（Alcobendas） | HPE | serviciosprofesionales.ecs.es@arrow.com | 请其转给 HPE 团队 |
| 6 | Supermicro Europe | 厂商 | 荷兰（欧洲总部） | Supermicro | Sales_Europe@supermicro.com | 英文；请其介绍西班牙合作伙伴 |
| 7 | PNY Technologies Europe | NVIDIA 欧洲、中东、非洲（EMEA）分销商 | 法国 | NVIDIA DGX B300 | pnypro@pny.eu | 英文；拿 DGX 报价做对比 |
| 8 | Giga Computing（技嘉） | 厂商 | 台湾 | Gigabyte | marketing@gigacomputing.com | 英文；请其转给西班牙销售 |

## 还需用表单或电话联系（同事操作，内容可直接复制上面的询价邮件）

| 供应商 | B300 型号 | 联系方式 |
|---|---|---|
| Dell Technologies（马德里） | PowerEdge XE9780 / XE9785（风冷）、XE9780L / XE9785L（液冷） | 电话 900 816 516；企业表单 https://www.dell.com/es-es/dt/forms/contact-us/isg.htm |
| HPE（马德里 Las Rozas，Sant Cugat 也有办公点） | HPE Compute XD690（风冷）、ProLiant Compute XD685（液冷 5U） | 表单 https://www.hpe.com/es/es/contact-hpe.html ；也可经 V-Valley |
| Fsas Technologies（原富士通，马德里） | PRIMERGY GX2580 M8s | 表单 https://eu.fsastech.com/es/about-us/contact/ |
| V-Valley（Esprinet，El Prat de Llobregat / 马德里） | HPE 全系列 | 表单 https://www.v-valley.com/en/contacts/ |
| Bechtle España | 多品牌 | 表单 https://www.bechtle.com/es/soluciones-de-it/business-applications/artificial-intelligence/nvidia-for-ai |
| Computacenter（巴塞罗那） | 多品牌（NVIDIA Elite） | 电话 936 207 000（先确认在西班牙是否卖硬件） |
| SIXE（马德里 / 巴塞罗那） | Dell、Lenovo、Supermicro | 电话 91 198 02 43 |
| TD SYNNEX（巴塞罗那） | ASUS XA NB3I-E12、Lenovo | 现有联想渠道：在同一封邮件里请 Alex Cruzado 同时报 ASUS 方案，不另开新邮件 |

## 已有渠道

- **联想**：TD SYNNEX（Alex Cruzado）+ Brain2Store / Unikal（Jordi Pérez）。10 月 2 日 9:30 到 12 号别墅看机房，报价单要求 10 月 6 日前给。
  - 注意：调研查到联想的 B300 机型（SR680a V4）是**风冷**，未找到液冷（Neptune）B300，需当面确认。

## 调研要点

- **液冷：** Supermicro 4U 液冷 B300 须整柜采购，Dell 液冷 XE9780L 需配专用机柜（IR7000），技嘉液冷机型也按整柜方案卖。首批只买 2 台，风冷 8–10U 机型最简单。
- **公开参考价**（欧洲，不含税，未打折，只作上限）：8 GPU 的 B300 服务器约 43–69 万欧元；DGX B300 约 53.5–71.4 万欧元。交货期 8–14 周，定制配置超过 20 周。
- **出口管制：** 交货到欧盟一般不需要美国许可证，但卖方会要求：
  - 最终用户与用途声明；
  - 承诺不转出口到美国 D:1/D:4/D:5 国家组（含中国）或澳门，也不从这些地方远程访问；
  - 无军事用途声明；
  - 受限方名单筛查。
  - 另外，如果公司的总部或最终母公司在 D:5 国家组或澳门，即使交货地在西班牙也可能需要美国许可证。请律师确认 OZZIE 的股权结构。
- **查过但不适合询价：**
  - Eviden / Atos：BullSequana AI 用的是 AMD GPU，没有 HGX B300 产品；
  - KAYTUS：在西班牙没有业务；
  - Exclusive Networks：只做网络安全；
  - Seidor、Inetum、Sothis：没有转售 HGX 的公开证据；
  - Telefónica Tech：只卖算力服务，不卖硬件。
