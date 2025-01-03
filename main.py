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
data = []


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
        headers = {
            "Content-Type": "application/json",
            "Content-Length": "65",
            "Host": "api-scheduling.hocmai.net",
            "Authorization": f"Bearer {token}",
        }
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
            response = requests.post(
                api_schedule_shifts, headers=headers, json=t["data_send"]
            )
            res = response.json()
            if response.status_code == 200:
                print(item["date"] + " - " + t["utc7"] + Fore.GREEN + " Thành công!")
                print(Style.RESET_ALL)
            else:
                print(
                    item["date"] + " - " + t["utc7"] + Fore.RED + " - " + "Thất bại!",
                    res["messages"][0],
                )
                print(Style.RESET_ALL)


def main():
    while True:
        display_menu()
        choice = input("Nhập lựa chọn của bạn: ")
        if choice == "1":
            prepare_data()
            time.sleep(2)
            print(Style.RESET_ALL)
        elif choice == "2":
            update_setting()
            time.sleep(2)
            print(Style.RESET_ALL)
        elif choice == "3":
            update_data()
            time.sleep(2)
            print(Style.RESET_ALL)
        elif choice == "4":
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
