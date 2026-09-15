# 回复 TD SYNNEX（Efrén Figueroa）— 单台 HGX B300

**取代：** `2026-09-15_TDSYNNEX_Lenovo_H200_respuesta.md`（7–10 站点 H200 版本，已作废）
**变更原因：** 选型改为 B300，数量改为单台，安装地点改为 Montgat 自有住宅内的技术间。

**来函要点（Efrén，2026-09-14 18:44）：** 需要协助办附件里的登记可以找他们；如果我们已在推进，拿到确认后通知他一起做；可打他签名里的电话。
**抄送：** Alexandre Bento（Lenovo）、Alex Cruzado（TD SYNNEX）、Eva Subias、Shan Dan、Rosario。

---

## 发出前必须填写的空格

| 位置 | 需要填入 |
|---|---|
| 公司注册地址 | OZZIE INTERNATIONAL 2019, S.L. 的税务住所 |
| 联系电话 | 吉隆的手机或座机 |
| 行政与开票联系人 | 姓名与邮箱 |
| 开户文件寄出日期 | 承诺的日期 |
| 付款条件 | 30 天还是 60 天 |
| 通话时间 | 可约的日期与时段 |

**发出前自查：** 附件里的 alta 表格是否已填好寄出。若已寄出，第 1 节首句改为 `Ya os hemos enviado el formulario el [fecha]; confírmame si lo habéis recibido y si falta algo`。

---

## 西语回复正文

Asunto: RE: Dada de Alta Jilong & Preparación de Oferta — Jilong Group / OZZIE INTERNATIONAL 2019, S.L. — Petición de oferta: 1 × NVIDIA HGX B300 (8 GPU, refrigeración líquida)

Hola Efrén,

Muchas gracias por tu respuesta y por vuestra disponibilidad.

Antes de nada, una corrección importante respecto a mi correo anterior: **hemos cambiado el alcance del proyecto**. En lugar de varios nodos H200 distribuidos en emplazamientos agrícolas, vamos a empezar con **una sola unidad basada en NVIDIA B300**, instalada en un inmueble propio. Prefiero validar la operación con un único nodo antes de plantear cualquier despliegue. Te pido por tanto que descartéis la petición anterior y trabajemos sobre lo que describo aquí.

### 1. Alta de cliente

Estamos completando la documentación del alta. Los datos de la sociedad son:

- Razón social: OZZIE INTERNATIONAL 2019, S.L.
- NIF: B67488866
- Domicilio social: [dirección fiscal]
- Contacto del proyecto y compras: Jilong Jiang — jilong@jilong.es — [teléfono]
- Administración y facturación: [nombre] — [correo]

Os enviaré el formulario firmado antes del [fecha], junto con el certificado de titularidad bancaria y el modelo 036. Si necesitáis algún documento adicional (escritura de constitución, poderes del firmante, últimas cuentas depositadas o informe de solvencia), indícamelo y lo incluyo en el mismo envío para no encadenar requerimientos.

Sobre condiciones comerciales nos interesa estudiar dos vías en paralelo: línea de crédito con pago a [30/60] días, y una operación de renting o leasing. Sobre esto último te pido una cosa concreta en el punto 4.

### 2. Registro de la oportunidad

Os pedimos que abráis el registro de oportunidad con Lenovo y con NVIDIA a nombre de OZZIE INTERNATIONAL 2019, S.L. antes de emitir la primera oferta, de forma que trabajemos con precio de proyecto desde el principio. Decidme qué necesitáis de nuestra parte.

### 3. Qué queremos que nos ofertéis

**Configuración principal: 1 × sistema HGX B300 de 8 GPU, refrigeración líquida.**

**Configuración alternativa, en la misma oferta: 1 × sistema B300 de 4 GPU.** Nos interesa mucho verla. Para una primera unidad de validación, la mitad de inversión y la mitad de potencia eléctrica puede encajarnos mejor, y queremos poder comparar las dos con números reales antes de decidir.

Para cada una de las dos configuraciones necesitamos:

