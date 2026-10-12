const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,AlignmentType,BorderStyle,ShadingType,LevelFormat,HeadingLevel,PageBreak}=require('docx');

function build(d){
  const F='Calibri';
  const P=(t,o={})=>new Paragraph({spacing:{after:120,line:300},...o,children:[new TextRun({text:t,font:F,size:22,...(o.run||{})})]});
  const B=(t)=>new Paragraph({spacing:{after:120,line:300},children:[new TextRun({text:t,font:F,size:22,bold:true})]});
  const H=(t)=>new Paragraph({spacing:{before:240,after:120},children:[new TextRun({text:t,font:F,size:24,bold:true,color:'0F4C5C'})]});
  const LI=(t)=>new Paragraph({numbering:{reference:'bul',level:0},spacing:{after:80,line:300},children:[new TextRun({text:t,font:F,size:22})]});
  const NUM=(t)=>new Paragraph({numbering:{reference:'num',level:0},spacing:{after:80,line:300},children:[new TextRun({text:t,font:F,size:22})]});
  const cell=(t,w,shade)=>new TableCell({width:{size:w,type:WidthType.DXA},shading:shade?{type:ShadingType.CLEAR,fill:'E8EEF0',color:'auto'}:undefined,margins:{top:60,bottom:60,left:100,right:100},children:[new Paragraph({children:[new TextRun({text:t,font:F,size:20,bold:!!shade})]})]});
  const tbl=(rows,w=[3200,6160])=>new Table({columnWidths:w,width:{size:w.reduce((a,b)=>a+b),type:WidthType.DXA},rows:rows.map((r,i)=>new TableRow({children:r.map((c,j)=>cell(c,w[j],j===0))}))});
  const rule=new Paragraph({spacing:{after:200},border:{bottom:{style:BorderStyle.SINGLE,size:6,color:'0F4C5C'}},children:[]});

  const children=[
    new Paragraph({spacing:{after:0},children:[new TextRun({text:d.emisor,font:F,size:24,bold:true,color:'0F4C5C'})]}),
    P(`NIF ${d.emisorNIF} · ${d.emisorDir}`,{run:{size:20,color:'555555'}}),
    P(`Tel. ${d.emisorTel} · ${d.emisorMail}`,{run:{size:20,color:'555555'}}),
    rule,
    P(`${d.lugarFecha}`,{alignment:AlignmentType.RIGHT}),
    B(d.arrendador), P(`NIF ${d.arrendadorNIF}`), P(d.arrendadorDir), P(`A la atención de: ${d.contacto}`),
    P(`Enviado por: ${d.canal}`,{run:{size:20,color:'555555'}}),
    new Paragraph({spacing:{before:200,after:200},children:[new TextRun({text:'Asunto: ',font:F,size:22,bold:true}),new TextRun({text:`Comunicación previa de obras e solicitud de conformidad – instalación de un sistema de almacenamiento de energía (batería) junto a la instalación fotovoltaica de ${d.sitio}`,font:F,size:22,bold:true})]}),
    P('Estimado/a Sr./Sra.:'),
    P(`En virtud del contrato de ${d.tipoContrato} de fecha ${d.fechaContrato} relativo a la finca ${d.finca} (referencia catastral ${d.refCatastral}), en la que ${d.estadoFV} la instalación fotovoltaica de ${d.potenciaFV} de la que ${d.emisor} es titular, les comunicamos nuestra intención de incorporar a dicha instalación un sistema de almacenamiento de energía mediante baterías, con el fin de aumentar el autoconsumo de la energía solar generada y mejorar la continuidad del suministro.`),
    H('1. Descripción de la actuación'),
    tbl([
      ['Equipo','Armario de baterías exterior Dunext PowerHill, 261 kWh, tecnología litio-ferrofosfato (LFP)'],
      ['Potencia','Limitada a 100 kW de carga/descarga (sin aumento de la potencia de conexión a la red)'],
      ['Dimensiones y peso','1.026 × 2.366 × 1.350 mm (ancho × alto × fondo), aprox. 2.800 kg'],
      ['Ubicación prevista',`${d.ubicacion} (según plano adjunto, Anexo II), a más de 3 m de cualquier edificación`],
      ['Obra civil','Losa de hormigón de aprox. 1,3 × 1,7 m sobre terreno nivelado, con 3 m libres frontales para mantenimiento'],
      ['Conexión','Al cuadro de la instalación fotovoltaica existente; no se modifica el suministro eléctrico de la explotación'],
      ['Seguridad','Ensayos UL 9540A e IEC 62619, envolvente IP55, sistema de detección y extinción integrado, nivel sonoro ≤ 70 dB(A) a 1 m'],
      ['Coste para el arrendador','Ninguno. La inversión, permisos, seguros y mantenimiento son a cargo de '+d.emisor],
    ]),
    H('2. Calendario y acceso'),
    P(`Fecha prevista de inicio: ${d.fechaInicio}. Duración estimada: ${d.duracion}, en horario de ${d.horario}.`),
    NUM('Día 1–2: replanteo y ejecución de la losa de hormigón.'),
    NUM(`Día ${d.diaGrua}: entrega del armario en camión con grúa o carretilla de ≥ 4 t; se requiere acceso de vehículo pesado hasta el punto de instalación.`),
    NUM('Días siguientes: conexionado eléctrico, pruebas y puesta en marcha con presencia del instalador autorizado.'),
    P(`No se iniciará ninguna actuación sin haber recibido su conformidad por escrito y sin disponer de los permisos correspondientes (licencia municipal de obras, actualización de los permisos de acceso y conexión de ${d.distribuidora} y, en su caso, autorización de la administración autonómica).`),
    H('3. Lo que les solicitamos'),
    LI('Devolver firmado el Anexo I (conformidad del arrendador) en un plazo de 15 días naturales desde la recepción de esta comunicación, o responder por correo electrónico a la dirección indicada.'),
    LI('Confirmar la ubicación propuesta o indicar una alternativa dentro de la finca.'),
    LI('Indicar persona de contacto y fechas preferentes para el acceso, así como cualquier condicionante de la explotación (presencia de animales, caminos de acceso, líneas o conducciones enterradas, horarios).'),
    P(`Quedamos a su disposición para cualquier aclaración en el teléfono ${d.emisorTel} o en ${d.emisorMail}. Les agradecemos su colaboración.`),
    P('Atentamente,'),
    new Paragraph({spacing:{before:400,after:0},children:[new TextRun({text:d.firmante,font:F,size:22,bold:true})]}),
    P(`${d.cargo} · ${d.emisor}`),
    P('Adjuntos: Anexo I – Conformidad del arrendador · Anexo II – Plano de ubicación y ficha técnica resumen',{run:{size:20,color:'555555'}}),
    new Paragraph({children:[new PageBreak()]}),
    new Paragraph({spacing:{after:200},children:[new TextRun({text:'ANEXO I – CONFORMIDAD DEL ARRENDADOR',font:F,size:26,bold:true,color:'0F4C5C'})]}),
    P(`D./Dña. ______________________________________, con DNI/NIE __________________, en representación de ${d.arrendador} (NIF ${d.arrendadorNIF}), en su condición de propietario/arrendador de la finca ${d.finca},`),
    B('DECLARA'),
    NUM(`Que ha recibido la comunicación previa de ${d.emisor} de fecha ${d.fechaCarta} relativa a la instalación de un sistema de almacenamiento de energía (batería de 261 kWh, 100 kW) junto a la instalación fotovoltaica existente.`),
    NUM('Que presta su conformidad a la instalación en la ubicación propuesta en el Anexo II  ☐  /  en la ubicación alternativa siguiente: ______________________________  ☐'),
    NUM('Que autoriza el acceso a la finca del personal y vehículos necesarios (incluido camión grúa) en las fechas que se acuerden con la persona de contacto indicada a continuación.'),
    NUM('Que la presente conformidad se entiende como anexo al contrato de referencia, sin modificación de sus restantes condiciones económicas, salvo pacto expreso posterior entre las partes.'),
    tbl([
      ['Persona de contacto en la finca','__________________________________'],
      ['Teléfono / correo electrónico','__________________________________'],
      ['Fechas u horarios preferentes','__________________________________'],
      ['Condicionantes de la explotación','__________________________________'],
      ['Observaciones','__________________________________'],
    ]),
    P(''),
    P('En ______________________, a ____ de ______________ de 2026'),
    P(''),
    P('Firma y sello: ______________________________'),
    new Paragraph({children:[new PageBreak()]}),
    new Paragraph({spacing:{after:200},children:[new TextRun({text:'ANEXO II – PLANO DE UBICACIÓN Y FICHA TÉCNICA RESUMEN',font:F,size:26,bold:true,color:'0F4C5C'})]}),
    P('[Insertar plano de emplazamiento con la posición del armario, distancias a edificaciones (≥ 3 m), zona de maniobra de la grúa y trazado del cableado hasta el cuadro fotovoltaico]',{run:{italics:true,color:'777777'}}),
    tbl([
      ['Instalación fotovoltaica existente',`${d.potenciaFV} · ${d.sitio} · CUPS/CIL ${d.cups}`],
      ['Sistema de almacenamiento','Dunext PowerHill P125-261, 261 kWh LFP, PCS limitado a 100 kW'],
      ['Modo de operación','Carga desde la instalación fotovoltaica; descarga para autoconsumo y apoyo de la explotación'],
      ['Normativa y certificados','UL 9540A (celda, módulo y unidad), IEC 62619, IEC 62933-5-2, UNE 217001/217002, EN 50549; RD 244/2019; RD 1183/2020 art. 27'],
      ['Distancias de seguridad','≥ 3,05 m a edificaciones (o 0,91 m con muro cortafuegos de 1 h); salida de venteo a > 4,6 m de puertas, ventanas y tomas de aire'],
      ['Ruido','≤ 70 dB(A) a 1 m del armario; ≤ 45 dB(A) nocturnos en fachada de vivienda más próxima'],
      ['Mantenimiento','Visitas de inspección periódicas por '+d.emisor+'; aviso previo de 48 h'],
      ['Seguros','Responsabilidad civil y daños materiales de la instalación a cargo de '+d.emisor],
      ['Contacto técnico',`${d.emisorMail} · ${d.emisorTel}`],
    ]),
  ];
  return new Document({
    styles:{default:{document:{run:{font:F,size:22}}}},
    numbering:{config:[
      {reference:'bul',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:270}}}}]},
      {reference:'num',levels:[{level:0,format:LevelFormat.DECIMAL,text:'%1.',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:360}}}}]},
    ]},
    sections:[{properties:{page:{margin:{top:1200,bottom:1100,left:1300,right:1300}}},children}],
  });
}

