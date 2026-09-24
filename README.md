# Cloud Cost Estimator

## The Problem

Teams provisioning AWS resources without cost visibility get
surprised by monthly bills. Without a quick way to estimate
costs before spinning up infrastructure, spend spirals —
especially in dev environments where instances are left running.

## The Solution

A Python CLI tool that estimates EC2 and S3 monthly costs before
resources are provisioned. Identifies free tier eligibility and
generates a cost report saved to a text file.

## Why This Approach

**CLI over dashboard** — zero setup friction, runs anywhere Python
runs, no browser or login required in a CI environment.

**Modular design** — `calculator.py` handles only math and is
importable by other tools or Lambda functions without pulling in
the CLI interface. `main.py` handles only user interaction.

**No external dependencies** — standard Python library only.
Runs in restricted environments without pip access.

## Architecture

```
User Input
    ↓
main.py  (handles interface and user input)
    ↓
calculator.py  (handles cost calculations only)
    ↓
Cost Result + report.txt
```

## Project Structure

```
cloud-cost-estimator/
├── calculator.py        # cost logic — importable module
├── main.py              # CLI entry point
├── test_calculator.py   # pytest unit tests
├── requirements.txt     # pytest dependency
└── README.md
```

## How to Run

```bash
git clone https://github.com/remshatech/cloud-cost-estimator
cd cloud-cost-estimator
python main.py
```

## Running Tests

```bash
pip install -r requirements.txt
python -m pytest test_calculator.py -v
```

Expected output — 10 tests, all passing:

```
test_calculator.py::test_ec2_free_tier           PASSED
test_calculator.py::test_ec2_over_free_tier      PASSED
test_calculator.py::test_ec2_paid_instance       PASSED
test_calculator.py::test_ec2_unknown_instance    PASSED
test_calculator.py::test_ec2_zero_hours          PASSED
test_calculator.py::test_s3_free_tier            PASSED
test_calculator.py::test_s3_exact_free_tier      PASSED
test_calculator.py::test_s3_over_free_tier       PASSED
test_calculator.py::test_total_cost              PASSED
test_calculator.py::test_total_cost_all_free     PASSED

10 passed
```

## Trade-offs Accepted

**Hardcoded prices** — a production version would call the
AWS Pricing API for real-time rates. Hardcoded values are
sufficient for a planning tool and remove the API dependency.

**Text file output** — cost reports write to a local .txt file.
A production version might write to S3 or send via SNS alert.

## What I Would Add Next

- AWS Pricing API integration for real-time rates
- Lambda wrapper to run on a schedule and post to Slack
- Multi-region pricing support
- GitHub Actions CI pipeline to run tests on every push

## Tech Stack

Python 3 · pytest · CLI · Modular design

---

*september 2026*