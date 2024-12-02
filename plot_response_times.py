import matplotlib.pyplot as plt
import csv
import sys

def plot_response_times(file_name):
    # Read response times
    response_times = []
    with open(file_name, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            response_times.append(float(row[2]))

    # Plot the response times
    plt.figure(figsize=(10, 6))
    plt.plot(response_times, marker='o')
    plt.title(f"Response Times for {file_name}")
    plt.xlabel("Request Number")
    plt.ylabel("Response Time (ms)")
    plt.grid(True)
    plt.show()

# Accept file name as a command-line argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_response_times.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    plot_response_times(file_name)