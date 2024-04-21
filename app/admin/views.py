from aiohttp_apispec import request_schema, response_schema
from sqlalchemy import select
from aiohttp_session import new_session, get_session
from aiohttp.web_exceptions import HTTPForbidden
from app.admin.models import AdminModel
from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        email, password = self.data["email"], self.data["password"]
        admin: AdminModel = await self.store.admins.get_by_email(email)
        if not admin or not admin.is_password_valid(password):
            raise HTTPForbidden

        admin_data = AdminSchema().dump(admin)
        session = await new_session(request=self.request)
        session["admin"] = admin_data
        return json_response(data=admin_data)


class AdminCurrentView(AuthRequiredMixin, View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        current_user = await self.store.admins.get_by_email(self.request.admin.email)
        return json_response(data=AdminSchema().dump(current_user))
