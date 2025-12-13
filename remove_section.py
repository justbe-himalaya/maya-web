
lines = []
with open('index.html', 'r') as f:
    lines = f.readlines()

# 1-based indexing to 0-based
# Remove lines 871 to 891
start_idx = 871 - 1
end_idx = 891 - 1

# Keep lines before start_idx and after end_idx
new_lines = lines[:start_idx] + lines[end_idx + 1:]

with open('index.html', 'w') as f:
    f.writelines(new_lines)

print(f"Removed lines {start_idx+1} to {end_idx+1}")
