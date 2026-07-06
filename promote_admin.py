import sys
from sqlmodel import Session, select
from app.database.connection import engine
from app.models import User

def promote(email: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            print(f"Error: User with email '{email}' not found.")
            return
        user.role = "admin"
        session.add(user)
        session.commit()
        print(f"Success: User '{user.name}' ({email}) promoted to 'admin'!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python promote_admin.py <email>")
        sys.exit(1)
    promote(sys.argv[1])
