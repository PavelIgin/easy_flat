import typing


class MockSMTP_SSL:
    """
    Mock object for smtplib.SMTP_SSL
    """

    def __init__(self) -> None:
        super().__init__()

    def __enter__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self

    def __exit__(
        self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any
    ) -> None:
        pass

    def login(self, email: typing.AnyStr, passsword: typing.AnyStr) -> None:
        pass


class MockSMTPSSLSuccess(MockSMTP_SSL):
    def sendmail(self, *args: typing.Any, **kwargs: typing.Any) -> int:
        return 1


class MockSMTPSSLError(MockSMTP_SSL):
    def sendmail(self, *args: typing.Any, **kwargs: typing.Any) -> Exception:
        raise KeyError("Exception")


class MockSMTPSSLFail(MockSMTP_SSL):
    def sendmail(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        return
