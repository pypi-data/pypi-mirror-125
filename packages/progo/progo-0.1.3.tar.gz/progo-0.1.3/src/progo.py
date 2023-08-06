import attr
import atexit
import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Union
from uuid import UUID

from requests import exceptions

from ble.constants import (
    CHARACTERISTIC_WIFI_ACCESS_POINT_PASSWORD,
    CHARACTERISTIC_WIFI_ACCESS_POINT_SSID,
    CONTROL_QUERY_COMMAND_UUID,
    UTF_8,
)
from ble.util import find_gopros
from loguru import logger

from bleak import BleakClient
from bleak.backends.device import BLEDevice
import requests
from requests.exceptions import ConnectionError
from wireless import Wireless

from exceptions import NoGoprosFoundException
from params import (
    FPS,
    AutoOff,
    MaxLensMode,
    MultishotFOV,
    PhotoFOV,
    PresetGroup,
    Resolution,
    VideoFOV,
    LED,
    Toggle,
)
from settings import SETTINGS_ATTR_INT_MAP, CameraSettings
from status import CameraStatus


OPEN_GOPRO_BASE_URL = "http://10.5.5.9:8080/gopro"
BASE_MEDIA_PATH = Path("100GOPRO/")


def update_state(func):
    def wrap(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self._update_progo_state()
        return result

    return wrap


def run_async_function_synchronously(async_func: Callable, *args, **kwargs):
    """Because I want to use `bleak` but actively don't care about async."""
    coroutine = async_func(*args, **kwargs)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)


def get_gopro(id: str = None) -> BLEDevice:
    gopros = run_async_function_synchronously(find_gopros)
    if not gopros:
        raise NoGoprosFoundException(
            "No Gopros found! Please set 'Wireless Connections' to 'On' or get closer to your camera."
        )
    if id:
        logger.debug(f"Discovering gopro {id}")
        for gopro in gopros:
            if id == gopro.name[-4:]:
                logger.debug(f"Found gopro {id}")
                return gopro
    return gopros[0]


