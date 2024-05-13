from abc import ABC, abstractmethod
from math import ceil
from typing import TypeVar, Generic, Optional

from bson import ObjectId
from pydantic import BaseModel
from pymongo.collection import Collection

from decorator.parser import parse_val_as
from entity.core import BaseMongoModel
from entity.pagination import Pageable

Model = TypeVar("Model", bound=BaseMongoModel)
CreateModel = TypeVar("CreateModel", bound=BaseMongoModel)
UpdateModel = TypeVar("UpdateModel", bound=BaseModel)


class BaseRepository(Generic[Model, CreateModel, UpdateModel], ABC):

    @property
    @abstractmethod
    def collection(self) -> Collection:
        pass

    @property
    def root_pipeline(self):
        return []

    def aggregate(self, *aggregate: dict, insert_before: bool = False):
        """
        Dùng insert_before true khi cần query các trường có sẵn trong DB
        :param aggregate: aggregate
        :param insert_before: Vị trí của các `aggregate` được thêm vào pipeline
        :return:
        """
        if insert_before:
            pipeline = list(aggregate) + self.root_pipeline
        else:
            pipeline = self.root_pipeline + list(aggregate)
        return self.collection.aggregate(pipeline)

    def is_exists_id(self, id_: str) -> bool:
        """Updated"""
        id_ = ObjectId(id_)
        return self.collection.count_documents({"_id": id_}) > 0

    def is_exists_ids(self, ids: list[str]) -> bool:
        """Updated"""
        ids = [ObjectId(id_) for id_ in ids]
        return self.collection.count_documents({"_id": {"$in": ids}}) == len(ids)

    def get_pageable(self, pageable: Pageable, query: Optional[dict] = None) -> Pageable:
        """Updated"""
        total_elements = self.collection.count_documents(query or {})
        total_pages = ceil(total_elements / pageable.limit)
        pageable.pages = total_pages
        pageable.items = total_elements
        return pageable

    def find_by_ids(self, ids: list[str], pageable: Pageable = None):
        ids = [ObjectId(id_) for id_ in ids]
        if pageable:
            self.get_pageable(pageable, {"_id": {"$in": ids}})
            return self.collection.find({"_id": {"$in": ids}}).skip(pageable.skip).limit(pageable.limit)
        else:
            return self.collection.find({"_id": {"$in": ids}})

    def get_all(self, pageable: Pageable = None):
        """Updated"""
        pipeline = self.root_pipeline
        if pageable is not None:
            self.get_pageable(pageable, {})
            pipeline += pageable.pipeline

        return self.collection.aggregate(pipeline)

    def get_by_id(self, obj_id: str, response_type: type = None):
        result = self.aggregate({"$match": {"_id": ObjectId(obj_id)}})
        return result if response_type is None else parse_val_as(result, response_type, get_first=True,
                                                                 exception_when_none=True,
                                                                 message_exception=f"Not found model with id {obj_id}")

    def create(self, obj: CreateModel):
        inserted = self.collection.insert_one(obj.model_dump(by_alias=True, exclude={"id"}))
        return self.aggregate({"$match": {"_id": inserted.inserted_id}})

    def update(self, obj_id: str, obj: UpdateModel):
        if hasattr(obj, "_id"):
            obj._id = None

        # remove attr is None of obj
        obj = obj.dict(exclude_none=True)

        result = self.collection.update_one({"_id": ObjectId(obj_id)}, {"$set": obj})

        if result.modified_count == 0:
            raise Exception("Không có bản ghi nào được cập nhật")

        return result

    def delete(self, obj_id: str):
        result = self.collection.delete_one({"_id": ObjectId(obj_id)})
        if result.deleted_count == 0:
            raise Exception("Không có bản ghi nào được xóa")
        return result
