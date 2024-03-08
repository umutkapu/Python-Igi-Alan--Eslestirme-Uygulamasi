import json
import networkx as nx
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

class Node:
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next_node = next_node

class SimpleHashMap:
    def __init__(self, capacity=16):
        self.buckets = [None] * capacity
        self.size = 0

    def get_bucket_index(self, key):
        hash_code = hash(key)
        return hash_code % len(self.buckets)

    def put(self, key, value):
        bucket_index = self.get_bucket_index(key)

        # Eğer bu bucket boşsa yeni bir giriş oluştur
        if self.buckets[bucket_index] is None:
            self.buckets[bucket_index] = Node(key, value)
            self.size += 1
            return

        # Eğer bu bucket doluysa, zinciri kontrol et ve ekle veya güncelle
        current = self.buckets[bucket_index]
        while current is not None:
            if current.key == key:
                current.value = value  # Anahtar zaten varsa güncelle
                return
            current = current.next_node

        # Zincir sonuna yeni bir giriş ekle
        new_entry = Node(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_entry
        self.size += 1

    def get(self, key):
        bucket_index = self.get_bucket_index(key)
        current = self.buckets[bucket_index]

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next_node

        return None  # Anahtar bulunamadı

    def size(self):
        return self.size

    def values(self):
        values_list = []
        for entry in self.buckets:
            while entry is not None:
                values_list.append(entry.value)
                entry = entry.next_node

        return values_list

# JSON dosyasını açın ve verileri okuyun
with open('C:\\Users\\umutk\\Dropbox\\PC\\Desktop\\fakeData1.json', 'r') as dosya:
    veriler = json.load(dosya)

# SimpleHashMap örneği oluşturun
hashmap = SimpleHashMap()

# İlk 1000 kullanıcının tweets özelliğindeki en çok geçen kelimeyi bulun ve hashmap'e ekleyin
for kullanici in veriler[:1000]:
    username = kullanici['username']
    tweets = kullanici['tweets']

    # Anlamlı kelimelere ayırma ve en çok geçen kelimeyi bulma
    all_tweets = ' '.join(tweets)
    tokenized_tweets = word_tokenize(all_tweets.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tweets = [word for word in tokenized_tweets if word.isalpha() and word not in stop_words]

    # Frekans dağılımını oluşturma
    freq_dist = FreqDist(filtered_tweets)

    # En çok geçen kelimeyi bulma
    most_common_word = freq_dist.max()

    # Hashmap'e ekleyin
    hashmap.put(username, most_common_word)

# Hashmap içeriğini yazdırın
print("Hashmap İçeriği:")
for entry in hashmap.buckets:
    while entry is not None:
        print(f"Key: {entry.key}, Value: {entry.value}")
        entry = entry.next_node
        print("\n")

# Grafı oluştur
graf_most_common_words = nx.Graph()

# Hashmap içeriğini kullanarak grafı oluşturun
for entry1 in hashmap.buckets:
    while entry1 is not None:
        for entry2 in hashmap.buckets:
            while entry2 is not None:
                if entry1.key != entry2.key and entry1.value == entry2.value:
                    # Birbirleriyle bağlantı kurmuş kullanıcıları ekleyin
                    graf_most_common_words.add_edge(entry1.key, entry2.value)
                entry2 = entry2.next_node
        entry1 = entry1.next_node

# Grafığı çiz
plt.figure(figsize=(8, 8))
pos = nx.spring_layout(graf_most_common_words)
nx.draw(graf_most_common_words, pos, with_labels=True, font_weight='bold')
plt.title("İlk 10 Kullanıcının Ortak En Çok Geçen Kelimeleri Arasındaki Bağlantılar")
plt.show()
