import json
import os
import re


def sort_extract_number(s):
    match = re.search(r'\d+', s)
    return int(match.group()) if match else float('inf')

def build_statistics(inbox_dir):
    chats = os.listdir(inbox_dir)

    for chat in chats:
        chat_path = os.path.join(inbox_dir, chat)

        # gather all msg files

        msg_files = [msg_file for msg_file in os.listdir(chat_path) if msg_file.endswith(".json") and not os.path.isdir(os.path.join(chat_path, msg_file))]
        msg_files.sort(key=sort_extract_number)

        print(f"{len(msg_files)} msg files with {chat}")
        # print(msg_files)

        # merge all msg files

        with open(os.path.join(chat_path, msg_files.pop(0)), "rt") as first_msg_file:
            output_chat_json = json.load(first_msg_file)
        
        for msg_file_path in msg_files:
            with open(os.path.join(chat_path, msg_file_path), "rt") as msg_file:
                msgs = json.load(msg_file)
                output_chat_json["messages"].extend(msgs["messages"])
        
        # remove unnecessary fields and add some other

        for message in output_chat_json["messages"]:
            try:
                del message["is_geoblocked_for_viewer"]
                del message["is_unsent_image_by_messenger_kid_parent"]
            except KeyError:
                pass

            try:
                if "photos" in message or "videos" in message:
                    message["type"] = "media"
                elif "call_duration" in message:
                    message["type"] = "call"
                elif "share" in message:
                    if message["share"]["link"].startswith("https://www.instagram.com/reel/"):
                        message["type"] = "reel"
                    elif message["share"]["link"].startswith("https://www.instagram.com/p/"):
                        message["type"] = "post"
                    else:
                        message["type"] = "share"
                elif "content" not in message:
                    message["type"] = "unknown"
                else:
                    message["type"] = "text"
            except KeyError:
                message["type"] = "unknown"

        # write formatted chat json to file

        output_path = os.path.join("statistics", chat, "message.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wt") as output_file:
            chars_written = output_file.write(
                json.dumps(output_chat_json, ensure_ascii=False, indent=4)
            )
            print(f"Wrote {chars_written/1024:.1f}kB for chat {chat}")
            

if __name__ == "__main__":
    build_statistics("your_instagram_activity/messages/inbox")