"""
Core IAM Engine for lifecycle event processing
"""

from enum import Enum
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class LifecycleEventType(str, Enum):
    """IAM lifecycle event types"""
    JOINER = "joiner"
    MOVER = "mover"
    LEAVER = "leaver"


class Employee(BaseModel):
    """Employee representation in the IAM system"""
    id: str
    name: str
    email: str
    department: str
    role: str
    assigned_applications: List[str] = Field(default_factory=list)
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.now)


class AccessRight(BaseModel):
    """Access right granted to an employee"""
    employee_id: str
    application: str
    role: str
    granted_at: datetime = Field(default_factory=datetime.now)
    revoked_at: Optional[datetime] = None
    is_active: bool = True


class IAMEngine:
    """Core IAM lifecycle management engine"""

    def __init__(self):
        self.employees: Dict[str, Employee] = {}
        self.access_rights: List[AccessRight] = []

    def process_joiner_event(self, employee: Employee, apps: List[str]) -> Employee:
        """
        Process new employee joining.
        Automatically assign applications based on department and role.
        """
        employee.assigned_applications = apps
        self.employees[employee.id] = employee
        
        # Grant access to applications
        for app in apps:
            access = AccessRight(
                employee_id=employee.id,
                application=app,
                role=employee.role
            )
            self.access_rights.append(access)
        
        return employee

    def process_mover_event(self, employee_id: str, new_role: str, new_apps: List[str]) -> Optional[Employee]:
        """
        Process role change for existing employee.
        Update role and applications.
        """
        employee = self.employees.get(employee_id)
        if not employee:
            return None

        # Revoke old access
        for access in self.access_rights:
            if access.employee_id == employee_id and access.is_active:
                access.is_active = False
                access.revoked_at = datetime.now()

        # Update employee
        employee.role = new_role
        employee.assigned_applications = new_apps

        # Grant new access
        for app in new_apps:
            access = AccessRight(
                employee_id=employee_id,
                application=app,
                role=new_role
            )
            self.access_rights.append(access)

        return employee

    def process_leaver_event(self, employee_id: str) -> Optional[Employee]:
        """
        Process employee departure.
        Revoke all access and mark employee as inactive.
        """
        employee = self.employees.get(employee_id)
        if not employee:
            return None

        # Revoke all active access
        for access in self.access_rights:
            if access.employee_id == employee_id and access.is_active:
                access.is_active = False
                access.revoked_at = datetime.now()

        # Mark employee as inactive
        employee.status = "inactive"
        
        return employee

    def get_active_access(self, employee_id: str) -> List[AccessRight]:
        """Get all active access rights for an employee"""
        return [
            access for access in self.access_rights
            if access.employee_id == employee_id and access.is_active
        ]

    def generate_audit_log(self, employee_id: str) -> Dict:
        """Generate audit log for an employee's IAM lifecycle"""
        employee = self.employees.get(employee_id)
        if not employee:
            return {}

        return {
            "employee": employee.dict(),
            "access_history": [
                access.dict() for access in self.access_rights
                if access.employee_id == employee_id
            ]
        }
