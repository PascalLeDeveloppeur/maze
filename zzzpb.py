# ll = ["un", "deux", "trois", "quatre", "cinq", "treize", "quinze"]
# for i, elt in enumerate(ll):
#     if "tr" in elt:
#         del ll[i]
# print(ll)


ll = ["un", "deux", "trois", "quatre", "cinq", "treize", "quinze"]
rewind = 0
for i in range(0, len(ll)):
    print(i)
    item = ll[i]
    if "trois" in item:
        ll[i] = None
ll.remove(None)
print(ll)
