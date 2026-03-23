import streamlit as st
import pandas as pd
from scanner import scan_network
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "192.168.1.1"
    finally:
        s.close()
    return ip

def get_device_icon(hostname, manufacturer):
    hostname = hostname.lower()
    manufacturer = manufacturer.lower()
    if any(x in hostname for x in ["router", "gateway", "dlink", "tplink", "asus"]):
        return "🌐 Router"
    elif any(x in manufacturer for x in ["apple", "samsung", "xiaomi", "oppo", "vivo"]):
        return "📱 Phone"
    elif any(x in hostname for x in ["laptop", "pc", "desktop", "computer"]):
        return "💻 Laptop/PC"
    elif any(x in manufacturer for x in ["dell", "hp", "lenovo", "asus", "acer"]):
        return "💻 Laptop/PC"
    else:
        return "📟 Unknown Device"

st.set_page_config(page_title="Device Finder", page_icon="🔍", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 2rem; }
    .stButton>button {
        background-color: #00c853;
        color: white;
        font-size: 18px;
        padding: 10px 30px;
        border-radius: 10px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00e676;
        color: black;
    }
    .device-card {
        background-color: #1e1e2e;
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 12px;
        border-left: 5px solid #00c853;
    }
    .tip-box {
        background-color: #1a237e;
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 10px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Device Finder")
st.markdown("##### Find all devices connected to your WiFi network easily!")
st.markdown("---")

local_ip = get_local_ip()
ip_parts = local_ip.rsplit('.', 1)[0]
ip_range = f"{ip_parts}.0/24"

with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")
    st.markdown("### 📌 Your Network Info")
    st.success(f"Your IP Address: **{local_ip}**")
    st.info(f"Scan Range: **{ip_range}**")
    st.markdown("---")
    st.markdown("### 🛠 Custom Scan Range")
    custom_range = st.text_input("Enter IP Range", placeholder="e.g. 192.168.1.0/24")
    st.markdown("---")
    st.markdown("""
    <div class='tip-box'>
    💡 <b>What is an IP Address?</b><br>
    It's like a home address for your device on the network.
    </div>
    <div class='tip-box'>
    💡 <b>What is a MAC Address?</b><br>
    It's a unique ID given to every device by its manufacturer.
    </div>
    <div class='tip-box'>
    💡 <b>What is a Hostname?</b><br>
    It's the name your device uses on the network.
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 📡 How to Use")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### 1️⃣ Connect to WiFi\nMake sure your PC is connected to your home or office WiFi.")
with col2:
    st.markdown("#### 2️⃣ Click Scan\nPress the green **Start Scan** button below.")
with col3:
    st.markdown("#### 3️⃣ See Devices\nAll connected devices will appear with details.")

st.markdown("---")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    scan_button = st.button("🚀 Start Scanning My Network")

if scan_button:
    target = custom_range if custom_range else ip_range
    with st.spinner("🔍 Scanning your network... This may take 10-30 seconds..."):
        devices = scan_network(target)

    if devices:
        st.balloons()
        st.success(f"✅ Great! Found **{len(devices)} device(s)** on your network!")
        st.markdown("---")
        st.markdown("### 📋 Devices Found")

        for i, device in enumerate(devices):
            icon = get_device_icon(device['Hostname'], device['Manufacturer'])
            st.markdown(f"""
            <div class='device-card'>
                <h4>{icon} &nbsp; Device {i+1}</h4>
                <table style='width:100%; font-size:15px;'>
                    <tr>
                        <td>🌐 <b>IP Address</b></td>
                        <td>{device['IP Address']}</td>
                        <td>🔌 <b>MAC Address</b></td>
                        <td>{device['MAC Address']}</td>
                    </tr>
                    <tr>
                        <td>🏷️ <b>Hostname</b></td>
                        <td>{device['Hostname']}</td>
                        <td>🏭 <b>Manufacturer</b></td>
                        <td>{device['Manufacturer']}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📊 Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("🖥️ Total Devices", len(devices))
        col2.metric("🌐 Network Range", target)
        col3.metric("📍 Your IP", local_ip)

        st.markdown("---")
        df = pd.DataFrame(devices)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="network_devices.csv",
            mime="text/csv"
        )

    else:
        st.error("⚠️ No devices found!")
        st.markdown("""
        ### 🛠️ Try these fixes:
        - ✅ Make sure you are connected to WiFi
        - ✅ Run VS Code as **Administrator**
        - ✅ Make sure Npcap is installed
        - ✅ Try entering the IP range manually in the sidebar
        """)

st.markdown("---")
st.caption("🔍 Device Finder Local Network | Built with Python + Streamlit | For Educational Purposes Only")