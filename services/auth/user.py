from decorator import singleton
from decorator.parser import parse_as
from entity.user import UserRegister, UserCreate, UserResponse
from repositories.user import UserRepository


@singleton
class UserService:

    def __init__(self):
        self.user_repo = UserRepository()

    @parse_as(UserResponse)
    def register_user(self, user_register: UserRegister):
        user_create = UserCreate.from_register(user_register)

        # Check ref code
        if user_create.ref_code is not None:
            ref_user = self.user_repo.check_ref_code(user_create.ref_code)
            if ref_user is None:
                raise ValueError("Ref code not found.")

        # Save user to database
        return self.user_repo.create(user_create)
