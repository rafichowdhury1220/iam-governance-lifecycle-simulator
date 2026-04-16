"""
Role-Based Access Control (RBAC) module
"""

from typing import Dict, List, Set


class RoleDefinition:
    """Define a role with associated permissions"""
    
    def __init__(self, name: str, permissions: Set[str]):
        self.name = name
        self.permissions = permissions

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions


class RBACManager:
    """Manage roles and access control policies"""

    def __init__(self):
        self.roles: Dict[str, RoleDefinition] = {}
        self.department_role_mapping: Dict[str, List[str]] = {}
        self._initialize_default_roles()

    def _initialize_default_roles(self):
        """Initialize default organizational roles"""
        self.roles["engineer"] = RoleDefinition(
            "engineer",
            {"code_repo", "ci_cd", "dev_tools", "logging"}
        )
        
        self.roles["manager"] = RoleDefinition(
            "manager",
            {"reporting", "team_access", "planning_tools", "hr_system"}
        )
        
        self.roles["analyst"] = RoleDefinition(
            "analyst",
            {"reporting", "analytics", "dashboard", "data_warehouse"}
        )
        
        self.roles["security"] = RoleDefinition(
            "security",
            {"security_tools", "audit_logs", "policy_management", "mfa"}
        )

    def map_department_to_roles(self, department: str) -> List[str]:
        """Map department to default roles"""
        mappings = {
            "engineering": ["engineer", "code_repo", "ci_cd"],
            "management": ["manager", "reporting"],
            "analytics": ["analyst", "reporting", "analytics"],
            "security": ["security", "security_tools"],
        }
        return mappings.get(department, ["analyst"])

    def get_role_permissions(self, role_name: str) -> Set[str]:
        """Get permissions for a role"""
        role = self.roles.get(role_name)
        return role.permissions if role else set()

    def create_custom_role(self, name: str, permissions: Set[str]):
        """Create a custom role with specified permissions"""
        self.roles[name] = RoleDefinition(name, permissions)

    def revoke_role(self, role_name: str):
        """Remove a role from the system"""
        if role_name in self.roles:
            del self.roles[role_name]
