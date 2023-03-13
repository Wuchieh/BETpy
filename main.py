import threading
import time
import random

# 定義的肉的類型和數量
meat = {'牛肉': 10, '豬肉': 7, '雞肉': 5}
num_workers = 5

# 定義互斥鎖
lock = threading.Lock()


# 定義員工類別
class Worker(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global meat
        while True:
            # 過濾調已經沒有剩餘的肉類
            remaining_meat = {k: v for k, v in meat.items() if v > 0}
            # 檢查是否所有肉類都已經被處理完畢 若是就結束執行緒
            if not remaining_meat:
                break
            # 任選一種剩餘肉類
            meat_type = random.choice(list(remaining_meat.keys()))
            # 互斥鎖進入鎖住狀態
            lock.acquire()
            if meat[meat_type] > 0:
                # 如果有剩餘肉 拿一份
                meat[meat_type] -= 1
                # 互斥鎖釋放
                lock.release()
                print(f"{self.name} 在 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 取得{meat_type}")
                # 處理肉類的時間
                time.sleep(1 if meat_type == '牛肉' else 2 if meat_type == '豬肉' else 3)
                print(f"{self.name} 在 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 處理完{meat_type}")
            else:
                # 如果沒有剩餘肉類，釋放互斥鎖
                lock.release()
                break


# 建立員工執行緒
workers = [Worker(chr(i + 65)) for i in range(num_workers)]

# 啟動員工執行緒
for worker in workers:
    worker.start()

# 等待所有員工執行緒執行完畢
for worker in workers:
    worker.join()

print("肉類都處理完畢")
