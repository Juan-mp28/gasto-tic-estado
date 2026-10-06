# Reglas de negocio — Gasto del Estado en nube y licencias

| # | Regla | Estado |
|---|---|---|
| R1 | Fuentes: SECOP II Contratos Electrónicos (`jbjy-vk9h`) y Tienda Virtual del Estado Colombiano (`rgxm-mmea`). | Cerrada |
| R2 | Periodo desde 2020-01-01. SECOP II por `fecha_de_firma`; TVEC por `fecha`. | Cerrada |
| R3 | Alcance: nube y licencias. El reporte principal suma `nube` + `licencia`. | Cerrada |
| R4 | Fabricante: `microsoft`, `oracle`, `aws`, `google`, `multi_fabricante`, `otros`. Se deriva del texto, no del contratista (que suele ser revendedor). | Cerrada |
| R5 | Contratos con varios fabricantes se marcan `multi_fabricante`. No se prorratea el valor. | Cerrada |
| R6 | Métrica: valor comprometido (`valor_del_contrato` en SECOP II, `total` en TVEC). Adiciones fuera por ahora. | Cerrada |
| R7 | Se excluyen los estados `Borrador` y `Cancelado`. | Cerrada |
| R8 | `tipo_gasto`: `nube`, `licencia`, `soporte_fabricante`, `fuera_de_alcance`. La renovación de soporte y actualización de licencias (Oracle SULS, Microsoft Software Assurance) cuenta como `licencia`. El soporte técnico como servicio (Microsoft Unified Support) va en `soporte_fabricante`. | Cerrada |
| R9 | Computadores con licencia incluida (TVEC `etc`/`etp`) se excluyen: es compra de hardware y el valor de la licencia no viene separado. | Cerrada |
| R10 | Órdenes de Nube Pública que incluyen horas de expertos se cuentan completas como `nube`. No se prorratea. | Cerrada |
| R11 | Filtro de ingesta SECOP II: objeto con términos de fabricante (MICROSOFT, AZURE, OFFICE 365, ORACLE, AMAZON WEB SERVICES, AWS, GOOGLE, GCP, UNIFIED) o NUBE, CLOUD, SOFTWARE; o bien LICENCI / SUSCRIPCI **solo** si el UNSPSC empieza por 43, 8111 u 8116. Lo que solo tiene UNSPSC de tecnología sin palabras clave no entra. | Cerrada |
| R12 | Filtro de ingesta TVEC: `agregacion` o `items` con términos de fabricante o NUBE, CLOUD, SOFTWARE. | Pendiente |

## Limitaciones conocidas

- No se usa SECOP I: se pierden entidades que siguieron publicando allí después de 2020.
- Contratos de nube que no nombran al fabricante quedan como `otros` aunque probablemente sean de uno de los cuatro.
- Contratos con UNSPSC de tecnología pero sin palabras clave quedan fuera (mayormente outsourcing, según la muestra 2025).
- Hay valores atípicos (la familia UNSPSC 8111 suma ~624 billones en 2024): se tratan con pruebas de calidad en dbt.
- Posible doble conteo entre TVEC y SECOP II: por verificar.

## Evidencia

`docs/exploracion_inicial.txt`, `docs/exploracion_detalle.txt`, `docs/medicion_palabras.txt`.