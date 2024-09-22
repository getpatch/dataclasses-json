import dataclasses
import sys

import pytest
import dataclasses_json


@dataclasses_json.dataclass_json(on_error=dataclasses_json.OnError.GROUP_AND_RAISE,
                                 undefined=dataclasses_json.Undefined.RAISE)
@dataclasses.dataclass
class DataClass(dataclasses_json.DataClassJsonMixin):
    a: int
    b: str


@pytest.mark.skipif(sys.version_info < (3, 11), reason="Only Python 3.9+")
class TestGroupAndRaise:

    def test_metadata(self):
        assert getattr(DataClass, "dataclass_json_config")["on_error"] == dataclasses_json.OnError.GROUP_AND_RAISE

    def test_success(self):
        DataClass.from_dict({"a": 1, "b": "test"})

    def test_failure_single(self):
        with pytest.raises(ExceptionGroup) as exc_info:
            DataClass.from_dict({"a": 1})
        assert len(exc_info.value.exceptions) == 1

    def test_failure_double(self):
        with pytest.raises(ExceptionGroup) as exc_info:
            DataClass.from_dict({})
        assert len(exc_info.value.exceptions) == 2
