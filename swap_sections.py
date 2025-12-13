
lines = []
with open('index.html', 'r') as f:
    lines = f.readlines()

# 1-based indexing to 0-based
# Section 1: What is 1 Pyeong Merit-Making?
# <div class="bg-white/80 ..."> (Line 800) to </div> (Line 820)
sec1_start = 800 - 1
sec1_end = 820 - 1

# Section 2: Participation Guide
# <div class="bg-amber-50/80 ..."> (Line 825) to </div> (Line 892)
sec2_start = 825 - 1
sec2_end = 892 - 1

# Extract blocks
block1 = lines[sec1_start : sec1_end + 1]
block2 = lines[sec2_start : sec2_end + 1]

# Construct new list
new_lines = []

# Before Section 1
new_lines.extend(lines[:sec1_start])

# Insert Section 2 (Participation Guide)
new_lines.extend(block2)

# Space between sections (lines 821-824 in original)
# We can just add a few newlines or copy the existing ones if we want to preserve exact spacing.
# Let's just add a couple of newlines for clean separation.
new_lines.append('\n\n\n')

# Insert Section 1 (What is 1 Pyeong Merit-Making?)
new_lines.extend(block1)

# After Section 2
new_lines.extend(lines[sec2_end + 1:])

with open('index.html', 'w') as f:
    f.writelines(new_lines)

print(f"Swapped Section 1 ({sec1_start+1}-{sec1_end+1}) and Section 2 ({sec2_start+1}-{sec2_end+1})")
