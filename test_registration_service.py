from services.game.registration_service import RegistrationService

registration = RegistrationService()

manager, finance, created = registration.register(
    555555555,
    "Edoardo"
)

print()

if created:
    print("NUOVO MANAGER CREATO")
else:
    print("MANAGER GIÀ ESISTENTE")

print()
print(manager)

print()
print(finance)