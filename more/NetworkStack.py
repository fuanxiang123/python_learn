class NetworkStack:
    def __init__(self):
        self.sockets = {}

    def send_packet(self, src_addr, dst_addr, data):
        print(f"Sending packet from {src_addr} to {dst_addr}: {data}")

    def receive_packet(self, dst_addr):
        return b"Hello, World!"  # 模拟接收数据