class Progo:
    def __init__(self, gopro_id: str = None) -> None:
        self._gopro_id: str = gopro_id
        self._gopro: BLEDevice = None
        self._ble_client: BleakClient = None
        self._wireless = Wireless()
        self._open_gopro_base_url = OPEN_GOPRO_BASE_URL
        self._media_path = BASE_MEDIA_PATH
        self.status = None
        self.settings = None
        atexit.register(self._adios)

    def _adios(self):
        logger.debug("Disconnecting ble client")
        if self._ble_client:
            run_async_function_synchronously(self._ble_client.disconnect)

    def _ensure_ble_connection(self):
        logger.debug("Ensuring BLE connection")
        connected = self._ble_client.is_connected
        while not connected:
            logger.debug("BLE client not connected - connecting")
            connected = run_async_function_synchronously(self._ble_client.connect)
        logger.debug("BLE client connected")

    def _write_ble_gatt_char(self, char_uuid: Union[str, UUID], cmd: int):
        data = bytearray([cmd])
        data.insert(0, len(data))
        self._ensure_ble_connection()
        logger.debug(f"Writing data {data} to {char_uuid}")
        return run_async_function_synchronously(
            self._ble_client.write_gatt_char, char_uuid, data
        )

    def _write_ble_gatt_char_with_param(
        self, char_uuid: Union[str, UUID], cmd: int, param: int
    ):
        data = bytearray([cmd])
        param = bytearray([param])
        data.extend([len(param), *param])
        data.insert(0, len(data))
        self._ensure_ble_connection()
        logger.debug(f"Writing data {data} to {char_uuid}")
        return run_async_function_synchronously(
            self._ble_client.write_gatt_char, char_uuid, data
        )

    def _http_get(self, url: str):
        url = f"{self._open_gopro_base_url}/{url}"
        response = requests.get(url, stream=True)
        return response

    def _get_json(self, url: str):
        response = self._http_get(url)
        return response.json()

    # BLE commands

    def power_down(self):
        logger.debug("Powering down camera")
        return self._write_ble_gatt_char(CONTROL_QUERY_COMMAND_UUID, 0x04)

    def sleep(self):
        logger.debug("Putting camera into standby")
        return self._write_ble_gatt_char(CONTROL_QUERY_COMMAND_UUID, 0x05)

    def enable_wifi_ap(self):
        logger.debug("Enabling wifi access point")
        return self._write_ble_gatt_char_with_param(
            CONTROL_QUERY_COMMAND_UUID, 0x17, Toggle.ON.value
        )

    def disable_wifi_ap(self):
        logger.debug("Disabling wifi access point")
        return self._write_ble_gatt_char_with_param(
            CONTROL_QUERY_COMMAND_UUID, 0x17, Toggle.OFF.value
        )

    def get_wifi_ssid(self):
        logger.debug("Getting wifi ssid")
        ssid = run_async_function_synchronously(
            self._ble_client.read_gatt_char, CHARACTERISTIC_WIFI_ACCESS_POINT_SSID
        )
        return ssid.decode(UTF_8)

    def get_wifi_password(self):
        logger.debug("Getting wifi password")
        password = run_async_function_synchronously(
            self._ble_client.read_gatt_char, CHARACTERISTIC_WIFI_ACCESS_POINT_PASSWORD
        )
        return password.decode(UTF_8)

    # Wifi commands

    @update_state
    def set_third_party_client_info(self):
        # 2.0 only
        return self._get_json("camera/analytics/set_client_info")

    @update_state
    def start_encoding(self):
        # 2.0 only
        return self._http_get("camera/shutter/start")

    @update_state
    def set_shutter_on(self):
        # 2.0 only
        return self.start_encoding()

    @update_state
    def stop_encoding(self):
        # 2.0 only
        return self._http_get("camera/shutter/stop")

    def set_shutter_off(self):
        # 2.0 only
        return self.stop_encoding()

    @update_state
    def set_digital_zoom(self, zoom_percent: int):
        return self._get_json(f"camera/digital_zoom?percent={zoom_percent}")

    def get_camera_state(self):
        return self._get_json("camera/state")

    def set_keep_alive(self):
        return self._get_json("camera/keep_alive")

    def get_media_list(self):
        return self._get_json("media/list")

    def download_file(self):
        pass

    def get_gpmf_data(self, filename: Path):
        response = self._http_get(f"media/gpmf?path={self._media_path.join(filename)}")
        # FIXME! Write response.data to a file locally

    def get_media_info(self, filename: Path):
        return self._http_get(f"media/info?path={self._media_path.join(filename)}")

    def get_screennail(self, filename: str):
        response = self._http_get(
            f"media/screennail?path{self._media_path.join(filename)}"
        )
        # FIXME! Write response.data to a file locally

    def get_thumbnail(self, filename: str):
        response = self._http_get(
            f"media/thumbnail?path={self._media_path.join(filename)}"
        )
        # FIXME! Write response.data to a file locally

    def get_telemetry(self, filename: str):
        response = self._http_get(
            f"media/telemetry?path={self._media_path.join(filename)}"
        )
        # FIXME! Write response.data to a file locally

    def get_open_gopro_api_version(self):
        return self._get_json("version")

    def get_preset_status(self):
        return self._get_json("camera/presets/get")

    @update_state
    def set_preset(self, preset: int) -> dict:
        resp = self._get_json(f"camera/presets/load?id={preset}")
        return resp

    @update_state
    def set_preset_group(self, preset_group: PresetGroup) -> dict:
        return self._get_json(f"camera/presets/set_group?id={preset_group.value}")

    @update_state
    def start_preview_stream(self):
        return self._get_json("camera/stream/start")

    @update_state
    def stop_preview_stream(self):
        return self._get_json("camera/stream/stop")

    @update_state
    def enable_turbo_mode(self):
        return self._get_json(f"media/turbo_transfer?p={Toggle.ON.value}")

    @update_state
    def disable_turbo_mode(self):
        return self._get_json(f"media/turbo_transfer?p={Toggle.OFF.value}")

    @update_state
    def _update_camera_setting(self, setting: int, option: int):
        return self._get_json(f"camera/setting?setting={setting}&option={option}")

    def set_resolution(self, resolution: Resolution):
        resolution_id = SETTINGS_ATTR_INT_MAP["resolution"]
        return self._update_camera_setting(resolution_id, resolution.value)

    def set_fps(self, fps: FPS):
        fps_id = SETTINGS_ATTR_INT_MAP["fps"]
        return self._update_camera_setting(fps_id, fps.value)

    def set_auto_off(self, auto_off: AutoOff):
        auto_off_id = SETTINGS_ATTR_INT_MAP["auto_off"]
        return self._update_camera_setting(auto_off_id, auto_off.value)

    def set_led(self, led: LED):
        led_id = SETTINGS_ATTR_INT_MAP["led"]
        return self._update_camera_setting(led_id, led.value)

    def set_video_fov(self, fov: VideoFOV):
        video_fov_id = SETTINGS_ATTR_INT_MAP["video_fov"]
        return self._update_camera_setting(video_fov_id, fov.value)

    def set_photo_fov(self, fov: PhotoFOV):
        photo_fov_id = SETTINGS_ATTR_INT_MAP["photo_fov"]
        return self._update_camera_setting(photo_fov_id, fov.value)

    def set_multi_shot_fov(self, fov: MultishotFOV):
        multi_shot_fov_id = SETTINGS_ATTR_INT_MAP["multi_shot_fov"]
        return self._update_camera_setting(multi_shot_fov_id, fov.value)

    def set_max_lens_mode(self, max_lens_mode: MaxLensMode):
        max_lens_mode_id = SETTINGS_ATTR_INT_MAP["max_lens_mode"]
        return self._update_camera_setting(max_lens_mode_id, max_lens_mode.value)

    # General

    def connect_to_wifi_ap(self):
        logger.info("Connecting to wap")
        connection_attempt = 1
        connected = False
        while not connected:
            logger.debug(f"WAP connection attempt {connection_attempt}")
            connected = self._wireless.connect(
                ssid=self.get_wifi_ssid(), password=self.get_wifi_password()
            )
            connection_attempt += 1
        return connected

    def _update_progo_state(self) -> bool:
        max_attempts = 100
        state_set = False
        attempt_num = 1
        while not state_set and attempt_num <= max_attempts:
            try:
                state = self.get_camera_state()
                self.settings = CameraSettings.from_dict(state["settings"])
                self.status = CameraStatus.from_dict(state["status"])
                state_set = True
            except ConnectionError:
                attempt_num += 1
        return state_set

    def initialize(self):
        logger.info("Initializing progo")
        self._gopro = get_gopro(self._gopro_id)
        self._gopro_id = self._gopro.name[-4:]
        self._ble_client = BleakClient(self._gopro)
        self._ensure_ble_connection()
        self.enable_wifi_ap()
        self.connect_to_wifi_ap()
        self._update_progo_state()
        logger.info("Progo initialized")
