import urllib.request
import base64
import json
import time
import socket
import os
from urllib.parse import urlparse, unquote

# 配置常量
SUB_URL = "https://raw.githubusercontent.com/Leon406/SubCrawler/refs/heads/main/sub/share/v2"
OUTPUT_FILE = "ustop30.txt"
TEST_TIMEOUT = 1.5  # 每个节点单次连接超时时间（秒）

def fetch_and_decode():
    print(f"正在从源地址获取节点: {SUB_URL}")
    try:
        req = urllib.request.Request(SUB_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8').strip()
        
        # 补齐 Base64 填充位
        padding = '=' * (4 - len(content) % 4)
        decoded = base64.b64decode(content + padding).decode('utf-8', errors='ignore')
        return decoded.splitlines()
    except Exception as e:
        print(f"获取订阅源失败: {e}")
        return []

def filter_us_vless_nodes(lines):
    us_nodes = []
    print("开始筛选【VLESS 协议】的美国节点...")
    for line in lines:
        line = line.strip()
        # 严格筛选 vless 协议
        if not line.startswith("vless://"):
            continue
        try:
            # VLESS 格式通常为: vless://uuid@server:port?query#remarks
            # 优先提取最后的备注部分（#后面）
            ps = ""
            if "#" in line:
                ps = unquote(line.split("#")[-1])
            
            ps_upper = ps.upper()
            line_upper = line.upper()
            
            # 匹配美国关键字或国旗
            if any(k in ps_upper for k in ["美国", "US", "UNITED STATES", "🇺🇸"]) or "美国" in line_upper:
                # 解析出服务器地址和端口用于测速
                # 移除 vless:// 前缀
                url_part = line[8:]
                # 隔离出用户认证信息之后的部分
                if "@" in url_part:
                    server_part = url_part.split("@")[-1]
                    # 隔离出查询参数或备注前的主机端口部分
                    host_port = server_part.split("?")[0].split("#")[0]
                    
                    if ":" in host_port:
                        add = host_port.split(":")[0]
                        port = host_port.split(":")[1]
                    else:
                        add = host_port
                        port = "443"  # 默认 VLESS 端口
                        
                    us_nodes.append({
                        "raw": line,
                        "add": add,
                        "port": port,
                        "ps": ps if ps else f"VLESS-{add}"
                    })
        except Exception as e:
            continue
            
    print(f"共筛选出 {len(us_nodes)} 个美国 VLESS 节点。")
    return us_nodes

def tcp_ping(add, port):
    """通过核心TCP三次握手时延模拟 urltest 核心逻辑"""
    try:
        port = int(port)
        start_time = time.time()
        sock = socket.create_connection((add, port), timeout=TEST_TIMEOUT)
        latency = (time.time() - start_time) * 1000  # 毫秒
        sock.close()
        return latency
    except Exception:
        return None

def test_nodes(us_nodes):
    print("开始对 VLESS 节点进行可用性与延迟测速...")
    valid_nodes = []
    for idx, node in enumerate(us_nodes):
        add, port, ps = node["add"], node["port"], node["ps"]
        if not add or not port:
            continue
        
        latency = tcp_ping(add, port)
        if latency is not None:
            print(f"[{idx+1}] 节点: {ps} | 延迟: {latency:.2f}ms")
            valid_nodes.append((latency, node["raw"]))
        else:
            continue
            
    # 按延迟升序排序（最快的排在最前面）
    valid_nodes.sort(key=lambda x: x[0])
    return valid_nodes

def main():
    lines = fetch_and_decode()
    if not lines:
        return
        
    us_nodes = filter_us_vless_nodes(lines)
    if not us_nodes:
        print("未找到任何美国 VLESS 节点，终止操作。")
        return
        
    fastest_nodes = test_nodes(us_nodes)
    
    # 提取前 30 个最快节点
    top_30 = fastest_nodes[:30]
    print(f"成功筛选出最快的 {len(top_30)} 个可用美国 VLESS 节点。")
    
    if not top_30:
        print("无可用节点，不执行写入。")
        return

    # 拼接所有 VLESS 节点并实施整体 Base64 加密，使其可直接订阅
    merged_nodes = "\n".join([raw_line for latency, raw_line in top_30])
    b64_encoded_sub = base64.b64encode(merged_nodes.encode('utf-8')).decode('utf-8')
    
    # 写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(b64_encoded_sub)
        
    print(f"结果已成功按【标准 VLESS 订阅格式】写入 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
