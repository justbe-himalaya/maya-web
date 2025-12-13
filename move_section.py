
lines = []
with open('index.html', 'r') as f:
    lines = f.readlines()

# 1-based indexing to 0-based
start_idx = 915 - 1
end_idx = 1105 - 1
insert_idx = 732 - 1

# Extract the block (inclusive)
# end_idx + 1 because slice is exclusive at the end
block = lines[start_idx : end_idx + 1]

# Remove the block
# We need to be careful about indices shifting.
# It's better to pop from the end or construct a new list.

# Let's construct a new list
new_lines = []

# Part 1: Before insertion point
new_lines.extend(lines[:insert_idx])

# Part 2: The block
new_lines.extend(block)
new_lines.append('\n') # Add a newline for spacing if needed

# Part 3: From insertion point to start of block
new_lines.extend(lines[insert_idx : start_idx])

# Part 4: After the block
new_lines.extend(lines[end_idx + 1:])

with open('index.html', 'w') as f:
    f.writelines(new_lines)

print(f"Moved lines {start_idx+1}-{end_idx+1} to before line {insert_idx+1}")
