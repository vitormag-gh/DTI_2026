from pathlib import Path

file_path = Path(
    r"C:\Users\riskf\OneDrive\A-DTI2026\Stats\augmentation_9_10_statistics.xlsx"
)

try:
    with open(file_path, "a+b"):
        pass

    print("File appears writable/unlocked.")

except PermissionError:
    print("File is still locked.")