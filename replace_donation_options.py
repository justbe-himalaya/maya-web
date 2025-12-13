
lines = []
with open('index.html', 'r') as f:
    lines = f.readlines()

# Find the start and end of the block
start_line = -1
end_line = -1

for i, line in enumerate(lines):
    if '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">' in line:
        start_line = i
        # The block ends when the div count balances or we find the next known element.
        # In this specific case, we know the structure.
        # It ends before <ul class="space-y-4 text-gray-700">
        break

if start_line != -1:
    for i in range(start_line, len(lines)):
        if '<ul class="space-y-4 text-gray-700">' in lines[i]:
            end_line = i
            break

if start_line != -1 and end_line != -1:
    # New content
    new_content = """                                <div class="mb-6">
                                    <h4 class="text-lg font-serif font-bold text-gray-800 mb-3 text-center" data-kr="1구좌 (1평)" data-en="1 Share (1 Pyeong)">1구좌 (1평)</h4>
                                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                        <!-- Option 1: One-time -->
                                        <div class="bg-white p-5 rounded-xl border border-amber-100 shadow-sm hover:shadow-md transition-shadow text-center">
                                            <h5 class="font-bold text-amber-800 mb-2 text-lg" data-kr="일시불" data-en="Lump Sum">일시불</h5>
                                            <p class="text-gray-700 font-medium" data-kr="100만원" data-en="1 Million KRW">100만원</p>
                                        </div>

                                        <!-- Option 2: Installment -->
                                        <div class="bg-white p-5 rounded-xl border border-amber-100 shadow-sm hover:shadow-md transition-shadow text-center">
                                            <h5 class="font-bold text-green-800 mb-2 text-lg" data-kr="분납" data-en="Installment">분납</h5>
                                            <p class="text-gray-700 text-sm" data-kr="월 3만원 × 36개월" data-en="30,000 KRW/mo × 36 mos">월 3만원 × 36개월</p>
                                            <p class="text-gray-500 text-xs mt-1" data-kr="(총 108만원)" data-en="(Total 1.08 Million KRW)">(총 108만원)</p>
                                        </div>
                                    </div>
                                </div>
"""
    # Replace
    new_lines = lines[:start_line] + [new_content] + lines[end_line:]
    
    with open('index.html', 'w') as f:
        f.writelines(new_lines)
    print(f"Replaced block from line {start_line+1} to {end_line}")
else:
    print("Could not find the block to replace.")
