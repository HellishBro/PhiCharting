import os
os.environ["RUST_BACKTRACE"] = "full"
os.system(os.environ["phira"] if "phira" in os.environ else input("Enter Phira path: "))