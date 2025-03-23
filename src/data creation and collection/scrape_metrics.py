import requests
import pandas as pd

start_time = "2025-03-04T13:44:00Z"
end_time = "2025-03-19T00:52:00Z"

queries = {
    "cpu_usage": 'rate(container_cpu_usage_seconds_total{namespace="default"}[5m])',
    "memory_usage": 'container_memory_usage_bytes{namespace="default"}',
    "pod_status_running": 'kube_pod_status_phase{namespace="default", phase="Running"}',
    "network_rx": 'rate(container_network_receive_bytes_total{namespace="default"}[5m])'
}

dataframes = {}
for metric, query in queries.items():
    url = f"http://localhost:9090/api/v1/query_range?query={query}&start={start_time}&end={end_time}&step=60s"
    response = requests.get(url).json()
    if response["status"] == "success":
        if response["data"]["result"]:
            values = response["data"]["result"][0]["values"]
            df = pd.DataFrame(values, columns=["timestamp", metric])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            dataframes[metric] = df
            print(f"Got data for {metric}: {len(values)} points")
        else:
            print(f"No results for {metric}")
    else:
        print(f"Query failed for {metric}: {response.get('error', 'Unknown error')}")

if dataframes:
    df = next(iter(dataframes.values()))
    for metric, df_metric in dataframes.items():
        if df_metric is not df:
            df = df.merge(df_metric[["timestamp", metric]], on="timestamp", how="outer")
    df.to_csv("azure_k8s_metrics_1.csv", index=False)
    print("Data exported to azure_k8s_metrics_1.csv")
else:
    print("No data to export")
