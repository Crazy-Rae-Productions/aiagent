from functions.get_file_content import get_file_content

test1 = get_file_content("calculator", "lorem.txt")

test2 = get_file_content("calculator", "main.py")

test3 = get_file_content("calculator", "pkg/calculator.py")

test4 = get_file_content("calculator", "/bin/cat")

test5 = get_file_content("calculator", "pkg/does_not_exist.py")

print(f"lorem.txt length: {len(test1)}")
print(f"lorem.txt truncated: {'truncated' in test1}")

print(test2)
print(test3)
print(test4)
print(test5)