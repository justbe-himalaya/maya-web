
lines = []
with open('index.html', 'r') as f:
    lines = f.readlines()

# 1. Remove the existing "mb-6" block (lines ~808-824 in previous view)
# We look for <div class="mb-6"> and the corresponding closing div before the <ul>
start_remove = -1
end_remove = -1

for i, line in enumerate(lines):
    if '<div class="mb-6">' in line and '1구좌 (1평)' in lines[i+1]: # Verify it's the right block
        start_remove = i
        break

if start_remove != -1:
    # Find the end. It should be before <ul class="space-y-4
    for i in range(start_remove, len(lines)):
        if '<ul class="space-y-4 text-gray-700">' in lines[i]:
            end_remove = i - 1 # The line before the UL
            break

# 2. Construct the new LI content
new_li_content = """                                    <li class="flex items-start">
                                        <span class="text-amber-600 mr-2 font-bold">•</span>
                                        <div class="w-full">
                                            <strong class="text-gray-900 text-lg" data-kr="1구좌 (1평):" data-en="1 Share (1 Pyeong):">1구좌 (1평):</strong>
                                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-3 mb-2">
                                                <!-- Option 1: One-time -->
                                                <div class="bg-white p-4 rounded-xl border border-amber-100 shadow-sm hover:shadow-md transition-shadow text-center">
                                                    <span class="inline-block bg-amber-100 text-amber-800 font-bold px-3 py-1 rounded-full mb-2 text-sm" data-kr="일시불" data-en="Lump Sum">일시불</span>
                                                    <p class="text-amber-700 font-bold text-lg" data-kr="100만원" data-en="1 Million KRW">100만원</p>
                                                </div>

                                                <!-- Option 2: Installment -->
                                                <div class="bg-white p-4 rounded-xl border border-amber-100 shadow-sm hover:shadow-md transition-shadow text-center">
                                                    <span class="inline-block bg-green-100 text-green-800 font-bold px-3 py-1 rounded-full mb-2 text-sm" data-kr="분납" data-en="Installment">분납</span>
                                                    <p class="text-gray-700 font-medium" data-kr="월 3만원 × 36개월" data-en="30,000 KRW/mo × 36 mos">월 3만원 × 36개월</p>
                                                    <p class="text-gray-400 text-xs mt-1" data-kr="(총 108만원)" data-en="(Total 1.08 Million KRW)">(총 108만원)</p>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
"""

# 3. Apply changes
if start_remove != -1 and end_remove != -1:
    # Remove the block
    # lines[start_remove : end_remove+1] are removed.
    # We also need to insert the new_li_content INSIDE the <ul>.
    # The <ul> starts at end_remove + 1 (in original indices)
    
    ul_index = end_remove + 1
    # Check if lines[ul_index] is indeed the UL
    if '<ul class="space-y-4 text-gray-700">' in lines[ul_index]:
        # We want to insert after the <ul> tag
        # So we keep lines[:start_remove], skip the removed block, keep the <ul> tag, then insert new_li, then the rest.
        
        new_lines = lines[:start_remove] + [lines[ul_index]] + [new_li_content] + lines[ul_index+1:]
        
        with open('index.html', 'w') as f:
            f.writelines(new_lines)
        print("Successfully restructured donation options.")
    else:
        print("Error: Could not find UL tag at expected position.")
else:
    print("Error: Could not find the block to remove.")
