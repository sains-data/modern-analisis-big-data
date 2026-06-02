"""Latihan 5B: row key reverse timestamp di HBase."""
import time

HBASE_HOST = "localhost"
HBASE_PORT = 9090


def reverse_ts(ts_ms=None) -> str:
    ts = ts_ms if ts_ms is not None else int(time.time() * 1000)
    return str(9999999999999 - ts)


def main() -> None:
    try:
        import happybase
    except ImportError as exc:
        raise SystemExit("Jalankan: bash scripts/install_happybase.sh") from exc

    conn = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
    conn.open()

    if b"event_log" in conn.tables():
        conn.delete_table("event_log", disable=True)

    conn.create_table("event_log", {"cf": {}})
    tabel = conn.table("event_log")

    events = [("EVT-001", "login"), ("EVT-002", "purchase"), ("EVT-003", "logout")]
    for eid, etype in events:
        time.sleep(0.01)
        rk = f"{reverse_ts()}#{eid}".encode()
        tabel.put(rk, {b"cf:type": etype.encode()})

    print("[Scan event_log — terbaru pertama]")
    for key, data in tabel.scan():
        print(key.decode(), data[b"cf:type"].decode())

    conn.close()


if __name__ == "__main__":
    main()