const base={
  emisor:'TORREBESSE SOLAR C.A., S.L.',emisorNIF:'B06912224',emisorDir:'Plaza de Tetuán 29, bajos, 08010 Barcelona',
  emisorTel:'933 993 099 / 688 555 906',emisorMail:'ingenieria@energiarea.es',
  distribuidora:'i-DE Redes Eléctricas Inteligentes',firmante:'Dan Shan Wang',cargo:'Administradora',
  canal:'correo electrónico certificado / burofax electrónico con acuse de recibo',
  fechaCarta:'[dd/mm/2026]',lugarFecha:'Barcelona, [dd] de [mes] de 2026',
  fechaInicio:'[dd/mm/2026] (a confirmar)',duracion:'3–5 días laborables',horario:'8:00 a 18:00',diaGrua:'3',
  cups:'[CUPS/CIL]',ubicacion:'[Descripción de la ubicación: p. ej. junto al cuadro de inversores, lado norte de la nave]',
  estadoFV:'se encuentra en explotación',tipoContrato:'arrendamiento (y su cesión)',
};
const sites=[
  {file:'PLANTILLA_Notificacion_arrendador_almacenamiento.docx',...base,
   emisor:'[Razón social de la SPV]',emisorNIF:'[NIF]',firmante:'[Nombre del firmante]',cargo:'[Cargo]',
   arrendador:'[Razón social del arrendador]',arrendadorNIF:'[NIF]',arrendadorDir:'[Dirección]',contacto:'[Persona de contacto]',
   sitio:'[Nombre del emplazamiento]',tipoContrato:'arrendamiento / cesión',fechaContrato:'[dd/mm/aaaa]',finca:'[polígono/parcela, municipio, provincia]',refCatastral:'[referencia catastral]',potenciaFV:'100 kW',
   estadoFV:'se encuentra en explotación / está prevista'},
  {file:'01_LOS_TINTOS_Notificacion_arrendador_almacenamiento.docx',...base,
   arrendador:'GANADOS GARSAN, S.L.',arrendadorNIF:'B45341070',arrendadorDir:'Calle Lanzarote 2, 45161 Polán (Toledo)',contacto:'D. Pablo García Vivar · Tel. 607 781 233',
   sitio:'Granja Los Tintos, Polán (Toledo)',tipoContrato:'arrendamiento de 17/05/2022 (cedido a Torrebesse Solar C.A., S.L. el 23/05/2022)',fechaContrato:'17/05/2022',
   finca:'Los Tintos, polígono 14 parcela 159, Cam. Dehesilla 38, 45161 Polán (Toledo)',refCatastral:'45134A014001590000ED',potenciaFV:'134,14 kWp / 100 kW',cups:'ES0021000007425612AJ (CAU ES0021000007425612AJ1FA000)'},
  {file:'02_PARCELA_108_Notificacion_arrendador_almacenamiento.docx',...base,
   emisor:'HELIANTHUS ENERGY 2020, S.L.',emisorNIF:'B02747715',emisorDir:'Plaza de Tetuán 29, bajos, 08010 Barcelona',
   arrendador:'JUAN JIMÉNEZ GARCÍA, S.A. (Grupo JISAP)',arrendadorNIF:'A30127849',arrendadorDir:'Avda. José Montoya García, Pol. Ind. Saprelorca, Ed. JISAP Parc. A, Lorca (Murcia)',contacto:'D. Alfonso Jiménez Reverte',
   sitio:'JISAP Parcela 108, Malpica de Tajo (Toledo)',tipoContrato:'arrendamiento de 05/01/2023 y su Anexo de 27/09/2023',fechaContrato:'05/01/2023',
   finca:'Finca Hornaguera Alta, polígono 19 parcela 108, 45692 Malpica de Tajo (Toledo)',refCatastral:'45090A019001080000TJ',potenciaFV:'100 kW',cups:'ES0021000011764649BP (CIL ES0021000011764649BP1F002)'},
  {file:'03_ZAGUISA_POZO_Notificacion_arrendador_almacenamiento.docx',...base,
   arrendador:'ZAGUISA 88, S.A.',arrendadorNIF:'A45202728',arrendadorDir:'Calle Miguel Hernández 14, 45690 La Pueblanueva (Toledo)',contacto:'Dña. Natalia Rodríguez García · Tel. 673 929 985 · zaguiza88sa@gmail.com',
   sitio:'Granja El Pozo, La Pueblanueva (Toledo)',tipoContrato:'arrendamiento de 17/02/2023 (suscrito por Rifer Machinery, S.L. y cedido a Torrebesse Solar C.A., S.L.)',fechaContrato:'17/02/2023',
   finca:'Granja El Pozo, Las Escalerillas, polígono 35 parcela 90, Ctra. Pueblanueva a San Martín 1, 45690 La Pueblanueva (Toledo)',refCatastral:'45138A035000900000LF',potenciaFV:'136 kWp / 100 kW',cups:'ES0021000007435478HN'},
  {file:'04_AVICOLA_BRAOJOS_Notificacion_arrendador_almacenamiento.docx',...base,
   arrendador:'EXPLOTACIONES AVÍCOLAS BRAOJOS CABELLO, S.L.',arrendadorNIF:'B01998517',arrendadorDir:'Calle Santa Teresa de Jesús 20, 45164 Gálvez (Toledo)',contacto:'[Persona de contacto]',
   sitio:'Avícola Braojos, Gálvez (Toledo)',tipoContrato:'arrendamiento (suscrito por Rifer Machinery, S.L. y cedido a Torrebesse Solar C.A., S.L.)',fechaContrato:'[dd/mm/2023 – ver archivo 2.1.2]',
   finca:'Camino Menasalbas 2, polígono 14 parcela 31, 45164 Gálvez (Toledo)',refCatastral:'45067A014000310000KK',potenciaFV:'136 kWp / 100 kW',cups:'ES0021000007371874JA',
   estadoFV:'está prevista (permiso de acceso y conexión i-DE ref. 9042281047)'},
  {file:'05_ROMANITOS_Notificacion_arrendador_almacenamiento.docx',...base,
   arrendador:'PORCIBRA ROMANITOS, S.L.',arrendadorNIF:'B45798949',arrendadorDir:'Polígono 5, Paraje Atochar Gordo, Sierrejuela, parcela 60, 45162 Noez (Toledo)',contacto:'[Persona de contacto – ficha: Juanma Braojo · Tel. 670 841 214, verificar]',
   sitio:'Granja Romanitos, Noez (Toledo)',tipoContrato:'acuerdo de colaboración y arrendamiento (cedido a Torrebesse Solar C.A., S.L.)',fechaContrato:'[dd/mm/aaaa – ver archivos 2.1.1 y 2.1.3]',
   finca:'Ctra. Noez a Pulgar km 0,1, polígono 5 parcela 60, Sierrejuela, 45162 Noez (Toledo)',refCatastral:'45117A005000600000TH',potenciaFV:'125,28 kWp / 100 kW',cups:'ES0021000007414732JN'},
  {file:'06_TOTANES_Notificacion_arrendador_almacenamiento.docx',...base,
   arrendador:'TOTACER, S. COOP. DE C-LM',arrendadorNIF:'F45307808',arrendadorDir:'Cra. Serranillos s/n, 45220 Yeles (Toledo) · Correo: Apartado de Correos 15, 45220 Estación de Yeles (Toledo)',contacto:'[Persona de contacto]',
   sitio:'Totanes (Secaderos y Semillas La Sagra), Totanés (Toledo)',tipoContrato:'acuerdo de colaboración y arrendamiento (cedido a Torrebesse Solar C.A., S.L.)',fechaContrato:'[dd/mm/aaaa – ver archivos 2.1.1 y 2.1.3]',
   finca:'Camino Sierra 20, polígono 1 parcela 215, Aceres, 45163 Totanés (Toledo)',refCatastral:'45175A001002150000RH',potenciaFV:'252,72 kWp',cups:'ES0021000007566896MP',
   estadoFV:'se encuentra en explotación en modalidad de autoconsumo sin excedentes'},
  {file:'07_ALPUEBREGA_Notificacion_arrendador_almacenamiento.docx',...base,
   arrendador:'D. Francisco Javier Barroso Lorente [verificar que es el arrendador]',arrendadorNIF:'03866335N',arrendadorDir:'Avda. San Sebastián 110, 45161 Polán (Toledo)',contacto:'D. Pablo García · Tel. 607 781 233',
   sitio:'Finca Alpuebrega, Polán (Toledo)',tipoContrato:'acuerdo de colaboración y arrendamiento (cedido a Torrebesse Solar C.A., S.L.)',fechaContrato:'[dd/mm/aaaa – ver archivos 2.1.1 y 2.1.3]',
   finca:'Finca La Alpedruega 1, polígono 17 parcela 177, 45161 Polán (Toledo)',refCatastral:'45134A017001770000ET',potenciaFV:'136 kWp / 100 kW',cups:'ES0021000007425072AW (CAU ES0021000007425072AW1FA000)',
   estadoFV:'está prevista (permiso de acceso y conexión i-DE ref. 9041839919 de 23/11/2022)'},
];
(async()=>{for(const s of sites){const buf=await Packer.toBuffer(build(s));fs.writeFileSync('/home/user/JILONGBOT/reports/notificaciones/'+s.file,buf);console.log('ok',s.file);}})();
