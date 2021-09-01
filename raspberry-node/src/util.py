
DEBUG_MODE = False

def print_tmp(msg_str_seg_list, msg_variable_seg_list):
    
    if not DEBUG_MODE:
        return

    if len(msg_str_seg_list) != len(msg_variable_seg_list):
        return
    
    for i in range(0, len(msg_str_seg_list)):
        try:
            var1 = msg_str_seg_list[i]
        except:
            var1 = ""
        try:
            var2 = msg_variable_seg_list[i]
        except:
            var2 = ""

        print("tmp__" + msg_str_seg_list[i] + " " + str(msg_variable_seg_list[i]) + " ")


def print_cmd_status_2(cmd_title, cmd_name, new_val_name_1, new_val_1, new_val_name_2, new_val_2):
    print("[" + cmd_title + "] " + cmd_name)
    print("... " + new_val_name_1 + ": " + str(new_val_1) + ", " + new_val_name_2 + ": " + str(new_val_2))


def print_cmd_status_1(cmd_title, cmd_name, new_val_name, new_val):
    print("[" + cmd_title + "] " + cmd_name)
    print("... " + new_val_name + ": " + str(new_val))