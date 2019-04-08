import json

from linebot.__about__ import __version__
from linebot.exceptions import LineBotApiError
from linebot.http_client import HttpClient
from linebot.models import Error, Profile, MemberIds, Content, RichMenuResponse

from .http_client import AioHttpClient


class LineBotApiAsync(object):

    DEFAULT_API_ENDPOINT = "https://api.line.me"

    def __init__(
        self,
        channel_access_token,
        endpoint=DEFAULT_API_ENDPOINT,
        timeout=HttpClient.DEFAULT_TIMEOUT,
        http_client=None,
    ):
        self.endpoint = endpoint
        self.headers = {
            "Authorization": "Bearer " + channel_access_token,
            "User-Agent": "line-bot-sdk-python/" + __version__,
        }

        if http_client:
            self.http_client = http_client
        else:
            self.http_client = AioHttpClient(timeout=timeout)

    async def close(self):
        await self.http_client.close()

    async def reply_message(self, reply_token, messages, timeout=None):
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            "replyToken": reply_token,
            "messages": [message.as_json_dict() for message in messages],
        }

        await self._post(
            "/v2/bot/message/reply", data=json.dumps(data), timeout=timeout
        )

    async def push_message(self, to, messages, timeout=None):
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {"to": to, "messages": [message.as_json_dict() for message in messages]}

        await self._post("/v2/bot/message/push", data=json.dumps(data), timeout=timeout)

    async def get_rich_menu(self, rich_menu_id, timeout=None):
        response = await self._get(
            "/v2/bot/richmenu/{rich_menu_id}".format(rich_menu_id=rich_menu_id),
            timeout=timeout,
        )

        json_resp = await response.json
        return RichMenuResponse.new_from_json_dict(json_resp)

    async def delete_rich_menu(self, rich_menu_id, timeout=None):
        await self._delete(
            "/v2/bot/richmenu/{rich_menu_id}".format(rich_menu_id=rich_menu_id),
            timeout=timeout,
        )

    async def create_rich_menu(self, rich_menu, timeout=None):
        response = await self._post(
            "/v2/bot/richmenu", data=rich_menu.as_json_string(), timeout=timeout
        )

        json_resp = await response.json
        return json_resp.get("richMenuId")

    async def link_rich_menu_to_user(self, user_id, rich_menu_id, timeout=None):
        await self._post(
            "/v2/bot/user/{user_id}/richmenu/{rich_menu_id}".format(
                user_id=user_id, rich_menu_id=rich_menu_id
            ),
            timeout=timeout,
        )

    async def get_rich_menu_list(self, timeout=None):
        response = await self._get("/v2/bot/richmenu/list", timeout=timeout)

        lst_result = []
        json_resp = await response.json
        for richmenu in json_resp["richmenus"]:
            lst_result.append(RichMenuResponse.new_from_json_dict(richmenu))

        return lst_result

    async def set_rich_menu_image(
        self, rich_menu_id, content_type, content, timeout=None
    ):
        self._post(
            "/v2/bot/richmenu/{rich_menu_id}/content".format(rich_menu_id=rich_menu_id),
            data=content,
            headers={"Content-Type": content_type},
            timeout=timeout,
        )

    async def get_rich_menu_id_of_user(self, user_id, timeout=None):
        response = await self._get(
            "/v2/bot/user/{user_id}/richmenu".format(user_id=user_id), timeout=timeout
        )

        json_resp = await response.json
        return json_resp.get("richMenuId")

    async def unlink_rich_menu_from_user(self, user_id, timeout=None):
        await self._delete(
            "/v2/bot/user/{user_id}/richmenu".format(user_id=user_id), timeout=timeout
        )

    async def get_rich_menu_image(self, rich_menu_id, timeout=None):
        response = await self._get(
            "/v2/bot/richmenu/{rich_menu_id}/content".format(rich_menu_id=rich_menu_id),
            timeout=timeout,
        )

        return Content(response)

    async def multicast(self, to, messages, timeout=None):
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {"to": to, "messages": [message.as_json_dict() for message in messages]}

        await self._post(
            "/v2/bot/message/multicast", data=json.dumps(data), timeout=timeout
        )

    async def get_profile(self, user_id, timeout=None):
        response = await self._get(
            "/v2/bot/profile/{user_id}".format(user_id=user_id), timeout=timeout
        )

        json_resp = await response.json
        return Profile.new_from_json_dict(json_resp)

    async def get_group_member_profile(self, group_id, user_id, timeout=None):
        response = await self._get(
            "/v2/bot/group/{group_id}/member/{user_id}".format(
                group_id=group_id, user_id=user_id
            ),
            timeout=timeout,
        )

        json_resp = await response.json
        return Profile.new_from_json_dict(json_resp)

    async def get_room_member_profile(self, room_id, user_id, timeout=None):
        response = await self._get(
            "/v2/bot/room/{room_id}/member/{user_id}".format(
                room_id=room_id, user_id=user_id
            ),
            timeout=timeout,
        )

        json_resp = await response.json
        return Profile.new_from_json_dict(json_resp)

    async def get_group_member_ids(self, group_id, start=None, timeout=None):
        params = None if start is None else {"start": start}

        response = await self._get(
            "/v2/bot/group/{group_id}/members/ids".format(group_id=group_id),
            params=params,
            timeout=timeout,
        )

        json_resp = await response.json
        return MemberIds.new_from_json_dict(json_resp)

    async def get_room_member_ids(self, room_id, start=None, timeout=None):
        params = None if start is None else {"start": start}

        response = await self._get(
            "/v2/bot/room/{room_id}/members/ids".format(room_id=room_id),
            params=params,
            timeout=timeout,
        )

        json_resp = await response.json
        return MemberIds.new_from_json_dict(json_resp)

    async def get_message_content(self, message_id, timeout=None):
        response = await self._get(
            "/v2/bot/message/{message_id}/content".format(message_id=message_id),
            stream=True,
            timeout=timeout,
        )

        return Content(response)

    async def leave_group(self, group_id, timeout=None):
        await self._post(
            "/v2/bot/group/{group_id}/leave".format(group_id=group_id), timeout=timeout
        )

    async def leave_room(self, room_id, timeout=None):
        await self._post(
            "/v2/bot/room/{room_id}/leave".format(room_id=room_id), timeout=timeout
        )

    async def _get(self, path, params=None, headers=None, stream=False, timeout=None):
        url = self.endpoint + path

        if headers is None:
            headers = {}
        headers.update(self.headers)

        response = await self.http_client.get(
            url, headers=headers, params=params, stream=stream, timeout=timeout
        )

        await self.__check_error(response)
        return response

    async def _post(self, path, data=None, headers=None, timeout=None):
        url = self.endpoint + path

        if headers is None:
            headers = {"Content-Type": "application/json"}
        headers.update(self.headers)

        response = await self.http_client.post(
            url, headers=headers, data=data, timeout=timeout
        )
        await self.__check_error(response)
        return response

    async def _delete(self, path, data=None, headers=None, timeout=None):
        url = self.endpoint + path

        if headers is None:
            headers = {}
        headers.update(self.headers)

        response = await self.http_client.delete(
            url, headers=headers, data=data, timeout=timeout
        )

        await self.__check_error(response)
        return response

    @staticmethod
    async def __check_error(response):
        if 200 <= response.status_code < 300:
            pass
        else:
            error = Error.new_from_json_dict((await response.json))
            raise LineBotApiError(response.status_code, error)
