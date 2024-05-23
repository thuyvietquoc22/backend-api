from bson import ObjectId

from app.decorator import singleton
from app.decorator.parser import parse_as
from app.entity.game.user import UserRegister, UserCreate, UserResponse, UserUpdate, User
from app.exceptions.not_updated_error import NotUpdatedError
from app.repositories.user import UserRepository
from app.utils.jwt_service import JWTService


@singleton
class UserService:

    def __init__(self):
        self.user_repo = UserRepository()
        self.jwt_service = JWTService()

    @parse_as(UserResponse, get_first=True)
    def register_user(self, user_register: UserRegister):
        user_create = UserCreate.from_register(user_register)

        # Check this user exist
        try:
            existed = self.user_repo.get_user_info_by_tele_id(user_create.tele_id)
            return self.update_user_info(user_register, existed.id)
        except ValueError as e:
            pass

        # Check ref code
        if user_create.ref_code is not None:
            ref_user = self.user_repo.get_user_info_by_tele_id(user_create.ref_code)
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
        token = self.jwt_service.generate_token(user)
        return token

    def get_user_info_by_token(self, token) -> User:
        payload = JWTService().decode_token(token)
        tele_id = payload.get("sub")
        user = self.user_repo.get_user_info_by_tele_id(tele_id)
        return user

    def get_invited_user(self, tele_id):
        invited_user = self.user_repo.get_invited_user(tele_id)
        return invited_user

