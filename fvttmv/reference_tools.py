from fvttmv.exceptions import FvttmvException


class ReferenceTools:
    illegal_chars = ["<", ">", ":", "\"", "\\", "|", "?", "*", " "]

    @staticmethod
    def assert_reference_is_ok(reference: str):

        if ReferenceTools.does_contain_illegal_char(reference):
            raise FvttmvException()
        if reference.startswith("/"):
            raise FvttmvException()

    @staticmethod
    def does_contain_illegal_char(reference: str):

        for char in ReferenceTools.illegal_chars:
            if char in reference:
                return True

        return False

    @staticmethod
    def create_reference_from_relative_path(path: str):
        result = path.replace("\\", "/")

        result = result.replace(" ", "%20")

        ReferenceTools.assert_reference_is_ok(result)

        return result
