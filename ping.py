import subprocess, platform, os, socket

def ping_device(ip):
    """Pings an IP, resolves its hostname, and prints status."""
    # Resolve hostname
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.timeout, Exception): # Catch common DNS errors
        hostname = "N/A"

    # Ping command based on OS
    cmd = ["ping", "-n" if platform.system().lower() == "windows" else "-c", "1", ip]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        status = "UP" if res.returncode == 0 and ("Reply from" in res.stdout or "bytes from" in res.stdout) else "DOWN"
        print(f"Device {ip} ({hostname}): {status}")
    except subprocess.TimeoutExpired:
        print(f"Device {ip} ({hostname}): DOWN (Timeout)")
    except Exception as e:
        print(f"Device {ip} ({hostname}): Error - {e}")

if __name__ == "__main__":
    file_path = "devices.txt"
    if not os.path.exists(file_path):
        print(f"Error: '{file_path}' not found.")
        exit()

    try:
        # Read IPs from file, stripping whitespace and filtering empty lines
        ips = [line.strip() for line in open(file_path) if line.strip()]
        if not ips:
            print(f"No IP addresses found in '{file_path}'.")
            exit()

        print("Starting ping and DNS checks...\n")
        for ip in ips:
            ping_device(ip)
        print("\nPing and DNS checks complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
