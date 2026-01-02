# # Today’s goal is to write your first Python script.

# # You will create a Python script that:

# # Takes threshold values (CPU, disk, memory) from user input
# # Also fetches system metrics using a Python library (example: psutil)
# # Compares metrics against thresholds
# # Prints the result to the terminal
# # This is your first step towards thinking like a DevOps engineer using Python.


import psutil

# Function to check CPU usage
def check_cpu(threshold):
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_usage}%")

    if cpu_usage > threshold:
        print(" CPU usage is above threshold")
    else:
        print(" CPU usage is within limit")


# Function to check Memory usage
def check_memory(threshold):
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    print(f"Memory Usage: {memory_usage}%")

    if memory_usage > threshold:
        print(" Memory usage is above threshold")
    else:
        print(" Memory usage is within limit")


# Function to check Disk usage
def check_disk(threshold):
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    print(f"Disk Usage: {disk_usage}%")

    if disk_usage > threshold:
        print("Disk usage is above threshold")
    else:
        print(" Disk usage is within limit")


# ---- Main Program ----
print("Enter threshold values (%)")

cpu_threshold = float(input("CPU Threshold: "))
memory_threshold = float(input("Memory Threshold: "))
disk_threshold = float(input("Disk Threshold: "))

print("\n--- System Health Check ---")

check_cpu(cpu_threshold)
check_memory(memory_threshold)
check_disk(disk_threshold)
