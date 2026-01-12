#!/usr/bin/env python3
"""Script to fix Grafana dashboard datasource configurations."""
import json
import os

DASHBOARDS_DIR = r"d:\hy-home.docker\infra\observability\grafana\dashboards"


def add_datasource_variable(dashboard: dict) -> dict:
    """Add datasource template variable if not present."""
    ds_var = {
        "current": {"text": "Prometheus", "value": "Prometheus"},
        "includeAll": False,
        "label": "Data Source",
        "name": "datasource",
        "options": [],
        "query": "prometheus",
        "refresh": 1,
        "regex": "",
        "type": "datasource"
    }
    
    if "templating" not in dashboard:
        dashboard["templating"] = {"list": []}
    if "list" not in dashboard["templating"]:
        dashboard["templating"]["list"] = []
    
    # Check if datasource variable already exists
    has_ds_var = any(
        v.get("name") in ("datasource", "DS_PROMETHEUS", "Datasource") 
        for v in dashboard["templating"]["list"]
    )
    if not has_ds_var:
        dashboard["templating"]["list"].insert(0, ds_var)
    
    return dashboard


def fix_datasource_refs(json_str: str) -> str:
    """Replace hardcoded Prometheus UIDs with variable reference."""
    replacements = [
        ('"uid": "Prometheus"', '"uid": "${datasource}"'),
        ('"datasource": "Prometheus"', '"datasource": "${datasource}"'),
    ]
    for old, new in replacements:
        json_str = json_str.replace(old, new)
    return json_str


def fix_cadvisor_dashboard():
    """Fix cAdvisor exporter dashboard."""
    file_path = os.path.join(DASHBOARDS_DIR, "Cadvisor exporter-1763791276601.json")
    
    with open(file_path, "r", encoding="utf-8") as f:
        dashboard = json.load(f)
    
    dashboard = add_datasource_variable(dashboard)
    json_str = json.dumps(dashboard, indent=2, ensure_ascii=False)
    json_str = fix_datasource_refs(json_str)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_str)
    
    print(f"✅ Fixed: Cadvisor exporter dashboard")


def fix_traefik_dashboard():
    """Fix Traefik Official dashboard."""
    file_path = os.path.join(DASHBOARDS_DIR, "Traefik Official Standalone Dashboard-1764330803133.json")
    
    with open(file_path, "r", encoding="utf-8") as f:
        dashboard = json.load(f)
    
    dashboard = add_datasource_variable(dashboard)
    # Make it editable
    dashboard["editable"] = True
    
    json_str = json.dumps(dashboard, indent=2, ensure_ascii=False)
    json_str = fix_datasource_refs(json_str)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_str)
    
    print(f"✅ Fixed: Traefik Official dashboard")


def fix_keycloak_dashboard():
    """Fix Keycloak dashboard for Docker Compose compatibility."""
    file_path = os.path.join(DASHBOARDS_DIR, "Keycloak Metrics Dashboard-1764330788865.json")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace kubernetes-specific labels with generic ones
    content = content.replace('kubernetes_pod_name="$instance"', 'instance=~"$instance"')
    content = content.replace('kubernetes_pod_name=\\"$instance\\"', 'instance=~\\"$instance\\"')
    
    # Update the instance variable query to use job label
    dashboard = json.loads(content)
    
    for var in dashboard.get("templating", {}).get("list", []):
        if var.get("name") == "instance":
            # Update to use a more generic query
            var["definition"] = 'label_values(jvm_memory_bytes_used{job=~".*keycloak.*"}, instance)'
            var["query"] = {
                "query": 'label_values(jvm_memory_bytes_used{job=~".*keycloak.*"}, instance)',
                "refId": "StandardVariableQuery"
            }
            var["label"] = "Instance"
    
    json_str = json.dumps(dashboard, indent=2, ensure_ascii=False)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_str)
    
    print(f"✅ Fixed: Keycloak dashboard (Docker Compose compatible)")


def check_redis_dashboards():
    """Check Redis dashboards for deduplication."""
    redis_files = [f for f in os.listdir(DASHBOARDS_DIR) if "redis" in f.lower()]
    print(f"\n📋 Redis dashboards found: {len(redis_files)}")
    for f in redis_files:
        file_path = os.path.join(DASHBOARDS_DIR, f)
        with open(file_path, "r", encoding="utf-8") as fp:
            dashboard = json.load(fp)
        title = dashboard.get("title", "Unknown")
        panels = len(dashboard.get("panels", []))
        print(f"   - {f}")
        print(f"     Title: {title}, Panels: {panels}")


if __name__ == "__main__":
    print("=" * 60)
    print("Grafana Dashboard Fix Script")
    print("=" * 60)
    
    fix_cadvisor_dashboard()
    fix_traefik_dashboard()
    fix_keycloak_dashboard()
    check_redis_dashboards()
    
    print("\n✅ All fixes applied!")
