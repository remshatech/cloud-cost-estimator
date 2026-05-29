# main.py
# Entry point for the Cloud Cost Estimator
# Handles all user input and output
# Imports calculation logic from calculator.py

from calculator import (
    calculate_ec2,
    calculate_s3,
    total_cost,
    EC2_RATES,
)


# ── Display helpers ────────────────────────────────────────

def print_header():
    print()
    print("=" * 42)
    print("  AWS Cloud Cost Estimator")
    print("  Prices us-east-1 | On-Demand | Linux")
    print("=" * 42)


def print_divider():
    print("-" * 42)


def print_result(result):
    """Prints one service result in a clean format."""
    print()
    print(f"  Service: {result['service']}")
    
    # EC2-specific 
    if result['service'] == "EC2":
        print(f"  Type: {result['instance_type']}")
        print(f"  Hours: {result['hours']} hrs/month")
        print(f"  Rate : ${result['rate_per_hr']}")

    # S3-specific fields
    if result['service'] == "S3":
        print(f"  Storage: {result['storage_gb']} GB total")
        print(f"  Billable: {result['billable_gb']} GB")

    # Cost - same for both
    if result["free_tier"]:
        print(" Cost:     Free (within free tier)")
    else:
        print(f" Cost:     ${result['cost']}/month")


def save_report(results, filename="sample-output.txt"):
    """Saves the session results to a text file."""
    with open(filename, "w") as f:
        f.write("AWS Cloud Cost Estimator Report\n")
        f.write("=" * 42 + "\n\n")

        for r in results:
            f.write(f"Service: {r['service']}\n")

            if r['service'] == "EC2":
                f.write(f"  Instance: {r['instance_type']}\n")
                f.write(f"  Hours: {r['hours']} hrs/month\n")

            if r['service'] == "S3":
                f.write(f"  Storage: {r['storage_gb']} GB\n")
                f.write(f"  Billable: {r['billable_gb']} GB\n")

            if r["free_tier"]:
                f.write(" Cost:     Free (free tier)\n")
            else:
                f.write(f" Cost:     ${r['cost']}/month\n")

            f.write("\n")

        total = total_cost(results)
        f.write("=" * 42 + "\n")
        f.write(f"Estimated Total: ${total} / month\n")

    print(f"\n Report saved → {filename}")

# ── Input helpers ──────────────────────────────────────────

def get_float(prompt):
    """Keeps asking until the user enters a valid number."""
    while True:
        try:
            value =  float(input(prompt))
            if value < 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input - please enter a number.")

def get_instance_type():
    """Shows the instance menu and returns the chosen type."""
    types = list (EC2_RATES.keys())
    
    print()
    print("  Available instance types:")
    for i, (itype, rate) in enumerate(EC2_RATES.items(), 1):
        free_label = " ← free tier eligible" if itype == "t2.micro" else ""
        print(f"   {i}. {itype} (${rate}/hr)")

    while True:
        try:
            choice = int(input("\n Choose instance (1-6): "))
            if 1 <= choice <= len(types):
                return types[choice - 1]
            print(f"  Enter a number between 1 and {len(types)}.")
        except ValueError:
            print("  Please enter a number.")

# ── Main program ───────────────────────────────────────────

def run() :
    print_header()

    results = []    # stores all calculated results this session
    running = True

    while running:
        print()
        print("  What would you like to estimate?")
        print("   1. EC2 instance cost")
        print("   2. S3 storage cost")
        print("   3. Show session total")
        print(" 4. save report and exit")

        choice = input("\n  Enter choice (1-4):").strip()
        if choice == "1":
            print_divider()
            print("  EC2 Cost Calculator")
            print_divider()

            hours         = get_float("  Hours per month (max 744): ")
            instance_type = get_instance_type()

            result = calculate_ec2(hours, instance_type)
            results.append(result)
            print_result(result)

# ── S3 ───────────────────────────────────────────
        elif choice == "2":
            print_divider()
            print("  S3 Cost Calculator")
            print_divider()

            storage_gb = get_float("  Storage in GB: ")

            result = calculate_s3(storage_gb)
            results.append(result)
            print_result(result)

# ── Session total ───────────────────────────────────────────
        elif choice == "3":
            if not results:
                print("\n No calculations yet.")
            else:
                print_divider()
                print(f"  Services calculated: {len(results)}")
                print(f"  Estimated Total: ${total_cost(results)} / month")

# ── Save and exit ─────────────────────────────────
        elif choice == "4":
            if results:
                save_report(results)
                print()
                print("  Goodbye!")
            running = False

        else:
            print("  Invalid choice — enter 1, 2, 3, or 4.")


# This block runs only when you execute main.py directly
# It does NOT run when calculator.py imports this file
if __name__ == "__main__":
    run()