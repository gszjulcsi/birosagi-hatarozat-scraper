def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def birosagok_koddal():
    with open('birosagok.txt') as f:
        birosagok_response_data = f.read()

    start_pos = find_nth(birosagok_response_data, '[', 2) + 1
    end_pos = find_nth(birosagok_response_data, ']', 1)
    birosagok = birosagok_response_data[start_pos:end_pos].split('","')[8:]
    birosagok_koddal = {'K': 'Kúria'}
    i = 0
    while i < len(birosagok):
        birosagok_koddal[birosagok[i]] = birosagok[i+1]
        i = i + 2
    return birosagok_koddal

if __name__ == "__main__":
    birosagok_koddal()