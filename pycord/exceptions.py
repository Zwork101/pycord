class PycordError(Exception):
    pass


class PycordInternalError(PycordError):
    pass


class CannotCastTypes(PycordInternalError):
    pass


class NoContextAvailable(PycordInternalError):
    pass


class ReusedCommandName(PycordError):
    pass


class ParseError(PycordError):
    pass


class InvalidModel(PycordError):
    pass


class GatewayError(PycordError):
    pass


class AuthenticationError(PycordError):
    pass
