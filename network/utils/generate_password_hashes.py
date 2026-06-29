import bcrypt

passwords = {
    "Officer@123": "Officer",
    "Engineer@123": "Engineer",
    "Staff@123": "Staff",
    "Admin@123": "Admin",
    "Guest@123": "Guest"
}

print("\nGenerated Password Hashes\n")

for password, role in passwords.items():

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    print(role)
    print(hashed.decode())
    print()