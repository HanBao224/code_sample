import database
import compago

app = compago.Application()

# command line driver would be:
# python3.6 shazam.py init_database "MUSIC/"
# python3.6 shazam.py identify "MUSIC/test_12s.wav"

@app.command
def init_database(path):
    database.init_db()
    database.build_tables(path)
    return True

@app.command
def identify(path):
    hash_input = database.get_all_fingerprint()
    query_table = database.hashing(hash_input)
    info, dis = database.query_hash_nearest(path, query_table)
    print(info)

@app.command
def insert_new_song(path):
    database.insert_new_songs(path)

@app.command
def insert_new_info(info_list, col_name):
    database.insert_new_info(info_list, col_name)


if __name__ == "__main__":
    app.run()
