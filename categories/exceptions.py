class WorkflowException(Exception):
    pass


class ShareContractCannotBeAccepted(WorkflowException):
    pass


class ShareContractCannotBeDeclined(WorkflowException):
    pass


class ShareContractCannotBeRevoked(WorkflowException):
    pass


class ShareContractAlreadyRevoked(WorkflowException):
    pass


class ShareContractUserIsOwner(WorkflowException):
    pass


class ShareContractAlreadyExists(WorkflowException):
    pass


class ShareContractUserDoesNotExist(WorkflowException):
    pass
