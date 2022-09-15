from enum import Enum, auto


class SuccessCode(Enum):
    GET_SUCCESS = auto()
    SET_SUCCESS = auto()
    DELETE_SUCCESS = auto()


class FailCode(Enum):
    KEY_NOT_FOUND = auto()
    SAVE_LOCAL_FAIL = auto()
    UPLOAD_S3_FAIL = auto()
    DELETE_FAIL = auto()
