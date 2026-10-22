
import pandas as pd
from pathlib import Path


def load_and_prepare_data():
    project_root = Path(__file__).resolve().parents[1]
    file_path = project_root / "Data" / "Deployement+Devices.xlsx"

    # Load the two sheets
    deployments = pd.read_excel(
        file_path,
        sheet_name="deployments"
    )

    devices = pd.read_excel(
        file_path,
        sheet_name="Devices"
    )

    return deployments, devices


if __name__ == "__main__":

    # Load the data
    deployments, devices = load_and_prepare_data()

    # Inspect the data
    print("DEPLOYMENTS")
    print("Shape:", deployments.shape)
    deployments.info()
    print("\nMissing values:")
    print(deployments.isna().sum())

    print("\nDEVICES")
    print("Shape:", devices.shape)
    devices.info()
    print("\nMissing values:")
    print(devices.isna().sum())

    print("Deployment Status Count:")
    print(deployments["status"].value_counts(dropna=False))

    unsuccessful = deployments[
        (deployments["status"] == "Failed") |
        (deployments["status"] == "Rolled Back")
    ]

    print(unsuccessful)

    unsuccessful_count = len(unsuccessful)
    print(unsuccessful_count)

    unsuccessful_rate = (unsuccessful_count / len(deployments)) * 100
    print(unsuccessful_rate, "%")

    earliest_date = deployments["deployment_date"].min()
    print(earliest_date)

    latest_date = deployments["deployment_date"].max()
    print(latest_date)

    deployments["deployment_month"] = (
        deployments["deployment_date"].dt.to_period("M")
    )
    print(deployments["deployment_month"])

    # Display deployment dates and months
    print(
        deployments[
            ["deployment_date", "deployment_month"]
        ].head()
    )

    # Count deployments per month
    deployment_count = (
        deployments.groupby("deployment_month").size()
    )
    print(deployment_count)

    # Add month information to unsuccessful deployments
    unsuccessful["deployment_month"] = (
        unsuccessful["deployment_date"].dt.to_period("M")
    )

    unsuccessful_count_per_month = (
        unsuccessful.groupby("deployment_month")
        .size()
        .sort_index()
    )
    print(unsuccessful_count_per_month)

    deployment_attempt_per_month = (
        deployments.groupby("deployment_month")
        .size()
        .sort_index()
    )
    print(deployment_attempt_per_month)

    monthly_unsuccessful_rate = (
        unsuccessful_count_per_month / deployment_attempt_per_month
    ) * 100
    print(monthly_unsuccessful_rate.round(2))

    print(unsuccessful_count_per_month.sum())
    print(deployment_attempt_per_month.sum())

    # Annual analysis
    deployments["deployment_year"] = (
        deployments["deployment_date"].dt.year
    )
    print(deployments["deployment_year"].head())

    deployment_attempt_per_year = (
        deployments.groupby("deployment_year").size().sort_index()
    )
    print(deployment_attempt_per_year)

    unsuccessful["deployment_year"] = (
        unsuccessful["deployment_date"].dt.year
    )
    print(unsuccessful["deployment_year"].head())

    unsuccessful_count_per_year = (
        unsuccessful.groupby("deployment_year").size().sort_index()
    )
    print(unsuccessful_count_per_year)

    annual_unsuccessful_rate = (
        unsuccessful_count_per_year / deployment_attempt_per_year
    ) * 100
    print(annual_unsuccessful_rate.round(2))

    print(unsuccessful_count_per_year.sum())
    print(deployment_attempt_per_year.sum())

    # Inspect device identifiers
    print(deployments["device_id"].head().sort_values())
    print(devices["device_id"].head())

    # Merge deployments and device information
    merged_deployment_data = deployments.merge(
        devices,
        on="device_id",
        how="left"
    )

    print(merged_deployment_data)
    print(merged_deployment_data.isna().sum())

    print(deployments["deployment_id"].duplicated().sum())

    # Validate overlapping columns
    print(
        (
            merged_deployment_data["device_type_x"] !=
            merged_deployment_data["device_type_y"]
        ).sum()
    )

    print(
        (
            merged_deployment_data["site_id_x"] !=
            merged_deployment_data["site_id_y"]
        ).sum()
    )

    print(
        (
            merged_deployment_data["site_name_x"] !=
            merged_deployment_data["site_name_y"]
        ).sum()
    )

    # Remove redundant columns and standardize names
    merged_deployment_data = merged_deployment_data.drop(
        columns=["site_id_y", "site_name_y", "device_type_y"]
    )

    merged_deployment_data = merged_deployment_data.rename(
        columns={
            "site_id_x": "site_id",
            "site_name_x": "site_name",
            "device_type_x": "device_type"
        }
    )

    print(merged_deployment_data.shape)
    print(merged_deployment_data.columns)

    # Unsuccessful deployments by device type
    unsuccessful_by_type = unsuccessful.groupby("device_type").size()
    print(unsuccessful_by_type)

    total_by_type = merged_deployment_data.groupby("device_type").size()
    print(total_by_type)

    unsuccessful_rate_by_type = (
        unsuccessful_by_type / total_by_type
    ) * 100
    print(unsuccessful_rate_by_type.round(2))

    # Unsuccessful deployments by site
    unsuccessful_by_site = unsuccessful.groupby("site_name").size()
    print(unsuccessful_by_site)

    total_by_site = merged_deployment_data.groupby("site_name").size()
    print(total_by_site)

    unsuccessful_rate_by_site = (
        unsuccessful_by_site / total_by_site
    ) * 100
    print(unsuccessful_rate_by_site.round(2))

    # Root-cause analysis
    root_cause_counts = (
        unsuccessful.groupby("root_cause_category").size()
    )
    print(root_cause_counts)

    root_cause_by_status = unsuccessful.groupby(
        ["status", "root_cause_category"]
    ).size()
    print(root_cause_by_status)

    error_code_counts = unsuccessful.groupby("error_code").size()
    print(error_code_counts)

    # Resolution-time analysis
    avg_resolution_by_status = (
        unsuccessful.groupby("status")["resolution_hours"].mean()
    )
    print(avg_resolution_by_status)

    avg_resolution_by_escalation = (
        unsuccessful.groupby("escalation_level")["resolution_hours"].mean()
    )
    print(avg_resolution_by_escalation)

    escalation_counts = unsuccessful.groupby("escalation_level").size()
    print(escalation_counts)
