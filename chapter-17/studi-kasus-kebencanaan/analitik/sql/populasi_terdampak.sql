-- populasi_terdampak.sql — Sedona/Spark SQL (referensi Bab 17)
-- Eksekusi di cluster dengan tabel Iceberg: silver.kelurahan_sumsel, gold.genangan_aktif

WITH kel AS (
  SELECT
    kode_kel,
    nama_kel,
    kabupaten,
    jumlah_penduduk,
    geometry AS geom_kel
  FROM silver.kelurahan_sumsel
),
gen AS (
  SELECT
    genangan_id,
    snapshot_ts,
    geometry AS geom_gen
  FROM gold.genangan_aktif
  WHERE snapshot_ts >= current_timestamp() - INTERVAL 1 HOUR
),
intersected AS (
  SELECT
    k.kode_kel,
    k.nama_kel,
    k.kabupaten,
    k.jumlah_penduduk,
    g.genangan_id,
    ST_Area(
      ST_Intersection(
        ST_Transform(k.geom_kel, 'EPSG:32748'),
        ST_Transform(g.geom_gen, 'EPSG:32748')
      )
    ) AS luas_intersect_m2,
    ST_Area(ST_Transform(k.geom_kel, 'EPSG:32748')) AS luas_kel_m2
  FROM kel k
  INNER JOIN gen g
    ON ST_Intersects(k.geom_kel, g.geom_gen)
)
SELECT
  kode_kel,
  nama_kel,
  kabupaten,
  genangan_id,
  luas_intersect_m2,
  CAST(
    jumlah_penduduk * (luas_intersect_m2 / NULLIF(luas_kel_m2, 0))
    AS INT
  ) AS estimasi_terdampak
FROM intersected
WHERE luas_intersect_m2 > 0;
