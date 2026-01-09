
"""
Log Analyzer Script
Analyzes log files and generates summary reports
"""

import json
from datetime import datetime


def read_log_file(file_path):
    """
    Reads log file and returns its content
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if not lines:
                raise ValueError("Log file is empty")
            return lines
    except FileNotFoundError:
        print(f"ERROR: File '{file_path}' not found")
    except ValueError as error:
        print(f"ERROR: {error}")
    except Exception as error:
        print(f"ERROR: Unexpected error reading file: {error}")

    return None


def analyze_logs(log_lines):
    """
    Analyzes log lines and counts log levels
    """
    log_counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    log_details = {
        "INFO": [],
        "WARNING": [],
        "ERROR": []
    }

    total_lines = 0

    for line in log_lines:
        line = line.strip()
        if not line:
            continue

        total_lines += 1

        if "INFO" in line:
            log_counts["INFO"] += 1
            log_details["INFO"].append(line)
        elif "WARNING" in line:
            log_counts["WARNING"] += 1
            log_details["WARNING"].append(line)
        elif "ERROR" in line:
            log_counts["ERROR"] += 1
            log_details["ERROR"].append(line)

    return {
        "counts": log_counts,
        "details": log_details,
        "total_lines": total_lines
    }


def print_summary(analysis):
    """
    Prints summary to terminal
    """
    print("\n" + "=" * 60)
    print("LOG ANALYSIS SUMMARY")
    print("=" * 60)

    print(f"Total log entries processed: {analysis['total_lines']}")
    print("-" * 60)

    counts = analysis["counts"]
    total_messages = sum(counts.values())

    for level in ["INFO", "WARNING", "ERROR"]:
        count = counts[level]
        percentage = (count / total_messages * 100) if total_messages else 0
        print(f"{level:10} : {count:4} ({percentage:5.1f}%)")

    print("=" * 60)

    if counts["ERROR"] > 0:
        print(f"\n  CRITICAL: Found {counts['ERROR']} ERROR message(s)")
    if counts["WARNING"] > 0:
        print(f"  ATTENTION: Found {counts['WARNING']} WARNING message(s)")

    print()


def write_text_summary(analysis, output_file):
    """
    Writes summary to a text file
    """
    try:
        with open(output_file, "w") as file:
            file.write("=" * 60 + "\n")
            file.write("LOG ANALYSIS SUMMARY\n")
            file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 60 + "\n\n")

            file.write(f"Total log entries processed: {analysis['total_lines']}\n")
            file.write("-" * 60 + "\n\n")

            counts = analysis["counts"]
            total_messages = sum(counts.values())

            for level in ["INFO", "WARNING", "ERROR"]:
                count = counts[level]
                percentage = (count / total_messages * 100) if total_messages else 0
                file.write(f"{level:10} : {count:4} ({percentage:5.1f}%)\n")

            file.write("\n" + "=" * 60 + "\n\n")

            for level in ["ERROR", "WARNING", "INFO"]:
                if counts[level] > 0:
                    file.write(f"{level} MESSAGES ({counts[level]}):\n")
                    file.write("-" * 60 + "\n")
                    for message in analysis["details"][level]:
                        file.write(message + "\n")
                    file.write("\n")

        print(f" Text summary written to: {output_file}")

    except Exception as error:
        print(f"ERROR: Failed to write text summary: {error}")


def write_json_summary(analysis, output_file):
    """
    Writes summary to a JSON file
    """
    try:
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_lines": analysis["total_lines"],
            "summary": analysis["counts"],
            "details": analysis["details"]
        }

        with open(output_file, "w") as file:
            json.dump(data, file, indent=2)

        print(f" JSON summary written to: {output_file}")

    except Exception as error:
        print(f"ERROR: Failed to write JSON summary: {error}")


def main():
    """
    Main execution function
    """
    log_file = "app.log"
    text_output = "log_summary.txt"
    json_output = "log_summary.json"

    print("\n Starting Log Analysis...")
    print(f" Reading log file: {log_file}")

    log_lines = read_log_file(log_file)
    if not log_lines:
        print("\n Log analysis failed")
        return

    print(f" Successfully read {len(log_lines)} lines")

    analysis = analyze_logs(log_lines)

    print_summary(analysis)

    print(" Writing output files...")
    write_text_summary(analysis, text_output)
    write_json_summary(analysis, json_output)

    print("\n Log analysis completed successfully!\n")


if __name__ == "__main__":
    main()
