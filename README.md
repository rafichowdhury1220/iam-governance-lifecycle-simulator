# IAM Governance Lifecycle Simulator

A Python-based solution for simulating enterprise identity and access management (IAM) lifecycle events.

## Concept

Simulate enterprise identity lifecycle management across three core events:
- **Joiner**: New employee onboarding with automatic role assignment
- **Mover**: Role changes and access modifications  
- **Leaver**: Employee departure with automated deprovisioning

## Architecture Flow

```
HR System → IAM Engine → Application Access
                ↓
          • RBAC (Role-Based Access Control)
          • Access provisioning
          • Automated deprovisioning
          • Identity governance
```

## Key Features

- Event-driven IAM lifecycle simulation
- Role-based access control (RBAC)
- Automated access provisioning/deprovisioning
- Identity governance workflow
- User journey tracking

## Quick Start

```bash
pip install -r requirements.txt
python -m iam_simulator
```

## Example Scenario

```
1. New Employee Created
   ↓
2. IAM assigns roles based on department
   ↓
3. Access granted to required applications
   ↓
4. Employee leaves
   ↓
5. Access revoked automatically
```

## Project Structure

```
iam-joiner-mover-leaver/
├── README.md
├── requirements.txt
├── iam_simulator/
│   ├── __init__.py
│   ├── core.py           # Core IAM engine
│   ├── events.py         # Lifecycle events
│   └── rbac.py           # Role-based access control
└── examples/
    └── scenario.py       # Example simulation
```

## Use Case

Perfect for solution architects designing IAM systems for enterprises needing to:
- Standardize employee onboarding workflows
- Implement consistent access provisioning
- Ensure compliant deprovisioning
- Track identity governance across applications
