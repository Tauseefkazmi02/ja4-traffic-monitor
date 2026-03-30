from scapy.all import sniff, TCP, IP, load_layer
import logging

# Load TLS layer
load_layer("tls")
from scapy.layers.tls.all import TLSClientHello

from ja4_engine import generate_ja4
from database import insert_log
from threat_detection import detect_threat
import pandas as pd

# 🔥 NEW IMPORTS (UI)
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# Disable scapy warnings
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# 🔥 ASCII BANNER
print(Fore.GREEN + Style.BRIGHT + """
╔══════════════════════════════════════╗
║     🔐 JA4 TRAFFIC MONITOR v1.0      ║
║   Real-Time Encrypted Analysis 🔥    ║
╚══════════════════════════════════════╝
""")

# Load fingerprint database
fingerprint_db = pd.read_csv("fingerprint_db.csv")


def identify_app(ja4):
    match = fingerprint_db[fingerprint_db["ja4"] == ja4]
    if not match.empty:
        return match.iloc[0]["app"]
    return "Unknown"


def packet_callback(packet):

    if not packet.haslayer(IP) or not packet.haslayer(TCP):
        return

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst

    # 🌐 SYN Packet
    if packet[TCP].flags == "S":
        now = datetime.now().strftime("%H:%M:%S")
        print(Fore.BLUE + f"[{now}] [SYN] New Connection: {src_ip} → {dst_ip}")
        return

    # 🔐 TLS HANDSHAKE DETECTION
    if packet.haslayer(TLSClientHello):
        try:
            tls_layer = packet[TLSClientHello]

            # Extract SNI
            try:
                sni = tls_layer.getlayer('TLS_Ext_ServerName').servernames[0].hostname.decode()
            except:
                sni = "No SNI"

            # Generate JA4
            raw_payload = bytes(packet[TCP].payload)
            ja4 = generate_ja4(packet, raw_payload)

            # Identify app
            app = identify_app(ja4)

            # 🔥 ADVANCED DETECTION (ADDED ONLY)
            if app == "Unknown":

                # SNI detection
                if sni != "No SNI":
                    sni_lower = sni.lower()

                    if "google" in sni_lower:
                        app = "Google Services"
                    elif "youtube" in sni_lower:
                        app = "YouTube"
                    elif "whatsapp" in sni_lower:
                        app = "WhatsApp"
                    elif "facebook" in sni_lower or "fbcdn" in sni_lower:
                        app = "Facebook"
                    elif "instagram" in sni_lower:
                        app = "Instagram"
                    elif "amazon" in sni_lower or "aws" in sni_lower:
                        app = "Amazon AWS"
                    elif "microsoft" in sni_lower or "teams" in sni_lower:
                        app = "Microsoft / Teams"

                # IP detection
                if app == "Unknown":
                    if dst_ip.startswith("142.") or dst_ip.startswith("172.217"):
                        app = "Google Services"
                    elif dst_ip.startswith("34."):
                        app = "Google Cloud"
                    elif dst_ip.startswith("151.101"):
                        app = "Fastly CDN"
                    elif dst_ip.startswith("172.64") or dst_ip.startswith("104."):
                        app = "Cloudflare"
                    elif dst_ip.startswith("157.240") or dst_ip.startswith("31.13"):
                        app = "Meta (WhatsApp/Facebook)"
                    elif dst_ip.startswith("52.") or dst_ip.startswith("3."):
                        app = "Amazon AWS"
                    elif dst_ip.startswith("20."):
                        app = "Microsoft Azure"
                    else:
                        app = "Unknown (Encrypted Traffic)"

            # ⏱️ TIME
            now = datetime.now().strftime("%H:%M:%S")

            # 🔥 BEAUTIFUL OUTPUT
            print(Fore.CYAN + f"\n[{now}] 🔐 TLS CONNECTION")
            print(Fore.YELLOW + f"  ➤ Source      : {src_ip}")
            print(Fore.YELLOW + f"  ➤ Destination : {dst_ip}")
            print(Fore.BLUE + f"  ➤ SNI         : {sni}")
            print(Fore.GREEN + Style.BRIGHT + f"  ➤ Application : {app}")
            print(Fore.MAGENTA + f"  ➤ JA4 Finger  : {ja4}")
            print(Style.DIM + "  " + "─" * 50)

            # 🚨 Threat Detection
            alerts = detect_threat(src_ip, ja4, app)

            for alert in alerts:
                print(Fore.RED + Style.BRIGHT + f"  🚨 ALERT: {alert}")

            # Save log
            insert_log(src_ip, dst_ip, ja4, app)

        except Exception as e:
            print(Fore.RED + f"[ERROR] TLS Processing: {e}")


# Start sniffing
sniff(prn=packet_callback, store=False)
