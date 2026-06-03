-- routing_evakuasi.sql — KNN join shelter (Sedona, referensi Bab 17)
-- Constraint jalan: ST_Crosses(jalan, genangan) = false (produksi)

WITH terdampak AS (
  SELECT
    kode_kel,
    nama_kel,
    estimasi_terdampak,
    ST_Centroid(geometry) AS geom_centroid
  FROM gold.populasi_terdampak p
  JOIN silver.kelurahan_sumsel k USING (kode_kel)
),
shelter AS (
  SELECT shelter_id, nama_shelter, kapasitas, geometry AS geom_shelter
  FROM gold.shelter_kapasitas
)
SELECT
  t.kode_kel,
  t.nama_kel,
  t.estimasi_terdampak,
  s.shelter_id,
  s.nama_shelter,
  s.kapasitas,
  ST_Distance(
    ST_Transform(t.geom_centroid, 'EPSG:32748'),
    ST_Transform(s.geom_shelter, 'EPSG:32748')
  ) AS jarak_m
FROM terdampak t
LATERAL (
  SELECT *
  FROM shelter s
  ORDER BY ST_Distance(
    ST_Transform(t.geom_centroid, 'EPSG:32748'),
    ST_Transform(s.geom_shelter, 'EPSG:32748')
  )
  LIMIT 1
) s;
