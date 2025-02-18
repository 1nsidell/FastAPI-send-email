from fastapi import APIRouter, Header

from src.app.depends.providers_depends import APIAccessProvider
from src.app.depends.use_cases_depends import EmailUseCase
from src.core.schemas import SSendTokenEmail, SSuccessfulRequest
from src.settings import settings


class SendEmailConfirm:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.send_confirm_email,
            self.send_confirm_email,
            methods=["POST"],
            response_model=SSuccessfulRequest,
        )

    async def send_confirm_email(
        self,
        EmailUseCase: EmailUseCase,
        api_access: APIAccessProvider,
        data: SSendTokenEmail,
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SSuccessfulRequest:
        await api_access.check_api_key(api_key)
        return await EmailUseCase.send_confirm_email(
            data.recipient, data.token
        )


email_confirm = SendEmailConfirm()

router = email_confirm.router
