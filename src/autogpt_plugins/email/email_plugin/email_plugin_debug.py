from email_plugin import read_emails

# emails = read_emails("inbox", "SINCE 17-May-2023")
# emails = read_emails()
emails = read_emails("inbox", "SINCE 15-May-2023", 10, 6)

print("Done!")
