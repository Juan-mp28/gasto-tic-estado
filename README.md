# Estado del proyecto — al 8 de octubre de 2026

## Hecho
- **Ingesta (Python):** `ingesta/api.py`, `carga.py`, `reglas.py`, `secop.py`, `tvec.py`, `db.py`. Carga mensual con reintentos, paginación verificada (esperadas = leídas = únicas), upsert y bitácora en `raw.cargas`. Los scripts terminan con error (`sys.exit`) si algún mes queda en error o incompleto.
- **Carga histórica completa:** SECOP II 2020–oct 2026 (46.090 contratos) y TVEC 2020–oct 2026 (~8.700 órdenes). Base ~64 MB antes de dbt, ~85 MB después.
- **Conexión:** variables PG* en `.env` local y en GitHub Secrets, vía session pooler de Supabase.
- **dbt 1.12.5 + dbt-postgres 1.11.0** sobre Python 3.14, proyecto en `transformacion/`, esquema `analitica`, `--profiles-dir .`. `dbt test`: 13/13 pasan.
- **Modelos:** staging, intermediate (`int_registros`, `int_clasificacion`), calidad (`evaluacion_muestra`), marts (`fct_gasto_tic` 21.614 filas, `mart_gasto_entidad_fabricante`, `mart_cancelaciones`), prueba `valor_atipico_en_gasto` (warn).
- **Clasificación por reglas en seeds**, evaluada con 60 registros: tipo de gasto 78 %, fabricante en alcance 96 %.
- **Resultado por fabricante (fct_gasto_tic):** otros 67 % del valor, Microsoft 28 % (~3,03 billones), Oracle ~0,24, Google ~0,19, multi ~0,04, AWS ~0,016 billones.
- **Rama Judicial:** se mantiene por dependencia (CSJ y DEAJ separadas). Decisión A.
- **Paso 8 — GitHub Actions** (`.github/workflows/pipeline.yml`): lunes a sábado 11:17 UTC ventana (mes anterior + actual); domingo 09:23 UTC recarga completa desde 2020; `workflow_dispatch` con modo ventana/completa; luego `dbt build`.
  - Ejecución #3 (ventana, manual): verde, 1m52s.
  - Ejecución #4 (completa, manual, 7 oct): verde, 18 min.
- **Lanzar workflows desde el codespace:** el `GITHUB_TOKEN` del codespace no tiene permiso (403). Hay que hacer `unset GITHUB_TOKEN` + `gh auth login` con la cuenta personal, o usar la web.

## Pendiente
1. Confirmar que las ejecuciones programadas (cron) se disparan solas.
2. `git pull` en el codespace (el workflow se editó en GitHub).
3. README del portafolio (siguiente paso).
4. Revisar el peso de `otros` (posible AWS/Google vía revendedores que no nombran al fabricante). AWS bajo: no se sabe si es real o efecto de clasificación.
5. Validar la regla `actualizacion_licencias` en Oracle (SULS vs Premier Support for Systems).
6. Después: capa de consumo (dashboard).

## Riesgos operativos
- Supabase free pausa el proyecto tras 7 días sin actividad; el workflow diario lo mantiene activo.
- GitHub desactiva los workflows programados tras 60 días sin actividad en el repo público: hay que hacer algún commit o reactivarlo a mano.
