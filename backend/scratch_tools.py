from app.auth.user_store import create_user, get_user_by_email
from app.core.security import hash_password, verify_password

u = create_user("test@example.com", hash_password("secret123"))
print(u.id)
found = get_user_by_email("TEST@example.com")
print(found.email, verify_password("secret123", found.password_hash))