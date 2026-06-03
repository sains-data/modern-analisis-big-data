-- zscore_prevalensi_desa.sql — referensi Spark/Sedona (Bab 17)

-- Stunting per balita (z < -2)
WITH scored AS (
  SELECT
    b.desa_id,
    b.balita_id,
    CASE WHEN b.z_tb_u < -2 THEN 1 ELSE 0 END AS is_stunting
  FROM silver.data_balita b
),
agg AS (
  SELECT
    desa_id,
    COUNT(*) AS n_balita,
    SUM(is_stunting) AS n_stunting
  FROM scored
  GROUP BY desa_id
  HAVING COUNT(*) >= 10
)
SELECT
  desa_id,
  n_balita,
  n_stunting,
  ROUND(100.0 * n_stunting / n_balita, 2) AS prev_pct
FROM agg;
