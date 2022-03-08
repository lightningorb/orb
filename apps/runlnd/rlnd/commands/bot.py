# from invoke import task
# import telegram
# import json
# import os

# token = (
#     open(f"{os.path.join(os.path.dirname(__file__), '..', '..', '.tg_token')}")
#     .read()
#     .strip()
# )
# bot = telegram.Bot(token=token)


# @task
# def balance_alert(c, env=dict(PATH=os.environ["PATH"])):
#     chat_id = None
#     chans = json.loads(c.run("lncli listchannels", hide=True, env=env).stdout)
#     t = 0.1
#     for ch in chans["channels"]:
#         lb, rb, ca = (
#             int(ch["local_balance"]),
#             int(ch["remote_balance"]),
#             int(ch["capacity"]),
#         )
#         if lb / ca < t or rb / ca < t:
#             alias = json.loads(
#                 c.run(
#                     f'lncli getnodeinfo {ch["remote_pubkey"]}', hide=True, env=env
#                 ).stdout
#             )["node"]["alias"]
#             print("-" * 100)
#             msg = f"'{alias}' has {round(min(rb / ca, lb / ca) * 100, 2)}% {('in', 'out')[rb / ca < t]}bound remaining"
#             print(msg)
#             updates = bot.get_updates()
#             if updates:
#                 chat_id = updates[0].message.from_user.id
#             if chat_id:
#                 bot.send_message(
#                     text=msg,
#                     chat_id=chat_id,
#                 )
