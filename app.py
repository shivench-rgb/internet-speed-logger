import streamlit as st
import pandas as pd
import speedtest
import os
from datetime import datetime

st.set_page_config(
    page_title="Internet Speed Logger",
    page_icon="🌐",
    layout="wide"
)

st.title("Internet Speed Logger")
st.caption("Monitor, record and analyze your internet performance.")

# -----------------------------
# Speed Test Function
# -----------------------------
def run_speed_test():

    st_obj = speedtest.Speedtest()
    st_obj.get_best_server()

    download = st_obj.download() / 1_000_000
    upload = st_obj.upload() / 1_000_000
    ping = st_obj.results.ping

    return download, upload, ping


# -----------------------------
# Internet Status
# -----------------------------
def get_status(download, ping):

    if download >= 50 and ping <= 50:
        return "Excellent"

    elif download >= 25 and ping <= 100:
        return "Good"

    elif download >= 10:
        return "Average"

    else:
        return "Slow"


# -----------------------------
# Run Test
# -----------------------------
if st.button("Run Speed Test", type="primary"):

    with st.spinner("Testing your internet speed..."):

        try:

            download, upload, ping = run_speed_test()

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            new_data = pd.DataFrame({
                "Timestamp": [timestamp],
                "Download_Mbps": [round(download, 2)],
                "Upload_Mbps": [round(upload, 2)],
                "Ping_ms": [round(ping, 2)]
            })

            file_exists = os.path.exists(
                "speed_history.csv"
            )

            new_data.to_csv(
                "speed_history.csv",
                mode="a",
                header=not file_exists,
                index=False
            )

            st.success("Speed test completed!")

            # Results
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Download",
                    f"{download:.2f} Mbps"
                )

            with col2:
                st.metric(
                    "Upload",
                    f"{upload:.2f} Mbps"
                )

            with col3:
                st.metric(
                    "Ping",
                    f"{ping:.2f} ms"
                )

            with col4:
                st.metric(
                    "Status",
                    get_status(download, ping)
                )

        except Exception as e:

            st.error(
                f"Speed test failed: {e}"
            )


# -----------------------------
# History
# -----------------------------
st.divider()

st.header("Speed History")

if os.path.exists("speed_history.csv"):

    df = pd.read_csv("speed_history.csv")

    # Statistics
    avg_download = df["Download_Mbps"].mean()
    avg_upload = df["Upload_Mbps"].mean()
    avg_ping = df["Ping_ms"].mean()

    fastest_download = df["Download_Mbps"].max()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average Download",
            f"{avg_download:.2f} Mbps"
        )

    with col2:
        st.metric(
            "Average Upload",
            f"{avg_upload:.2f} Mbps"
        )

    with col3:
        st.metric(
            "Average Ping",
            f"{avg_ping:.2f} ms"
        )

    with col4:
        st.metric(
            "Fastest Download",
            f"{fastest_download:.2f} Mbps"
        )

    st.subheader("Download Speed")

    st.line_chart(
        df.set_index("Timestamp")[
            "Download_Mbps"
        ]
    )

    st.subheader("Upload Speed")

    st.line_chart(
        df.set_index("Timestamp")[
            "Upload_Mbps"
        ]
    )

    st.subheader("Ping")

    st.line_chart(
        df.set_index("Timestamp")[
            "Ping_ms"
        ]
    )

    st.subheader("Test Records")

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "No speed test records yet. "
        "Run your first test above."
    )