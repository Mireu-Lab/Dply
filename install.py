status = input("Do you specify GPU assignment values? (A / Y / N) : ")

import tensorflow as tf
gpu = len(tf.config.experimental.list_physical_devices("GPU"))

if status == "A" or status == "a":
    gpu = len(tf.config.experimental.list_physical_devices("GPU"))

elif status == "Y" or status == "y":
    while True:
        gpuInput = int(input("\n\nPlease specify the number of GPU assignments (0 is considered None): ")) - 1

        if gpu < gpuInput:
            print("You have specified more than the number of hardware GPUs.")
        else:
            gpu = gpuInput
            break
else:
    gpu = 0

with open("env/.env", "w", encoding="utf8") as env:
    env.write(f"""GPUSetting {gpu}""")
