import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from inspectdata import load_and_prepare_data
from pathlib import Path

deployments, devices = load_and_prepare_data()
unsuccessful=deployments[deployments['status'].isin(['Failed','Rolled Back'])
                         ]
root_cause_counts=unsuccessful['root_cause_category'].value_counts()
values = root_cause_counts.values
colors = [
    '#176B5B' if value == max(values) else '#A8D5CC'
    for value in values
]

plt.figure(figsize=(10,6))
ax=sns.barplot(x=root_cause_counts.values,y=root_cause_counts.index,hue=root_cause_counts.index,
    palette=colors,
    legend=False)
ax.set_axisbelow(True)
ax.grid(axis='x', linestyle='--', alpha=0.25)
for container in ax.containers:
    ax.bar_label(
        container,
        padding=4,
        fontsize=9
    )

plt.title('Unsucessful Firmware Deployement by Root Cause')
plt.xlabel('Number of Unsuccessful Attempts')
plt.ylabel('Root-Cause Categories')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


project_root = Path(__file__).resolve().parents[1]

plt.tight_layout()
plt.savefig(project_root / "root_cause_analysis.png", dpi=300)
#plt.show()

unsuccessful_by_device_type=unsuccessful.groupby('device_type').size()
total_by_device_type=deployments.groupby('device_type').size()
unsuccessful_deployment_rate_percent=((unsuccessful_by_device_type/total_by_device_type)*100).round(2)
values = unsuccessful_deployment_rate_percent.values

colors = [
    '#176B5B' if value == max(values) else '#A8D5CC'
    for value in values
]

    


plt.figure(figsize=(10, 6))

ax = sns.barplot(
    x=unsuccessful_deployment_rate_percent.index,
    y=unsuccessful_deployment_rate_percent.values,
    hue=unsuccessful_deployment_rate_percent.index,
        palette=colors,
        legend=False
)
ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='--', alpha=0.25)
for container in ax.containers:
    ax.bar_label(
        container,
        padding=4,
        fontsize=9
    )

plt.title("Unsuccessful Firmware Deployment Rate by Device Type")
plt.xlabel("Device Type")
plt.ylabel("Unsuccessful Deployment Rate (%)")
plt.xticks(rotation=25, ha="right")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(project_root / "device_type_failure_rate.png", dpi=300)
#plt.show()



unsuccessful_by_site_type=unsuccessful.groupby('site_name').size()
total_by_site_type=deployments.groupby('site_name').size()
unsuccessful_deployment_rate_sitetype_percent=((unsuccessful_by_site_type/total_by_site_type)*100).round(2)
values=unsuccessful_deployment_rate_sitetype_percent.values
colors=[ '#176B5B' if value == max(values) else '#A8D5CC'
    for value in values]

plt.figure(figsize=(10, 9))

ax = sns.barplot(
    x=unsuccessful_deployment_rate_sitetype_percent.values,
    y=unsuccessful_deployment_rate_sitetype_percent.index,
     hue=unsuccessful_deployment_rate_sitetype_percent.index,
    palette=colors,
    legend=False
)
ax.set_axisbelow(True)
ax.grid(axis='x', linestyle='--', alpha=0.25)
for container in ax.containers:
    ax.bar_label(
        container,
        padding=4,
        fontsize=9
    )
#ax.bar_label(ax.containers[0], fmt="%.2f%%", padding=4,fontsize=9)
plt.title("Unsuccessful Firmware Deployment Rate by Site")
plt.xlabel("Unsuccessful Deployment Rate (%)")
plt.ylabel("Site Name")

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(project_root / "site_failure_rate.png", dpi=300)
#plt.show()

avg_resolution_by_escalation = (
unsuccessful.groupby("escalation_level")["resolution_hours"].mean()
    ).round(2)
values = avg_resolution_by_escalation.values

colors = [
    '#176B5B' if value == max(values) else '#A8D5CC'
    for value in values
]

plt.figure(figsize=(10,7))
ax=sns.barplot( x=avg_resolution_by_escalation.index,
    y=avg_resolution_by_escalation.values,
    hue=avg_resolution_by_escalation.index,
        palette=colors,
        legend=False)
for container in ax.containers:
    ax.bar_label(
        container,
        padding=4,
        fontsize=9
    )

#ax.bar_label(ax.containers[0],fmt='%.2f Hours',padding=4)
ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='--', alpha=0.25)
plt.title('Average Resolution Time by Escalation Level')
plt.xlabel('Escalation level')
plt.ylabel('Average resolution time (hours)')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(project_root/'resolution_time_by_escalation.png',dpi=300)
plt.show()
