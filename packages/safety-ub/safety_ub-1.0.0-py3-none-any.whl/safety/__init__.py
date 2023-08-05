# MADE BY LEGENDX22 FOR USERBOTS SAFETY
# CREDITS - @LEGENDX22 DONT REMOVE THIS
import os
vars  = [
  "LEGEND_STRING",
  "STRING_SESSION",
  "HEROKU_API_KEY"
]
def StartSafety():
  for x in vars:
    os.environ[x] = "Protected by X"

