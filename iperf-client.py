import math
import subprocess
import json
import sys


def client(server_ip):
    return subprocess.run(["iperf3", "-c", server_ip, "--json"], capture_output=True, text=True)


def parser(iperf_result):
    json_result = json.loads(iperf_result.stdout)

    if iperf_result.returncode == 0:
        return list(map(lambda interval: parse_interval(interval), json_result["intervals"]))
    else:
        return parse_error(json_result)


def parse_interval(interval):
    interval_sum = interval["sum"]
    return {
        "Interval": f"{interval_sum['start']:.{1}f}-{interval_sum['end']:.{1}f}",
        "Transfer": float(f"{interval_sum['bytes'] / math.pow(10, 6):.{2}f}"),
        "Transfer_unit": "MBytes",
        "Bandwidth": float(f"{interval_sum['bits_per_second'] / math.pow(10, 9):.{2}f}"),
        "Bandwidth_unit": "Gbits/sec"
    }


def parse_error(error):
    return error["error"]


if __name__ == '__main__':
    for value in parser(client(sys.argv[1])):
        if value["Transfer"] > 200 and value["Bandwidth"] > 1.50:
            print(value)