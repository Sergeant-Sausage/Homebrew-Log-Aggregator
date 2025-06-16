import json
import os

def normalize_entra_logs(input_file, output_file):
    with open(input_file, 'r') as f:
        raw_logs = json.load(f)

    normalized_logs = []
    for log in raw_logs:
        norm = {
            "timestamp": log.get("createdDateTime"),
            "username": log.get("userDisplayName"),
            "user_principal": log.get("userPrincipalName"),
            "ip_address": log.get("ipAddress"),
            "location_city": log.get("location", {}).get("city"),
            "location_state": log.get("location", {}).get("state"),
            "app_name": log.get("appDisplayName"),
            "resource_name": log.get("resourceDisplayName"),
            "client_app": log.get("clientAppUsed"),
            "device_name": log.get("deviceDetail", {}).get("displayName"),
            "os": log.get("deviceDetail", {}).get("operatingSystem"),
            "browser": log.get("deviceDetail", {}).get("browser"),
            "status_code": log.get("status", {}).get("errorCode"),
            "status_reason": log.get("status", {}).get("failureReason"),
            "mfa_info": log.get("status", {}).get("additionalDetails"),
            "conditional_access": log.get("conditionalAccessStatus"),
        }
        normalized_logs.append(norm)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(normalized_logs, f, indent=2)

    print(f"✅ Normalized log written to: {output_file}")


if __name__ == "__main__":
    input_path = os.path.join("data", "entra_signins.json")
    output_path = os.path.join("data", "normalized_entra.json")
    normalize_entra_logs(input_path, output_path)

