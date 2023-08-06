from __future__ import annotations

import asyncio
import json
import logging
import socket
from dataclasses import dataclass
from typing import Any, Callable, Dict

import aiohttp
import async_timeout
import backoff
from requests import Session
from signalrcore_async.hub.auth_hub_connection import AuthHubConnection
from signalrcore_async.hub.base_hub_connection import BaseHubConnection
from signalrcore_async.hub_connection_builder import HubConnectionBuilder
from yarl import URL

from .exceptions import (
    GlimmrConnectionError,
    GlimmrRConnectionTimeoutError,
    GlimmrEmptyResponseError,
    GlimmrError,
)
from .models import SystemData

@dataclass
class Glimmr:
    """Main class for handling connections with GLIMMR."""

    host: str
    request_timeout: float = 8.0
    session: aiohttp.ClientSession | None = None
    _client: AuthHubConnection | BaseHubConnection | None = None
    _close_session: bool = False
    device: SystemData | None = None
    _connected: bool = False
    LOGGER = logging.getLogger(__name__)

    @property
    def connected(self) -> bool:
        """Return if we are connect to the WebSocket of a GLIMMR device.

        Returns:
            True if we are connected to the WebSocket of a GLIMMR device,
            False otherwise.
        """
        return self._connected

    async def connect(self) -> None:
        """Connect to the WebSocket of a GLIMMR device.

        Raises:
            GLIMMRError: The configured GLIMMR device, does not support WebSocket
                communications.
            GLIMMRConnectionError: Error occurred while communicating with
                the GLIMMR device via the WebSocket.
        """
        if self.connected:
            self.LOGGER.debug("Already connected.")
            return

        if not self.device:
            self.LOGGER.debug("Updating device info?")
            await self.update()

        with Session():
            url = "http://" + self.host + "/socket"
            self.LOGGER.debug("Connecting to url: " + url)
            connection = HubConnectionBuilder() \
                .with_url(url) \
                .build()
            self.LOGGER.debug("Connected...")
            if not self.session or not self.device:
                self.LOGGER.debug("Unsupported session or device?")
                raise GlimmrError(
                    "The Glimmr device at {self.host} does not support WebSockets"
                )

            try:
                self.LOGGER.debug("Setting client.")
                self._client = connection
                self.LOGGER.debug("Starting connection.")
                # start a connection
                await connection.start()
                self.LOGGER.debug("Connected!")
                self._connected = True
                connection.on('olo', self.olo)
                self.LOGGER.debug("OLO!")
                connection.on('mode', self.dev_mode)
                self.LOGGER.debug("MODE!")
            except (

            ) as exception:
                self._connected = False
                self.LOGGER.debug("Glimmr con exception...")
                raise GlimmrConnectionError(
                    "Error occurred while communicating with GLIMMR device"
                    f" on WebSocket at {self.host}"
                ) from exception

    def olo(self, data):
        self.device = SystemData.from_dict(data)
        self.LOGGER.debug("DEVICE: ", self.device)

    def dev_mode(self, mode):
        if self.device is not None:
            self.device.device_mode = mode

    async def disconnect(self) -> None:
        """Disconnect from the WebSocket of a GLIMMR device."""
        if not self._client or not self.connected:
            return

        await self._client.stop()
        self._connected = False

    def add_callback(self, method: str, callback: Callable[[SystemData], None]):
        if self._client is not None:
            self.LOGGER.debug("Adding callback for " + method)
            self._client.on(method, callback)
        else:
            self.LOGGER.debug("Client is not set!")

    @backoff.on_exception(backoff.expo, GlimmrConnectionError, max_tries=3, logger=None)
    async def request(
            self,
            uri: str = "",
            method: str = "GET",
            data: int | str | Dict[str, any] | None = None,
    ) -> Any:
        """Handle a request to a Glimmr device.

        A generic method for sending/handling HTTP requests done gainst
        the GLIMMR device.

        Args:
            uri: Request URI, for example `/json/si`.
            method: HTTP method to use for the request.E.g., "GET" or "POST".
            data: Integer, string, or SystemData object to send to the endpoint.

        Returns:
            A Python dictionary (JSON decoded) with the response from the
            GLIMMR device.

        Raises:
            GLIMMRConnectionError: An error occurred while communitcation with
                the GLIMMR device.
            GLIMMRConnectionTimeoutError: A timeout occurred while communicating
                with the GLIMMR device.
            GLIMMRError: Received an unexpected response from the GLIMMR device.
        """
        path = "/api/Glimmr/" + uri
        self.LOGGER.debug("Path: " + path)
        url = URL.build(scheme="http", host=self.host, port=80, path=path)
        self.LOGGER.debug("URL: %s", url)
        headers = {
            "Accept": "application/json, text/plain, */*",
        }

        if self.session is None:
            self.LOGGER.debug("Setting session...")
            self.session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                self.LOGGER.debug("Awaiting response...")
                response = await self.session.request(
                    method,
                    url,
                    json=data,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            self.LOGGER.debug("Timeout...")
            raise GlimmrRConnectionTimeoutError(
                f"Timeout occurred while connecting to GLIMMR device at {self.host}"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            self.LOGGER.debug("Connection error...")
            raise GlimmrConnectionError(
                f"Error occurred while communicating with GLIMMR device at {self.host}"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if (response.status // 100) in [4, 5]:
            self.LOGGER.debug("Reading response...")
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise GlimmrError(response.status, json.loads(contents.decode("utf8")))
            raise GlimmrError(response.status, {"message": contents.decode("utf8")})

        if "application/json" in content_type:
            self.LOGGER.debug("Reading json?")
            response_data = await response.json()
            if (
                    method == "POST"
                    and uri == "systemData"
                    and self.device is not None
                    and data is not None
            ):
                self.device.from_dict(data={"glimmr_data": response_data})
            return response_data
        self.LOGGER.debug("Returning response text...")
        return await response.text()

    @backoff.on_exception(
        backoff.expo, GlimmrEmptyResponseError, max_tries=3, logger=None
    )
    async def update(self) -> SystemData:
        """Get all information about the device in a single call.

        This method updates all GLIMMR information available with a single API
        call.

        Returns:
            GLIMMR Device data.

        Raises:
            GLIMMREmptyResponseError: The GLIMMR device returned an empty response.
        """
        self.LOGGER.debug("Updating")
        data = await self.request("")
        if not data:
            self.LOGGER.debug("Error fetching data...")
            raise GlimmrEmptyResponseError(
                f"GLIMMR device at {self.host} returned an empty API"
                " response on full update"
            )

        sd = SystemData.from_dict(data)
        self.device = sd
        self.LOGGER.debug("Updating scenes.")
        await self.update_scenes()
        self.LOGGER.debug("Scene updated, returning.")
        return self.device

    async def update_scenes(self) -> {}:
        scenes = await self.request("ambientScenes")
        self.LOGGER.debug("Scenes: ", scenes)
        if scenes:
            await self.device.load_scenes(scenes)
        return self.device.scenes

    async def master(
            self
    ):
        """Change master glimmr_data of a GLIMMR Light device.

        Args:
        """
        if self.device is None:
            await self.update()

        if self.device is None:
            raise GlimmrError("Unable to communicate with GLIMMR to get the current glimmr_data")

    async def mode(self, mode: int) -> None:
        """Set the default transition time for manual control.

        Args:
            mode: New target device mode.
        """
        await self.request(
            "mode", method="POST", data=mode
        )

    async def ambient_scene(self, scene: int) -> None:
        """Update the ambient scene.
        Args:
            scene: Scene ID to change to.
        """
        if scene < -1:
            mode = 0
            if scene == -2:
                mode = 1
            if scene == -3:
                mode = 2
            if scene == -4:
                mode = 3
            if scene == -5:
                mode = 4
            if scene == -6:
                mode = 5
            await self.request("ambientScene", method="POST", data=mode)
        else:
            await self.request(
                "ambientScene", method="POST", data=scene
            )

    async def ambient_color(self, color: str) -> None:
        """Update the ambient scene.
        Args:
            color: Ambient color to set.
        """
        self.LOGGER.debug("Setting ambient color: " + color)
        await self.request(
            "ambientColor", method="POST", data=color
        )

    async def reset(self) -> None:
        """Reboot GLIMMR device."""
        self.LOGGER.debug("Reboot requested.")
        await self.request("systemControl", method="POST", data="reboot")

    async def close(self) -> None:
        """Close open client (WebSocket) session."""
        await self.disconnect()
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Glimmr:
        """Async enter.

        Returns:
            The GLIMMR object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()

    async def set(self, device: SystemData):
        self.LOGGER.debug("Updating sd object.")
        await self.request("systemData", method="POST", data=device.to_dict())

    def set_logger(self, logger):
        self.LOGGER = logger
