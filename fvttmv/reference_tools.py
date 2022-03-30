class ReferenceTools:
    illegal_chars = ["<", ">", ":", "\"", "\\", "|", "?", "*"]

    @staticmethod
    def does_contain_illegal_char(string: str):

        for char in ReferenceTools.illegal_chars:
            if char in string:
                return True

        return False
