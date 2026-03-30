import hashlib
from scapy.layers.tls.all import TLSClientHello

def get_tls_version(packet):
    try:
        version = packet[TLSClientHello].version

        if version == 0x0304:
            return "13"   # TLS 1.3
        elif version == 0x0303:
            return "12"   # TLS 1.2
        elif version == 0x0302:
            return "11"
        elif version == 0x0301:
            return "10"
        else:
            return "00"
    except:
        return "00"


def generate_ja4(packet, payload):
    try:
        # ✅ Correct TLS version
        tls_ver = get_tls_version(packet)

        # Basic fingerprint data (simplified JA4)
        cipher_part = payload[10:40]
        ext_part = payload[40:100]

        raw = cipher_part + ext_part

        hash_val = hashlib.sha256(raw).hexdigest()[:16]

        return f"t{tls_ver}_{hash_val}"

    except:
        return "unknown"
