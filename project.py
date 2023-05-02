import psutil
import json
import time
import pynvml

# number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

print("-----------------------------------------------------")

# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {svmem.total/(1024*1024):.2f} MB")
print(f"Available: {svmem.available/(1024*1024):.2f} MB")
print(f"Used: {svmem.used/(1024*1024):.2f} MB")
print(f"Percentage: {svmem.percent}%")

# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {swap.total/(1024*1024):.2f} MB")
print(f"Free: {swap.free/(1024*1024):.2f} MB")
print(f"Used: {swap.used/(1024*1024):.2f} MB")
print(f"Percentage: {swap.percent}%")

print("-----------------------------------------------------")

# Disk Information
print("Disk Information")
print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"\t Device: {partition.device} \t")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {partition_usage.total/(1024*1024):.2f} MB")
    print(f"  Used: {partition_usage.used/(1024*1024):.2f} MB")
    print(f"  Free: {partition_usage.free/(1024*1024):.2f} MB")
    print(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {disk_io.read_bytes/(1024*1024):.2f} MB")
print(f"Total write: {disk_io.write_bytes/(1024*1024):.2f} MB")

print("-----------------------------------------------------------------")


pynvml.nvmlInit()

# تعداد کارت‌های گرافیکی موجود را به‌دست می‌آوریم
device_count = pynvml.nvmlDeviceGetCount()

# برای هر کارت گرافیکی
for i in range(device_count):
    # اطلاعات کارت گرافیکی را به‌دست می‌آوریم
    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
    info = pynvml.nvmlDeviceGetName(handle)

    # میزان حافظه‌ی استفاده شده و کلی کارت گرافیکی را به‌دست می‌آوریم
    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    used_memory = memory_info.used / (1024 ** 2)
    total_memory = memory_info.total / (1024 ** 2)

    # بار پردازشی کارت گرافیکی را به‌دست می‌آوریم
    utilization_rates = pynvml.nvmlDeviceGetUtilizationRates(handle)
    gpu_utilization = utilization_rates.gpu


    print(f'دستگاه {i}: {info}')
    print(f'used memory: {used_memory:.2f} MiB')
    print(f'total memory: {total_memory:.2f} MiB')
    print(f'بار پردازشی: {gpu_utilization}%')


pynvml.nvmlShutdown()



print("-----------------------------------------------------------------")

# یک تابع برای نمایش بار هر یک از منابع سیستم
def get_system_load():
    # دریافت درصد استفاده از CPU
    cpu_percent = psutil.cpu_percent(interval=1)

    # دریافت درصد استفاده از RAM
    memory_percent = psutil.virtual_memory().percent

    # دریافت درصد استفاده از هارد
    disk_percent = psutil.disk_usage('/').percent



    return cpu_percent, memory_percent, disk_percent


# تنظیمات تمرین
sample_interval = 5  # نمونه‌گیری هر 5 ثانیه
total_samples = 10  # تعداد کل نمونه‌ها

# لیستی از دیکشنری‌ها برای ذخیره نتایج هر نمونه‌گیری
results = []

# شروع نمونه‌گیری ها
for i in range(total_samples):
    # دریافت بار هر یک از منابع سیستم
    cpu_percent, memory_percent, disk_percent = get_system_load()

    # ایجاد دیکشنری برای ذخیره نتیجه نمونه‌گیری
    result = {
        'sample_number': i + 1,
        'cpu_percent': cpu_percent,
        'memory_percent': memory_percent,
        'disk_percent': disk_percent
    }

    # اضافه کردن نتیجه به لیست نتایج
    results.append(result)

    # توقف برای مدت زمان مشخص شده برای نمونه‌گیری
    time.sleep(sample_interval)

# ذخیره نتایج در فایل JSON
with open('system_load.json', 'w') as f:
    json.dump(results, f, indent=4)