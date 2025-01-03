import os
import sys
import time
import requests
import re
from colorama import Fore, Back, Style
from datetime import datetime, timedelta, timezone

user_default = "hocmai"
password_default = "Hocmai@1234"
time_default = "18:00 - 18:30, 18:35 - 19:05, 19:10 - 19:40, 19:45 - 20:15, 20:20 - 20:50, 20:55 - 21:25, 21:30 - 22:00"
credit_cost_default = 20
ca_default = 10


token = ""
headers = {}
api_login = "https://sso.hocmai.com/auth/realms/hocmai/protocol/openid-connect/token"
api_pro = "https://api-scheduling.hocmai.net/users/profile"
api_shifts_search = "https://api-scheduling.hocmai.net/shifts/search"
api_schedule_shifts = "https://api-scheduling.hocmai.net/schedule-shift"
data = [
    {
        "id": 2388,
        "fromDate": "2022-06-26T01:25:54.412846Z",
        "toDate": "2022-06-26T01:55:54.412854Z",
        "days": [
            "WEDNESDAY",
            "THURSDAY",
            "SATURDAY",
            "MONDAY",
            "SUNDAY",
            "TUESDAY",
            "FRIDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:54.412940Z",
        "createBy": "class_in",
        "updateDate": None,
        "updateBy": "longnb",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2594,
        "fromDate": "2024-05-28T01:30:00.717Z",
        "toDate": "2024-05-28T02:15:00.717Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T03:42:07.638747Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2405,
        "fromDate": "2022-06-26T01:30:54.465075Z",
        "toDate": "2022-06-26T03:00:54.465080Z",
        "days": [
            "FRIDAY",
            "WEDNESDAY",
            "TUESDAY",
            "SATURDAY",
            "THURSDAY",
            "MONDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:54.465169Z",
        "createBy": "class_in",
        "updateDate": None,
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1673,
        "fromDate": "2022-05-22T02:00:09.544253Z",
        "toDate": "2022-05-22T03:00:09.544Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:09.544694Z",
        "createBy": "class_in",
        "updateDate": "2024-05-06T03:21:23.221185Z",
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2435,
        "fromDate": "2022-06-26T02:00:54.578145Z",
        "toDate": "2022-06-26T02:30:54.578151Z",
        "days": [
            "MONDAY",
            "SATURDAY",
            "TUESDAY",
            "FRIDAY",
            "THURSDAY",
            "WEDNESDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:54.578238Z",
        "createBy": "class_in",
        "updateDate": None,
        "updateBy": "longnb",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2595,
        "fromDate": "2024-05-28T02:20:00.207Z",
        "toDate": "2024-05-28T03:05:00.207Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T03:45:19.127880Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2607,
        "fromDate": "2024-06-01T02:30:00.050Z",
        "toDate": "2024-06-01T03:15:00.050Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-06-01T03:53:45.802032Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1812,
        "fromDate": "2022-05-22T02:35:10.140422Z",
        "toDate": "2022-05-22T03:05:10.140Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:10.140644Z",
        "createBy": "class_in",
        "updateDate": "2022-05-22T10:57:25.749260Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1854,
        "fromDate": "2022-05-23T03:10:00Z",
        "toDate": "2022-05-23T04:10:00Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-23T08:07:05.452038Z",
        "createBy": "system",
        "updateDate": "2024-05-06T03:21:46.499056Z",
        "updateBy": "lienpt",
        "canBeRemoved": False,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2596,
        "fromDate": "2024-05-28T03:10:00.210Z",
        "toDate": "2024-05-28T03:55:00.210Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T03:59:09.043373Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1622,
        "fromDate": "2022-05-22T03:10:09.366298Z",
        "toDate": "2022-05-22T03:40:09.366Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:09.366490Z",
        "createBy": "class_in",
        "updateDate": "2022-05-22T10:57:54.245946Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2027,
        "fromDate": "2022-06-26T03:15:53.003069Z",
        "toDate": "2022-06-26T04:45:53.003084Z",
        "days": [
            "FRIDAY",
            "WEDNESDAY",
            "TUESDAY",
            "SATURDAY",
            "THURSDAY",
            "MONDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:53.003288Z",
        "createBy": "class_in",
        "updateDate": None,
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1334,
        "fromDate": "2022-05-22T03:45:08.228934Z",
        "toDate": "2022-05-22T04:15:08.228Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:08.229516Z",
        "createBy": "class_in",
        "updateDate": "2022-05-22T10:58:19.734845Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2597,
        "fromDate": "2024-05-28T04:00:00.483Z",
        "toDate": "2024-05-28T04:45:00.483Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:00:20.335747Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2463,
        "fromDate": "2022-06-26T06:25:54.671639Z",
        "toDate": "2022-06-26T06:55:54.671Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:54.671720Z",
        "createBy": "class_in",
        "updateDate": "2022-08-11T10:33:12.954293Z",
        "updateBy": "longnb",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1260,
        "fromDate": "2022-05-04T07:00:00.179Z",
        "toDate": "2022-05-04T07:30:00.179Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-04T09:30:40.340343Z",
        "createBy": "system",
        "updateDate": "2022-05-04T09:32:53.989424Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2598,
        "fromDate": "2024-05-28T07:00:00.460Z",
        "toDate": "2024-05-28T07:45:00.460Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:01:12.245735Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1810,
        "fromDate": "2022-05-22T07:00:10.130414Z",
        "toDate": "2022-05-22T08:00:10.130Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:10.130723Z",
        "createBy": "class_in",
        "updateDate": "2024-05-06T03:22:40.337042Z",
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2189,
        "fromDate": "2022-06-26T07:00:53.609974Z",
        "toDate": "2022-06-26T08:30:53.609980Z",
        "days": [
            "FRIDAY",
            "WEDNESDAY",
            "TUESDAY",
            "SATURDAY",
            "THURSDAY",
            "MONDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:53.610110Z",
        "createBy": "class_in",
        "updateDate": None,
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1289,
        "fromDate": "2022-05-22T07:35:07.992818Z",
        "toDate": "2022-05-22T08:05:07.992Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:07.993225Z",
        "createBy": "class_in",
        "updateDate": "2022-05-22T10:59:13.951872Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2608,
        "fromDate": "2024-06-01T07:45:00.519Z",
        "toDate": "2024-06-01T08:30:00.519Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-06-01T03:54:12.747417Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2599,
        "fromDate": "2024-05-28T07:50:00Z",
        "toDate": "2024-05-28T08:35:00Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:08:01.982629Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1518,
        "fromDate": "2022-05-22T08:10:08.959463Z",
        "toDate": "2022-05-22T09:10:08.959Z",
        "days": [
            "WEDNESDAY",
            "SUNDAY",
            "MONDAY",
            "TUESDAY",
            "SATURDAY",
            "FRIDAY",
            "THURSDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:08.959777Z",
        "createBy": "class_in",
        "updateDate": "2022-08-08T04:32:31.394351Z",
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [{"id": 38, "code": "SNP112", "name": "SOL - GV Nam Phi 1:12"}],
    },
    {
        "id": 1519,
        "fromDate": "2022-05-22T08:10:08.963650Z",
        "toDate": "2022-05-22T08:40:08.963Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:08.963920Z",
        "createBy": "class_in",
        "updateDate": "2022-05-22T10:59:32.608802Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2600,
        "fromDate": "2024-05-28T08:40:00.186Z",
        "toDate": "2024-05-28T09:25:00.186Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:09:06.904809Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1657,
        "fromDate": "2022-05-22T08:45:09.490481Z",
        "toDate": "2022-05-22T09:15:09.490Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:09.490660Z",
        "createBy": "class_in",
        "updateDate": "2022-05-22T10:59:53.157407Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1942,
        "fromDate": "2022-06-26T08:45:52.673203Z",
        "toDate": "2022-06-26T10:15:52.673Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:52.673456Z",
        "createBy": "class_in",
        "updateDate": "2024-05-28T04:18:57.185410Z",
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1261,
        "fromDate": "2022-05-04T09:20:00Z",
        "toDate": "2022-05-04T09:50:00Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-04T09:31:57.728691Z",
        "createBy": "system",
        "updateDate": "2022-05-04T09:33:14.655043Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1688,
        "fromDate": "2022-05-22T09:20:09.625340Z",
        "toDate": "2022-05-22T10:20:09.625Z",
        "days": ["SATURDAY", "SUNDAY"],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:09.625540Z",
        "createBy": "class_in",
        "updateDate": "2023-12-09T04:12:19.878738Z",
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [{"id": 38, "code": "SNP112", "name": "SOL - GV Nam Phi 1:12"}],
    },
    {
        "id": 2601,
        "fromDate": "2024-05-28T09:30:00.915Z",
        "toDate": "2024-05-28T10:15:00.915Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:10:12.243231Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1852,
        "fromDate": "2022-05-22T09:55:10.317857Z",
        "toDate": "2022-05-22T10:25:10.317Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:10.318028Z",
        "createBy": "class_in",
        "updateDate": "2022-05-22T11:00:30.209550Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2512,
        "fromDate": "2022-06-26T10:15:54.836686Z",
        "toDate": "2022-06-26T11:45:54.836Z",
        "days": ["WEDNESDAY"],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:54.836785Z",
        "createBy": "class_in",
        "updateDate": "2024-12-16T08:03:56.466734Z",
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1305,
        "fromDate": "2022-05-22T10:25:08.083Z",
        "toDate": "2022-05-22T10:55:08.083Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:08.084007Z",
        "createBy": "class_in",
        "updateDate": "2024-10-07T07:44:52.036991Z",
        "updateBy": "hocmai",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2609,
        "fromDate": "2024-06-01T10:45:00.003Z",
        "toDate": "2024-06-01T11:30:00.003Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-06-01T03:54:35.815863Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1581,
        "fromDate": "2022-05-22T11:00:09.210Z",
        "toDate": "2022-05-22T11:30:09.210Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:09.211493Z",
        "createBy": "class_in",
        "updateDate": "2022-05-23T07:53:15.672145Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1597,
        "fromDate": "2022-05-22T11:00:09.272501Z",
        "toDate": "2022-05-22T12:00:09.272Z",
        "days": [
            "TUESDAY",
            "SUNDAY",
            "FRIDAY",
            "MONDAY",
            "THURSDAY",
            "SATURDAY",
            "WEDNESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:09.272728Z",
        "createBy": "class_in",
        "updateDate": "2023-12-09T04:06:12.841658Z",
        "updateBy": "hocmai",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [{"id": 38, "code": "SNP112", "name": "SOL - GV Nam Phi 1:12"}],
    },
    {
        "id": 2498,
        "fromDate": "2022-06-26T11:00:54.794140Z",
        "toDate": "2022-06-26T11:45:54.794145Z",
        "days": [
            "SATURDAY",
            "SUNDAY",
            "MONDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:54.794229Z",
        "createBy": "class_in",
        "updateDate": None,
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2610,
        "fromDate": "2024-06-01T11:30:00.611Z",
        "toDate": "2024-06-01T12:15:00.611Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-06-01T03:55:15.594299Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1532,
        "fromDate": "2022-05-22T11:35:09.010Z",
        "toDate": "2022-05-22T12:05:09.010Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:09.010303Z",
        "createBy": "class_in",
        "updateDate": "2022-05-23T07:55:02.374470Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2606,
        "fromDate": "2024-05-28T11:45:00.018Z",
        "toDate": "2024-05-28T13:15:00.018Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:19:57.064197Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2602,
        "fromDate": "2024-05-28T11:45:00.644Z",
        "toDate": "2024-05-28T12:30:00.644Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:11:24.423399Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1303,
        "fromDate": "2022-05-22T12:10:08.075220Z",
        "toDate": "2022-05-22T13:10:08.075Z",
        "days": [
            "WEDNESDAY",
            "SUNDAY",
            "FRIDAY",
            "SATURDAY",
            "THURSDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:08.075604Z",
        "createBy": "class_in",
        "updateDate": "2022-08-08T04:39:59.547720Z",
        "updateBy": "hocmai",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [{"id": 37, "code": "SPW", "name": "SPEAKWELL"}],
    },
    {
        "id": 1530,
        "fromDate": "2022-05-22T12:10:09.003Z",
        "toDate": "2022-05-22T12:40:09.003Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:09.003740Z",
        "createBy": "class_in",
        "updateDate": "2022-05-23T07:55:40.363874Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2611,
        "fromDate": "2024-06-01T12:20:00Z",
        "toDate": "2024-06-01T13:05:00Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-06-01T03:55:34.664986Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": False,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 2603,
        "fromDate": "2024-05-28T12:35:00Z",
        "toDate": "2024-05-28T13:20:00Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:12:17.339182Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1322,
        "fromDate": "2022-05-22T12:45:08.169Z",
        "toDate": "2022-05-22T13:15:08.169Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:08.169863Z",
        "createBy": "class_in",
        "updateDate": "2022-05-23T07:50:27.370757Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1304,
        "fromDate": "2022-05-23T13:20:00Z",
        "toDate": "2022-05-23T13:50:00Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:08.079878Z",
        "createBy": "class_in",
        "updateDate": "2022-05-23T07:43:41.814567Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1342,
        "fromDate": "2022-05-22T13:20:08.265254Z",
        "toDate": "2022-05-22T14:20:08.265Z",
        "days": [
            "WEDNESDAY",
            "SUNDAY",
            "FRIDAY",
            "SATURDAY",
            "THURSDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:08.265775Z",
        "createBy": "class_in",
        "updateDate": "2024-04-20T02:38:46.693981Z",
        "updateBy": "hocmai",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [
            {"id": 37, "code": "SPW", "name": "SPEAKWELL"},
            {
                "id": 1343,
                "code": "ICCNSPW002108VN075",
                "name": "Speak Well - Starters - Size lớp 1:8 - Giáo viên Việt Nam - Số buổi 75",
            },
        ],
    },
    {
        "id": 2604,
        "fromDate": "2024-05-28T13:30:00.691Z",
        "toDate": "2024-05-28T14:15:00.691Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:12:58.984179Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1949,
        "fromDate": "2022-06-26T13:30:52.715302Z",
        "toDate": "2022-06-26T15:00:52.715324Z",
        "days": [
            "FRIDAY",
            "WEDNESDAY",
            "TUESDAY",
            "SATURDAY",
            "THURSDAY",
            "MONDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:52.715571Z",
        "createBy": "class_in",
        "updateDate": None,
        "updateBy": "lienpt",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1438,
        "fromDate": "2022-05-22T13:55:08.646Z",
        "toDate": "2022-05-22T14:25:08.646Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:08.647431Z",
        "createBy": "class_in",
        "updateDate": "2022-05-23T07:51:36.178913Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1923,
        "fromDate": "2022-06-26T14:00:52.596649Z",
        "toDate": "2022-06-26T15:00:52.596Z",
        "days": [
            "TUESDAY",
            "SUNDAY",
            "FRIDAY",
            "MONDAY",
            "THURSDAY",
            "SATURDAY",
            "WEDNESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-06-25T17:00:52.596896Z",
        "createBy": "class_in",
        "updateDate": "2023-12-09T04:08:42.650929Z",
        "updateBy": "hocmai",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [{"id": 38, "code": "SNP112", "name": "SOL - GV Nam Phi 1:12"}],
    },
    {
        "id": 2605,
        "fromDate": "2024-05-28T14:20:00Z",
        "toDate": "2024-05-28T15:05:00Z",
        "days": [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2024-05-28T04:13:51.790092Z",
        "createBy": "lienpt",
        "updateDate": None,
        "updateBy": None,
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1612,
        "fromDate": "2022-05-22T14:30:09.326Z",
        "toDate": "2022-05-22T15:00:09.326Z",
        "days": [
            "THURSDAY",
            "FRIDAY",
            "WEDNESDAY",
            "SUNDAY",
            "SATURDAY",
            "MONDAY",
            "TUESDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:09.326703Z",
        "createBy": "class_in",
        "updateDate": "2022-05-23T07:54:23.104306Z",
        "updateBy": "system",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
    {
        "id": 1808,
        "fromDate": "2022-05-23T15:05:00Z",
        "toDate": "2022-05-23T15:35:00Z",
        "days": [
            "THURSDAY",
            "SUNDAY",
            "TUESDAY",
            "FRIDAY",
            "WEDNESDAY",
            "MONDAY",
            "SATURDAY",
        ],
        "status": "ACTIVE",
        "maintenance": False,
        "credit": 1,
        "createDate": "2022-05-22T07:17:10.118037Z",
        "createBy": "class_in",
        "updateDate": "2022-05-23T07:59:20.256517Z",
        "updateBy": "longnb",
        "canBeRemoved": True,
        "canBeUpdate": None,
        "products": [],
    },
]


def display_menu():
    os.system("cls" if os.name == "nt" else "clear")
    print("********Học mãi tool kit ********")
    print("Tài khoản: ", user_default)
    print("Mật khẩu: ", password_default)
    print("Thời gian: ", time_default)
    print("Credit cost: ", credit_cost_default)
    print("CA: ", ca_default)
    print("*********************************")
    print("Chọn một tùy chọn:")
    print("1. Chạy ứng dụng với cài đặt ở trên")
    print("2. Cài đặt")
    print("3. Cập nhật dữ liệu")
    print("4. Thoát")

    print()


def get_input(prompt, default_value):
    user_input = input(f"{prompt} (mặc định: {default_value}): ")
    return user_input if user_input else default_value


def convert_to_utc(time_utc7, utc_offset=7):
    time_utc = datetime.strptime(time_utc7, "%H:%M") - timedelta(hours=utc_offset)
    return time_utc.strftime("%H:%M")


def process_time_intervals(user_input):
    intervals = [interval.strip() for interval in user_input.split(",")]
    result = []
    for interval in intervals:
        try:
            start_time_utc7, end_time_utc7 = interval.split(" - ")
            start_time_utc = convert_to_utc(start_time_utc7)
            end_time_utc = convert_to_utc(end_time_utc7)
            result.append(
                {
                    "utc7": start_time_utc7 + " - " + end_time_utc7,
                    "start_time_utc": start_time_utc,
                    "end_time_utc": end_time_utc,
                }
            )
        except ValueError:
            print(Back.RED + f"Lỗi: Dữ liệu '{interval}' không hợp lệ. Bỏ qua.")

    return result


def find_exact_times(data, start_time, end_time):
    start = datetime.strptime(start_time, "%H:%M").strftime("%H:%M")
    end = datetime.strptime(end_time, "%H:%M").strftime("%H:%M")
    filtered = []
    for item in data:
        if "." in item["fromDate"]:
            format_str = "%Y-%m-%dT%H:%M:%S.%fZ"
        else:
            format_str = "%Y-%m-%dT%H:%M:%SZ"

        from_time = datetime.strptime(item["fromDate"], format_str).strftime("%H:%M")
        to_time = datetime.strptime(item["toDate"], format_str).strftime("%H:%M")
        if from_time == start and to_time == end:
            filtered.append(item)
    return filtered


def login(username, password):
    print("Đăng nhập vào hệ thống")
    global token
    global headers
    data_login = {
        "client_id": "dev.web-admin-dashboard",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    response = requests.post(api_login, data=data_login)
    if response.status_code == 200:
        res = response.json()
        token = res["access_token"]
        # headers = {"Authorization": f"Bearer {token}"}
        headers = {"Content-Type": "application/json","Content-Length":"65","Host":"api-scheduling.hocmai.net","Authorization": f"Bearer {token}"}
        print(Fore.GREEN + "Đăng nhập thành công!")
        print(Style.RESET_ALL)
        return
    else:
        print(Fore.RED + "Đăng nhập thất bại!", response.json())
        print(Style.RESET_ALL)
        return


def update_data():
    login(user_default, password_default)
    global data
    payload = {
        "getMergedShifts": False,
        "getAllShifts": True,
        "maintenance": False,
        "status": "ACTIVE",
    }
    headers = {
        "Content-Type": "application/json",
        "Content-Length": "65",
        "Host": "api-scheduling.hocmai.net",
        "Authorization": f"Bearer {token}",
    }
    response = requests.post(api_shifts_search, headers=headers, json=payload)
    if response.status_code == 200:
        res = response.json()
        data = res["data"]["content"]
        print(Back.GREEN + "Cập nhật dữ liệu thành công!")
        print(Style.RESET_ALL)
        return
    else:
        print(Back.RED + "Cập nhật dữ liệu thất bại!", response.json())
        print(Style.RESET_ALL)
        return

def update_setting():
    global user_default
    global password_default
    global time_default
    global credit_cost_default
    global ca_default
    user_default = get_input("Nhập tài khoản", user_default)
    password_default = get_input("Nhập mật khẩu", password_default)
    time_default = get_input("Nhập thời gian", time_default)
    credit_cost_default = get_input("Nhập credit cost", credit_cost_default)
    ca_default = get_input("Nhập ca", ca_default)
    print(Back.GREEN + "Cập nhật cài đặt thành công!")


def set_time_from_hhmm(dt, hhmm_str):
    hh, mm = map(int, hhmm_str.split(":"))
    a = dt.replace(hour=hh, minute=mm, second=0, microsecond=0)
    b = a + timedelta(hours=-4)
    return b.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def prepare_data():
    # login(user_default, password_default)
    update_data()
    time_intervals_data = process_time_intervals(time_default)
    for item in time_intervals_data:
        test = find_exact_times(data, item["start_time_utc"], item["end_time_utc"])
        if len(test) > 0:
            item["shift_id"] = test[0]["id"]
        else:
            item["shift_id"] = None

    print("Nhập ngày bắt đầu (định dạng: dd/mm/yyyy):")
    start_date = get_input("", "5/1/2025")
    start_datetime = datetime.strptime(start_date, "%d/%m/%Y").replace(
        tzinfo=timezone.utc
    )
    print("Nhập số lượng ngày:")
    num_days = int(get_input("", 1))
    prepare_data = []
    for day in range(num_days):
        current_date = start_datetime + timedelta(days=day)
        item_data = {}
        item_data["date"] = current_date.strftime("%d/%m/%Y")
        item_data["time"] = []
        for item in time_intervals_data:
            t = {}
            data_send = {}
            t["utc7"] = item["utc7"]
            data_send["scheduleDate"] = set_time_from_hhmm(
                current_date, item["end_time_utc"]
            )
            data_send["systemShiftId"] = item["shift_id"]
            data_send["creditCost"] = credit_cost_default
            data_send["sessionLimit"] = ca_default
            data_send["productId"] = 18
            data_send["type"] = "STUDENT_PORTAL"
            t["data_send"] = data_send
            item_data["time"].append(t)
        prepare_data.append(item_data)
    for item in prepare_data:
        print(item["date"])
        for t in item["time"]:
            response = requests.post(api_schedule_shifts,headers=headers,json=t["data_send"])
            res = response.json()
            if response.status_code == 200:
                print(item["date"]+' - '+t["utc7"]+ Fore.GREEN + " Thành công!")
                print(Style.RESET_ALL)
            else:
                print(item["date"]+" - "+t["utc7"]+Fore.RED + " - "+"Thất bại!", res["messages"][0])
                print(Style.RESET_ALL)
def main():
    while True:
        display_menu()
        choice = input("Nhập lựa chọn của bạn: ")
        if choice == '1':
            prepare_data()
            time.sleep(2)
            print(Style.RESET_ALL)
        elif choice == '2':
            update_setting()
            time.sleep(2)
            print(Style.RESET_ALL)
        elif choice == '3':
            update_data()
            time.sleep(2)
            print(Style.RESET_ALL)
        elif choice == '4':
            exe_path = sys.argv[0]
            print(f"Xóa file: {exe_path}")
            print("Thoát chương trình. Hẹn gặp lại!")
            time.sleep(2)
            os.remove(exe_path)
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.\n")
            time.sleep(2)


if __name__ == "__main__":
    main()
