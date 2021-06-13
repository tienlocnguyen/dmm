from typing import cast, Any, TypeVar

from .v86d.controller import V86DController

from dmm.controller import DMMControllerBase

controller_mapping = {"v86d": V86DController}


class DMMController(DMMControllerBase):
    def __new__(  # type: ignore
        cls: "DMMController", device_type: str, *args: Any, **kwargs: Any
    ) -> DMMControllerBase:
        device_cls = controller_mapping[device_type]

        controller = device_cls.__new__(*args, **kwargs)

        return cast(DMMControllerBase, controller)
