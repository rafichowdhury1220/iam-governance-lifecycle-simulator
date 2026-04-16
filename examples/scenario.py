"""
Example scenario demonstrating the IAM lifecycle simulator
"""

from iam_simulator.core import IAMEngine, Employee, LifecycleEventType
from iam_simulator.events import EventManager
from iam_simulator.rbac import RBACManager


def run_scenario():
    """Run an example IAM lifecycle scenario"""
    
    # Initialize components
    engine = IAMEngine()
    event_manager = EventManager()
    rbac = RBACManager()

    print("=" * 60)
    print("IAM Governance Lifecycle Simulator - Example Scenario")
    print("=" * 60)

    # Scenario 1: Employee Joins
    print("\n[1] JOINER EVENT: New Engineer Hired")
    print("-" * 60)
    
    emp1 = Employee(
        id="emp_001",
        name="Alice Johnson",
        email="alice@company.com",
        department="engineering",
        role="Software Engineer"
    )
    
    engineer_apps = ["code_repo", "ci_cd", "slack", "jira"]
    emp1 = engine.process_joiner_event(emp1, engineer_apps)
    
    print(f"✓ Employee: {emp1.name} (ID: {emp1.id})")
    print(f"✓ Department: {emp1.department}")
    print(f"✓ Role: {emp1.role}")
    print(f"✓ Assigned Applications: {', '.join(emp1.assigned_applications)}")
    
    # Create and log joiner event
    event_manager.create_joiner_event(
        emp1.id, emp1.name,
        {"department": emp1.department, "role": emp1.role}
    )

    # Scenario 2: Employee Gets Promoted
    print("\n[2] MOVER EVENT: Role Change - Promotion to Tech Lead")
    print("-" * 60)
    
    new_role = "Tech Lead"
    new_apps = ["code_repo", "ci_cd", "slack", "jira", "project_management", "reporting"]
    
    emp1 = engine.process_mover_event(emp1.id, new_role, new_apps)
    
    print(f"✓ New Role: {emp1.role}")
    print(f"✓ Updated Applications: {', '.join(emp1.assigned_applications)}")
    print(f"✓ Active Access Rights: {len(engine.get_active_access(emp1.id))}")
    
    # Create and log mover event
    event_manager.create_mover_event(
        emp1.id, emp1.name,
        {"old_role": "Software Engineer", "new_role": new_role}
    )

    # Scenario 3: Employee Leaves Company
    print("\n[3] LEAVER EVENT: Employee Departure")
    print("-" * 60)
    
    emp1 = engine.process_leaver_event(emp1.id)
    
    print(f"✓ Status: {emp1.status}")
    print(f"✓ Active Access Rights: {len(engine.get_active_access(emp1.id))}")
    print(f"✓ All applications access revoked automatically")
    
    # Create and log leaver event
    event_manager.create_leaver_event(
        emp1.id, emp1.name,
        {"reason": "Resignation"}
    )

    # Display audit log
    print("\n[4] AUDIT LOG: Complete Employee Lifecycle")
    print("-" * 60)
    
    audit = engine.generate_audit_log(emp1.id)
    print(f"Employee: {audit['employee']['name']}")
    print(f"Status: {audit['employee']['status']}")
    print(f"Total Access Events: {len(audit['access_history'])}")
    
    print("\nAccess Timeline:")
    for i, access in enumerate(audit['access_history'], 1):
        status = "✓ GRANTED" if access['is_active'] else "✗ REVOKED"
        print(f"  {i}. {access['application']} - {status}")

    # Event history
    print("\n[5] EVENT HISTORY")
    print("-" * 60)
    
    for event in event_manager.get_event_history():
        print(f"[{event.event_type.value.upper()}] {event.employee_name} - {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n" + "=" * 60)
    print("Scenario Complete - IAM Lifecycle Demonstrated Successfully")
    print("=" * 60)


if __name__ == "__main__":
    run_scenario()
