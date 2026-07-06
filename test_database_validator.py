from services.validators.database_validator import DatabaseValidator

validator = DatabaseValidator()

errors = validator.validate()

print(f"Errori trovati: {len(errors)}")

for error in errors[:100]:
    print("-", error)