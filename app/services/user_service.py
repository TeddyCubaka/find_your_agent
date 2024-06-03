class UserService:
    @staticmethod
    def get_all_users():
        # Logique pour obtenir tous les utilisateurs
        return [{'id': 1, 'name': 'John Doe'}]

    @staticmethod
    def get_user_by_id(user_id):
        # Logique pour obtenir un utilisateur par ID
        return {'id': user_id, 'name': 'John Doe'}

    @staticmethod
    def create_user(data):
        # Logique pour créer un nouvel utilisateur
        # Ici vous pouvez ajouter la logique de validation et de création d'utilisateur
        return {'id': 2, 'name': data.get('name')}
