ROLES = [
    ("ROLE_ADMIN", "admin"),
    ("ROLE_SUPER_ADMIN", "surper_admin"),
    ("ROLE_OWNER", "Propriétaire"),
    ("ROLE_MANAGER", "Gérant"),
    ("ROLE_ACCOUNTANT", "Comptable"),
    ("ROLE_COOKER", "Cuisinier"),
    ("ROLE_TECHNICIAN", "Technicien"),
    ("ROLE_ANONYME", "Anonyme"),
]

STATUT = [("CREATED", "nouveau"), ("VALIDATED", "validation"), ("SUBMITTED", "Soumis"),
          ("ACQUISITION", "acquisition"), ("CLOSED", "closed"), ("REJECTED", "rejeté")]

ROLE_TECHNICIAN_HERITED = ["ROLE_COOKER", "ROLE_TECHNICIAN"]

ROLE_ADMIN_HERITED = ["ROLE_SUPER_ADMIN", "ROLE_ADMIN"]

ROLE_OWNER_HERITED = ["ROLE_SUPER_ADMIN", "ROLE_ADMIN", "ROLE_OWNER"]


EDITABLE_STATUT = ["CREATED", "REJECTED"]
