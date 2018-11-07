class PycordError(Exception):
    pass


class PycordInternalError(PycordError):
    pass


class CannotCastTypes(PycordInternalError):
    pass


class ReusedCommandName(PycordError):
    pass


class ParseError(PycordError):
    pass