1. **Modelo exacto** del servidor y configuración propuesta de CPU, memoria, almacenamiento y red.
2. **Consumo eléctrico real sostenido en carga**, no el valor de placa, y consumo adicional del sistema de refrigeración. Este dato condiciona todo nuestro diseño eléctrico, así que es el más importante de la oferta.
3. **Refrigeración líquida**: si Lenovo suministra el CDU y el disipador exterior como parte de la solución, o si debemos integrarlos localmente. En el primer caso, incluidlos en la oferta.
4. **Datos físicos**: peso y dimensiones del sistema completo, si se puede transportar desmontado y qué anchura de paso y qué pendiente máxima admite la manipulación. Lo pregunto porque el acceso al local es por una puerta de garaje y una rampa.
5. **Envolvente ambiental**: rango de temperatura y humedad de operación admisible y requisitos de limpieza del aire.
6. **Ubicación**: la instalación irá en una sala técnica acondicionada dentro de un inmueble propio en Montgat (Barcelona). **No es un centro de datos.** Confirmadme si esto afecta de algún modo a la garantía o al soporte del fabricante, porque prefiero saberlo ahora y no después.
7. **Garantía y soporte**: nivel de servicio en la provincia de Barcelona, tiempo de respuesta, si hay intervención in situ y precio de la extensión a tres y a cinco años.
8. **Plazo de entrega** para una unidad.
9. **Licencias de software**: NVIDIA AI Enterprise u otras necesarias, si van incluidas y su coste anual.
10. **Precio**: precio de una unidad, y a título indicativo el escalado a dos y a cuatro unidades, puesto en destino e impuestos aparte.

### 4. Financiación

Dado que se trata de una única unidad, la estructura de financiación nos condiciona la decisión tanto como el precio. Os pido presupuesto para:

- **Leasing o renting a 60 y a 84 meses.** Los plazos cortos no nos encajan: la vida económica útil de este tipo de equipo es de tres a cinco años y necesitamos que la cuota sea compatible con los ingresos reales de la máquina, no con los del primer año.
- Valor residual y opciones a vencimiento en el caso de renting.
- Documentación que pide la entidad financiera, para ir preparándola en paralelo al alta.

### 5. Siguientes pasos

Propongo una llamada de treinta minutos esta semana o la próxima, con vosotros y con Alexandre, para repasar los puntos 3 y 4. Estoy disponible [días y franja horaria].

Si existe la posibilidad de acceder a una unidad de prueba o a un centro de demostración de Lenovo para medir consumo y comportamiento térmico antes del pedido, nos interesa mucho y estamos dispuestos a desplazarnos.

Quedo a la espera y gracias de nuevo por la rapidez.

Un saludo,

Jilong Jiang
OZZIE INTERNATIONAL 2019, S.L. — NIF B67488866
jilong@jilong.es — [teléfono]

---

## 中文对照与要点

**开头先撤回上一版。** 上一封讲的是 7–10 个农场站点的 H200，方向已经变了。与其让对方猜，不如明说"改了范围，请按新的来"，这样不会收到一份基于旧需求的报价浪费两周。

**第 3 节多要了一个 4 卡方案。** 这是本封邮件最有价值的一句。4 卡 B300 投资腰斩、功率减半，对"先买一台验证"这个目标可能比 8 卡更合适。多问一句不花钱，但可能省一半钱。

**第 3.2 项写明要"真实持续功耗，不要铭牌值"。** 别墅只有 43.64 kW 三相，整机到底是 14 kW 还是 18 kW 直接决定配电设计和能不能放第二台。

**第 3.6 项主动交代安装在住宅内。** 这件事瞒不住，而且会影响原厂保修与上门服务。现在问清楚，比装完再发现保修不认要好得多。

**第 4 节把融资期限点破。** 我们算过，三年期无论如何还不上，七年期才有正现金流。所以直接要 60 个月和 84 个月两个方案，并说明理由是设备经济寿命，这个理由对方无法反驳。

**没有提的两件事：**

- 没提我们的目标价。让他们先出价。
- 没提我们还没拿到 Montgat 的用地许可。报价不需要许可，可以并行走；但**在许可拿到之前不要签采购合同**。
