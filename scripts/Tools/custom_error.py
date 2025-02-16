# Description: Custom error classes for the project

class CustomException:
    """
    A custom exception class for the project.
    """
    title: str
    msg: str
    error: Exception

    def __init__(self, title: str, msg: str, error: Exception):
        """
        Initialize the CustomException class.

        :param title: The title of the error.
            :type title: str
        :param msg: The message of the error.
            :type msg: str
        :param error: The exception object.
            :type error: Exception
        """
        self.title = title
        self.msg = msg
        self.error = error

    def raise_exception(self):
        """
        Raise the error stored in the object.

        :raises: Exception - The error stored in the object.
        """
        raise self.error

    def __dict__(self):
        """
        Return the object as a dictionary.

        :return: The object as a dictionary.
            :rtype: dict
        """
        return {"title": self.title, "msg": self.msg, "error": self.error}

    def __str__(self):
        """
        Return the object as a string.

        :return: The object as a string.
            :rtype: str
        """
        return f"{self.title}: {self.msg}"

    def __json__(self):
        """
        Return the object as a json object.

        :return: The object as a json object.
            :rtype: dict
        """
        return self.__dict__()

    def __add__(self, other):
        """
        Add another CustomException or MultiException object to this object.

        :param other: The object to add.
            :type other: CustomException | MultiException

        :return: A MultiException object that contains both objects in the case of other being a CustomException objects, or None if other is a MultiException object.
            :rtype: MultiException | None
        """
        if isinstance(other, CustomException):
            return MultiException([self, other])
        elif isinstance(other, MultiException):
            other.append(self)
            return other
        else:
            raise TypeError("Can only add CustomException or MultiException")

class MultiException:
    """
    A class to hold multiple CustomException objects.
    """
    exceptions: list[CustomException]

    def __init__(self, exceptions: list[CustomException]):
        """
        Initialize the MultiException class.

        :param exceptions: The list of CustomException objects.
            :type exceptions: list[CustomException]
        """
        self.exceptions = exceptions

    def append(self, excpt: CustomException):
        """
        Append a CustomException object to the list.

        :param excpt: The CustomException object to append.
            :type excpt: CustomException
        """
        self.exceptions.append(excpt)

    def remove(self, excpt: CustomException):
        """
        Remove a CustomException object from the list.

        :param excpt: The CustomException object to remove.
            :type excpt: CustomException

        :return: The removed CustomException object.
            :rtype: CustomException
        """
        return self.exceptions.remove(excpt)

    def pop(self, index: int):
        """
        Remove a CustomException object from the list by index.

        :param index: The index of the CustomException object to remove.
            :type index: int

        :return: The removed CustomException object.
            :rtype: CustomException
        """
        return self.exceptions.pop(index)

    def __list__(self):
        """
        Return the list of CustomException objects.

        :return: The list of CustomException objects.
            :rtype: list[CustomException
        """
        return self.exceptions

    def __subtract__(self, other: CustomException | "MultiException"):
        """
        Subtract another CustomException or MultiException object from this object.

        :param other: The object to subtract.
            :type other: CustomException | MultiException
        """
        if isinstance(other, MultiException):
            rets = []
            for excpt in other.exceptions:
                rets.append(self.exceptions.remove(excpt))
            return rets
        elif isinstance(other, CustomException):
            return self.exceptions.remove(other)

    def __json__(self):
        """
        Return the list of CustomException objects as a json object.

        :return: The list of CustomException objects as a json object.
            :rtype: list[dict]
        """
        return [excpt.__dict__() for excpt in self.exceptions]

    def __add__(self, other: CustomException | "MultiException"):
        """
        Add another CustomException or MultiException object to this object.

        :param other: The object to add.
            :type other: CustomException | MultiException
        """
        if isinstance(other, MultiException):
            self.exceptions += other.exceptions
        elif isinstance(other, CustomException):
            self.exceptions.append(other)