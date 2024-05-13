from bson import ObjectId

from decorator import singleton
from decorator.parser import parse_as
from entity.user import UserRegister, UserCreate, UserResponse, UserUpdate
from exceptions.not_updated_error import NotUpdatedError
from repositories.user import UserRepository
from utils.jwt_service import JWTService


@singleton
class UserService:

    def __init__(self):
        self.user_repo = UserRepository()
        self.jwt_service = JWTService()

    @parse_as(UserResponse, get_first=True)
    def register_user(self, user_register: UserRegister):
        user_create = UserCreate.from_register(user_register)

        # Check this user exist
        existed = self.user_repo.get_user_info_by_tele_id(user_create.tele_id)
        if existed is not None:
            return self.update_user_info(user_register, existed.id)

        # Check ref code
        if user_create.ref_code is not None:
            ref_user = self.user_repo.check_ref_code(user_create.ref_code)
            if ref_user is None:
                raise ValueError("Ref code not found.")

        # Save user to database
        return self.user_repo.create(user_create)

    def update_user_info(self, user_create: UserRegister, user_id: str):
        user_update = UserUpdate(**user_create.dict())
        try:
            self.user_repo.update(user_id, user_update)
        except NotUpdatedError as e:
            pass
        result = self.user_repo.aggregate({"$match": {"_id": ObjectId(user_id)}})
        return result

    def get_user_info_by_id(self, tele_id):
        return self.user_repo.get_user_info_by_tele_id(tele_id)

    def get_user_token(self, tele_id):
        user: UserResponse = self.user_repo.get_user_info_by_tele_id(tele_id)
        token = self.jwt_service.generate_token(user.tele_id)
        return token
