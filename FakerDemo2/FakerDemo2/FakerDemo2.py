from faker import Faker
import random
import json

def generate_fake_data(num_records):
    fake = Faker()
    data = []

    # Rastgele kullanıcı adları oluştur
    usernames = [fake.user_name() for _ in range(30000)]

    # Belirlenen ilgi alanları
    interest_areas = ["Technology", "Basketball", "Food", "Travel", "Music", "Fashion", "Books", "Fitness", "Movie", "Dance", "Football", "Astronomy", "Hiking", "Ancient Architecture", "Yoga"]

    for _ in range(num_records):
        # Kullanıcı adı
        username = random.choice(usernames)
        usernames.remove(username)  # Kullanılan adı listeden çıkar

        # Ad ve soyad
        full_name = fake.name()

        # Takipçi sayısı ve takip edilen sayısı
        followers_count = random.randint(0, min(100, len(usernames)))
        following_count = random.randint(0, min(100, len(usernames)))

        # Dil ve bölge
        language = fake.language_name()
        region = fake.country()

        # Tweet içerikleri
        num_tweets = random.randint(1, min(30, random.randint(1, 30)))
        tweets = [fake.text() + f" {random.choice(interest_areas)}" for _ in range(num_tweets)]

        # Takip edilen ve takipçi listeleri oluştur
        followers = random.sample(usernames, followers_count)
        following = random.sample(usernames, following_count)

        # Kendi kullanıcı adını çıkar
        if username in followers:
            followers.remove(username)
        if username in following:
            following.remove(username)

        user_data = {
            "username": username,
            "name": full_name,
            "followers_count": followers_count,
            "following_count": following_count,
            "language": language,
            "region": region,
            "tweets": tweets,
            "following": following,
            "followers": followers
        }
        data.append(user_data)

    with open('fakeData1.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    num_records = 30000
    generate_fake_data(num_records)
