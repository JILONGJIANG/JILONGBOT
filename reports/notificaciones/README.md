# 房东通知函（储能柜安装前）

| 文件 | 收件人 | 发件主体 |
|---|---|---|
| `PLANTILLA_…docx` | 通用模板，方括号 [ ] 为待填字段 | — |
| `01_LOS_TINTOS_…docx` | Ganados Garsan S.L.（B45341070），Calle Lanzarote 2, Polán；Pablo García Vivar 607 781 233 | Torrebesse Solar C.A. S.L.（B06912224） |
| `02_PARCELA_108_…docx` | Juan Jiménez García S.A. / JISAP（A30127849），Lorca；Alfonso Jiménez Reverte | Helianthus Energy 2020 S.L.（B02747715） |
| `03_ZAGUISA_POZO_…docx` | Zaguisa 88 S.A.（A45202728），La Pueblanueva；Natalia Rodríguez García 673 929 985 | Torrebesse |
| `04_AVICOLA_BRAOJOS_…docx` | Explotaciones Avícolas Braojos Cabello S.L.（B01998517），Gálvez；联系人待补 | Torrebesse |
| `05_ROMANITOS_…docx` | Porcibra Romanitos S.L.（B45798949），Noez；联系人待核 | Torrebesse |
| `06_TOTANES_…docx` | Totacer S. Coop. de C-LM（F45307808），Yeles（Apdo. Correos 15）；联系人待补 | Torrebesse |
| `07_ALPUEBREGA_…docx` | Francisco Javier Barroso Lorente（03866335N，须核实为出租人），Polán；Pablo García 607 781 233 | Torrebesse |

数据来源：SharePoint Energia 站点档案（租约、i-DE 许可、电费单、ficha），提取日期 2026-09-14。

结构：正文（合同引用、设备与位置、工期与吊车进场、许可前置、15 天答复请求）→ Anexo I 房东同意书（位置确认、联系人、日期、签字）→ Anexo II 布置图占位与技术摘要表。

**发出前仍需人工填写：** 发函日期与地点、开工日期、储能柜位置描述与布置图（Anexo II）；Romanitos、Totanes、Braojos、Alpuebrega 的租约签署日期（签署版为扫描件）；Braojos、Totanes 联系人；Alpuebrega 出租人身份。签字人已预填 Dan Shan Wang（两家 SPV 的 administradora）。

**电子送达：** correo electrónico certificado 或 burofax electrónico con acuse de recibo。邮件正文建议：

> Asunto: Comunicación previa – instalación de batería junto a la planta fotovoltaica de [sitio]
>
> Estimado/a [contacto]: Adjuntamos comunicación formal de [SPV] relativa a la instalación de un sistema de almacenamiento (batería de 261 kWh, 100 kW) junto a la instalación fotovoltaica de [sitio], en la finca objeto del contrato de arrendamiento de [fecha]. Les rogamos nos devuelvan firmado el Anexo I en un plazo de 15 días, o nos indiquen cualquier observación sobre la ubicación propuesta. No se iniciará ninguna obra sin su conformidad y sin los permisos correspondientes. Quedamos a su disposición en ingenieria@energiarea.es / 933 993 099. Atentamente, [firmante], [SPV].

同意书签回后作为租赁合同附件归档到各站 02 目录。

重新生成：在 `reports/notificaciones/` 下 `npm install docx && node notif.js`（`sites` 数组中每站一条记录）。
