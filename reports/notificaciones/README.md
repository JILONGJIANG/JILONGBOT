# 房东通知函（储能柜安装前）

| 文件 | 用途 |
|---|---|
| `PLANTILLA_Notificacion_arrendador_almacenamiento.docx` | 通用模板，方括号 [ ] 为待填字段：房东名称与 NIF、合同类型与日期、地籍号、储能位置、开工日期、发件主体、签字人 |
| `LOS_TINTOS_Notificacion_arrendador_almacenamiento.docx` | Los Tintos 预填版（Ganados Garsan S.L., Calle Lanzarote 2, 45161 Polán, Tel. 607 781 233；发件主体 Torrebesse Solar CA S.L.，NIF 待核） |

结构：正文（合同引用、设备与位置、工期与吊车进场、许可前置、15 天答复请求）→ Anexo I 房东同意书（位置确认、联系人、日期、签字）→ Anexo II 布置图占位与技术摘要表。

发送方式：correo electrónico certificado 或 burofax electrónico con acuse de recibo；同意书签回后作为租赁合同附件归档。

重新生成：`node scratchpad/notif.js`（脚本见 `reports/notificaciones/notif.js`），在 `sites` 数组中为每个站点增加一条记录即可批量生成。
