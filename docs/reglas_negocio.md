# Reglas de negocio — Gasto del Estado en nube y licencias

| # | Regla | Estado |
|---|---|---|
| R1 | Fuentes: SECOP II Contratos Electrónicos (`jbjy-vk9h`) y Tienda Virtual del Estado Colombiano (`rgxm-mmea`). | Cerrada |
| R2 | Periodo desde 2020-01-01. SECOP II por `fecha_de_firma`; TVEC por `fecha`. | Cerrada |
| R3 | Alcance: nube y licencias. El reporte principal suma `nube` + `licencia`. | Cerrada |
| R4 | Fabricante: `microsoft`, `oracle`, `aws`, `google`, `multi_fabricante`, `otros`. Se deriva del texto, no del contratista (que suele ser revendedor). Excepción: si el proveedor es el propio fabricante (p. ej. Branch of Microsoft Colombia, Oracle Colombia), cuenta como señal de fabricante. | Cerrada |
| R5 | Contratos con varios fabricantes se marcan `multi_fabricante`. No se prorratea el valor. | Cerrada |
| R6 | Métrica: valor comprometido (`valor_del_contrato` en SECOP II, `total` en TVEC). Adiciones fuera por ahora. | Cerrada |
| R7 | Se excluyen del gasto los estados `Borrador` y `Cancelado` (SECOP II) y `Cancelado` (TVEC). No se borran: se marcan, para poder medir la tasa de cancelación. | Cerrada |
| R8 | `tipo_gasto`: `nube`, `licencia`, `soporte_fabricante`, `fuera_de_alcance`, `sin_clasificar`. La renovación de soporte y actualización de licencias (Oracle SULS / Software Update, Premier Support for Software, Microsoft Software Assurance) cuenta como `licencia`. El soporte técnico como servicio (Microsoft Unified / Premier Support, Oracle Premier Support for Systems) va en `soporte_fabricante`. | Cerrada |
| R9 | Computadores con licencia incluida (TVEC `etc`/`etp`) se excluyen en dbt: es compra de hardware y el valor de la licencia no viene separado. | Cerrada |
| R10 | Órdenes de Nube Pública que incluyen horas de expertos se cuentan completas como `nube`. No se prorratea. | Cerrada |
| R11 | Filtro de ingesta SECOP II: objeto con términos de fabricante (MICROSOFT, AZURE, OFFICE 365, ORACLE, AMAZON WEB SERVICES, AWS, GOOGLE, GCP, UNIFIED) o NUBE, CLOUD, SOFTWARE; o bien LICENCI / SUSCRIPCI **solo** si el UNSPSC empieza por 43, 8111 u 8116. Lo que solo tiene UNSPSC de tecnología sin palabras clave no entra. | Cerrada |
| R12 | Filtro de ingesta TVEC: fecha desde 2020 y `agregacion` o `items` con términos de fabricante o NUBE, CLOUD, SOFTWARE. LICENCI / SUSCRIPCI no se usan (TVEC no tiene UNSPSC para controlar el ruido). | Cerrada |
| R13 | Actualización: cada día se recargan los últimos 2 meses de ambas fuentes; cada semana, recarga completa desde 2020. Se ejecuta con GitHub Actions junto con dbt. | Cerrada |
| R14 | Criterios de clasificación: el software como servicio (SaaS) cuenta como `nube`; el soporte de un tercero sobre la plataforma de un fabricante es `fuera_de_alcance`; implementar un sistema de gestión documental (aunque se despliegue en la nube) es `fuera_de_alcance`; personas contratadas, desarrollo de software, BPO y computadores son `fuera_de_alcance`. Las reglas viven en seeds de dbt (`terminos_fabricante`, `proveedores_fabricante`, `reglas_tipo_gasto`) con prioridad única por tipo de gasto. | Cerrada |

## Calidad de la clasificación (muestra etiquetada de 60 registros)

- Primera medición: tipo de gasto 72 %, fabricante en alcance 96 %.
- Tras corregir el uso de `UNIFIED` (era parte del nombre de licencias M365, no solo de soporte): tipo de gasto 78 %, fabricante en alcance 96 %.
- La muestra la etiquetó el mismo asistente que escribió las reglas (antes de escribirlas) y la revisó el autor: la medición no es totalmente independiente.

## Limitaciones conocidas

- No se usa SECOP I: se pierden entidades que siguieron publicando allí después de 2020.
- Contratos de nube que no nombran al fabricante quedan como `otros` aunque probablemente sean de uno de los cuatro.
- Productos de un fabricante para la plataforma de otro (p. ej. licencias Fortinet para Azure) se atribuyen al fabricante de la plataforma.
- Licencias cuyo texto no usa palabras de licenciamiento (p. ej. "renovación del software RPA") quedan `sin_clasificar` y fuera del reporte.
- Contratos con UNSPSC de tecnología pero sin palabras clave quedan fuera de la ingesta (mayormente outsourcing, según la muestra 2025).
- Hay valores atípicos (un contrato de ~620 billones en SECOP II): se tratan con pruebas de calidad en dbt.
- Posible doble conteo entre TVEC y SECOP II: por verificar.
- Registros que desaparezcan de la fuente no se borran de la base (el upsert no elimina): por verificar si ocurre.

## Evidencia

`docs/exploracion_inicial.txt`, `docs/exploracion_detalle.txt`, `docs/medicion_palabras.txt`, `transformacion/seeds/etiquetas_manuales.csv`.