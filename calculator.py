# calculator.py
# Core calculation logic for the Cloud Cost Estimator
#this file handles only math - no user inpot, no printing
# It is imported and used by main.py

# ── EC2 pricing (us-east-1, on-demand, linux) ──────────────
EC2_RATES = {
    't2.micro': 0.0116,
    't2.small': 0.0230,
    't2.medium': 0.0464,
    't3.micro': 0.0104,
    't3.small': 0.0208,
    't3.medium': 0.0416,
}

# ── S3 pricing ─────────────────────────────────────────────
S3_RATE_PER_GB = 0.023    # per GB per month
S3_FREE_TIER_GB = 5       # first 5 GB is always free

# ── EC2 free tier ───────────────────────────────────────────
EC2_FREE_TIER_HOURS = 750
EC2_FREE_TIER_TYPE = 't2.micro'


def calculate_ec2(hours, instance_type):
    """
    Calculate monthly EC2 cost.
  
    Parameters:
        hours (float)     - hours of usage per month
        instance_type (str) - EC2 instance type e.g. "t2.micro"

    Returns:
        dict with cost breakdown
    """
    if instance_type not in EC2_RATES:
        raise ValueError(f"Unknown instance type: {instance_type}")

    rate = EC2_RATES[instance_type]
    raw_cost = hours * rate

    # Free tier : t2.micro under 750 hours = $0
    is_free = (
        instance_type == EC2_FREE_TIER_TYPE and
        hours <= EC2_FREE_TIER_HOURS
    )

    return {
        "service": "EC2",
        "instance_type": instance_type,
        "hours": hours,
        "rate_per_hr": rate,
        "cost" : 0 if is_free else round(raw_cost, 4),
        "free_tier" : is_free
    }

def calculate_s3(storage_gb):
    """
    Calculate monthly S3 storage cost.

    Parameters:
        storage_gb (float) - total GB stored

    Returns:
        dict with cost breakdown
    """
    billable_storage = max(0, storage_gb - S3_FREE_TIER_GB)
    cost = billable_storage * S3_RATE_PER_GB

    return {
        "service": "S3",
        "storage_gb": storage_gb,
        "billable_gb": billable_storage,
        "rate_per_gb": S3_RATE_PER_GB,
        "cost": round(cost, 4),
        "free_tier": storage_gb <= S3_FREE_TIER_GB,
    }


def total_cost(results) :
    """
    Adds up the cost across all calculated services.
    
    Parameters:
        results (list) - list of docts returned by calculate_ec2 \ calculate_s3
        
        Returns:
        float - total monthly cost
        """
    return round(sum(r["cost"] for r in results), 4)