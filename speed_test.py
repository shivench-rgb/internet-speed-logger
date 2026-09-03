import speedtest
from datetime import datetime
import csv
import os


def run_speed_test():
    print("Starting internet speed test...")
    print("Please wait...\n")

    st = speedtest.Speedtest()

    st.get_best_server()

    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000
    ping = st.results.ping

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Download Speed : {download_speed:.2f} Mbps")
    print(f"Upload Speed   : {upload_speed:.2f} Mbps")
    print(f"Ping           : {ping:.2f} ms")

    save_result(timestamp, download_speed, upload_speed, ping)


def save_result(timestamp, download, upload, ping):
    file_exists = os.path.isfile("speed_history.csv")

    with open("speed_history.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "Download_Mbps",
                "Upload_Mbps",
                "Ping_ms"
            ])

        writer.writerow([
            timestamp,
            round(download, 2),
            round(upload, 2),
            round(ping, 2)
        ])

    print("\nResult saved to speed_history.csv")


if __name__ == "__main__":
    run_speed_test()