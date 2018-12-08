from pycord.client import Client

client = Client(">>")
client.load_extensions([
    "test_extension.TestExtension"
])
client.run()

# client = pycord.client.client.Client("!")
#
# emoji = pycord.models.Emoji(client, {
# "id": "41771983429993937",
#   "name": "LUL",
#   "roles": [ "41771983429993000", "41771983429993111" ],
#   "user": {
#     "username": "Luigi",
#     "discriminator": "0002",
#     "id": "96008815106887111",
#     "avatar": "5500909a3274e1812beb4e8de6631111"
#   },
#   "require_colons": True,
#   "managed": False,
#   "animated": False
# })
