from django.core.management.base import BaseCommand
from src.users.models import User, Role

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.setup_staff()

        self.stdout.write(self.style.SUCCESS("ЮЗЕРА СТВОРЕНІ"))

    def setup_staff(self):
        create_staff = []

        users = [
            {'id': 1, 'user': 'Директор', 'first_name': 'Директор', 'last_name': 'Директорович', 'email': 'abs@gmail.com', 'phone_number': '3809900000011', 'password': '1234',
             'user_status': 'Активен', 'is_admin': True, 'role': 'director'},

            {'id': 2, 'user': 'Управляющий', 'first_name': 'Управляющий', 'last_name': 'Управленец', 'email': 'abss@gmail.com', 'phone_number': '3809900000022', 'password': '1234',
             'user_status': 'Активен', 'is_admin': True, 'role': 'manager'},

            {'id': 3, 'user': 'Бухгалтер', 'first_name': 'Бухгалтер', 'last_name': 'Бухгалтеревна', 'email': 'absss@gmail.com', 'phone_number': '3809900000033', 'password': '1234',
             'user_status': 'Активен', 'is_admin': True, 'role': 'accountant'},

            {'id': 4, 'user': 'Сантехник', 'first_name': 'Сантехник', 'last_name': 'Сантехникович', 'email': 'abssss@gmail.com', 'phone_number': '3809900000044', 'password': '1234',
             'user_status': 'Активен', 'is_admin': True, 'role': 'plumber'},

            {'id': 5, 'user': 'Электрик', 'first_name': 'Электрик', 'last_name': 'Электриктрикович', 'email': 'absssss@gmail.com', 'phone_number': '3809900000055', 'password': '1234',
             'user_status': 'Активен', 'is_admin': True, 'role': 'electrician'},
        ]

        for user_obj in users:
            user = User.objects.create_user(
                username=user_obj['user'],
                email=user_obj['email'],
                password=user_obj['password'],
                first_name=user_obj['first_name'],
                last_name=user_obj['last_name'],
                phone_number=user_obj['phone_number'],
                user_status=user_obj['user_status'],
                is_admin=user_obj['is_admin'],
                is_staff=True,
            )
            create_staff.append(user)

            role = Role.objects.create(role=user_obj['role'])

            role.user.add(user)

