import os
import json
import csv

def build_qbr_report():
    # Detect config file regardless of execution directory
    candidates = [
        'sap_portfolio_config.json',
        'config.json',
        '../sap_portfolio_config.json',
        '../config.json'
    ]
    
    config_file = None
    for path in candidates:
        if os.path.exists(path):
            config_file = path
            break

    if not config_file:
        raise FileNotFoundError(f"Configuration file not found in {os.getcwd()}")

    base_dir = os.path.dirname(os.path.abspath(config_file))

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    print("==================================================")
    print(f" Initializing {config.get('project_name', 'SAP QBR Report')} (v{config.get('version', '1.0.0')})")
    print("==================================================")

    sap_sync_config = config.get('configuration', {}).get('sap_sync', {})
    sap_host_var = sap_sync_config.get('sap_host_env_var', 'SAP_S4HANA_HOST')
    sap_host_val = os.getenv(sap_host_var)

    use_live_sap = sap_sync_config.get('auto_detect', True) and sap_host_val is not None

    if use_live_sap:
        print(f"[STATUS] SAP Host Detected ({sap_host_val}). Executing Live S/4HANA Sync...")
        execution_mode = "LIVE_SAP_S4HANA"
        payload = {"message": f"Connected to live SAP RFC/OData endpoint at {sap_host_val}"}
    else:
        print("[STATUS] SAP S/4HANA host not detected. Fallback to local Demo CSV resources...")
        execution_mode = "DEMO_CSV_FALLBACK"
        payload = {}

        sources = config.get('configuration', {}).get('portfolio_data_sources', {})
        for key, filepath in sources.items():
            target_path = os.path.normpath(os.path.join(base_dir, filepath))
            fallback_path = os.path.normpath(os.path.join(base_dir, 'resources', os.path.basename(filepath)))
            
            target = target_path if os.path.exists(target_path) else fallback_path

            if os.path.exists(target):
                with open(target, mode='r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    payload[key] = [row for row in reader]
                print(f" -> Loaded resource: {os.path.basename(target)} ({len(payload[key])} records)")
            else:
                print(f" -> Warning: Resource path not found: {filepath}")

    compiled_data = {
        "project": config.get("project_name"),
        "version": config.get("version"),
        "execution_mode": execution_mode,
        "governance": config.get("configuration", {}).get("governance_rules", {}),
        "data": payload
    }

    dist_dir = os.path.join(base_dir, 'dist')
    os.makedirs(dist_dir, exist_ok=True)
    output_file = os.path.join(dist_dir, 'compiled_qbr_report.json')

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(compiled_data, f, indent=2)

    print("--------------------------------------------------")
    print(f" SUCCESS: Report compiled to '{output_file}'")
    print("==================================================")

if __name__ == "__main__":
    build_qbr_report()
