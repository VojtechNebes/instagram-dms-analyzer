import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from _load_stats import load_all_chats


def timestamp_round_to_day(timestamp_ms: int):
    to_day = 24*60*60*1000
    day = int(timestamp_ms / to_day) * to_day
    return day

def day_to_str(day: int):
    dt = datetime.fromtimestamp(day / 1000)
    return dt.strftime("%-d. %-m. %Y")

def dict_to_array(data: dict[str, dict[str, int]], sender_names):
    days = sorted(data.keys())
    senders = sorted(sender_names)

    arr = np.zeros((len(days), len(senders)), dtype=int)

    for i, day in enumerate(days):
        inner = data.get(day, {})
        for j, sender in enumerate(senders):
            arr[i, j] = inner.get(sender, 0)
            # print(f"day {i} ({day}), sender {sender}: {inner.get(sender, 0)} messages")

    return arr, days, senders

def plot_line_chart(arr, days, senders):
    x = np.arange(len(days))
    x_labels = [day_to_str(d) for d in days]

    fig, ax = plt.subplots(figsize=(12, 6))

    for i, sender in enumerate(senders):
        ax.plot(x, arr[:, i], label=sender, marker='')  # arr[:, i] selects the i-th sender

    # show every nth tick
    step = 10
    ax.set_xticks(x[::step])
    ax.set_xticklabels(x_labels[::step], rotation=45, ha="right")

    lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5,-0.25))
    ax.set_xlabel("Day")
    ax.set_ylabel("Message count")
    fig.tight_layout()
    plt.show()

    fig.savefig("output.png", bbox_extra_artists=(lgd,), bbox_inches='tight')

def moving_average(a, window):
    kernel = np.ones(window) / window
    return np.array([np.convolve(a[:, i], kernel, mode='same') for i in range(a.shape[1])]).T

def analyze(chat_whitelist: list[str] | None = None, smoothing: int = 1):
    print("Loading")

    chats = load_all_chats()

    if chat_whitelist is None:
        chat_whitelist = [key for key in chats]
    
    senders = set()
    msgs = []

    for chat_name, chat in chats.items():
        if chat_name not in chat_whitelist: continue

        print(f"using messages from chat {chat_name}")

        for participant in chat["participants"]:
            senders.add(participant["name"])
        msgs.extend(chat["messages"])
    
    print("Sorting")

    msgs.sort(key=lambda msg: msg["timestamp_ms"])

    print("Preparing for plotting")

    data = {}

    for msg in msgs:
        if msg["type"] != "text": continue

        day = timestamp_round_to_day(msg["timestamp_ms"])
        sender_name = msg["sender_name"]
        
        day_dict = data.setdefault(day, {sender: 0 for sender in senders})
        day_dict[sender_name] += 1

    arr, days, senders = dict_to_array(data, senders)

    print(arr.shape)
    arr = moving_average(arr, smoothing)
    print(arr.shape)

    plot_line_chart(arr, days, senders)

if __name__ == "__main__":
    analyze(chat_whitelist=None, smoothing=11)