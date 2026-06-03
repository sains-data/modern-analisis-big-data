-- akuntabilitas_konsesi.sql — referensi Sedona (Bab 17)
SELECT
  k.nama_perusahaan,
  k.no_izin,
  k.jenis_konsesi,
  COUNT(h.hotspot_id) AS n_hotspot,
  SUM(h.frp) AS total_frp_mw,
  COUNT(DISTINCT h.acq_date) AS n_hari_aktif
FROM silver.konsesi_riau k
JOIN silver.hotspot_firms_verified h
  ON ST_Contains(k.geometry, ST_Point(h.longitude, h.latitude))
WHERE h.confidence IN ('nominal', 'high')
GROUP BY k.nama_perusahaan, k.no_izin, k.jenis_konsesi
ORDER BY n_hotspot DESC;
