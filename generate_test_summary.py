import pandas as pd

# Load the CSV files
registration = pd.read_csv("load_test_results.csv")
login = pd.read_csv("login_test_results.csv")

# Summarize metrics
summary = {
    "Metric": ["Total Requests", "Average Response Time (ms)", "Success Rate"],
    "Registration": [
        len(registration),
        registration["responseTime(ms)"].mean(),
        len(registration[registration["result"] == "Success"]) / len(registration) * 100
    ],
    "Login": [
        len(login),
        login["responseTime(ms)"].mean(),
        len(login[login["result"] == "Success"]) / len(login) * 100
    ]
}

# Convert to DataFrame
summary_df = pd.DataFrame(summary)

# Save summary to CSV
summary_df.to_csv("test_summary.csv", index=False)

# Print Summary
print(summary_df)