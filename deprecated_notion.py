from notion.client import NotionClient

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2=token_v2)

# Replace this URL with the URL of the page you want to edit
page = client.get_block("https://www.notion.so/myorg/Test-c0d20a71c0944985ae96e661ccc99821")
url = "https://www.notion.so/5496d5344c624ef5abd665008e354edf?v=0d20a700785747cc8ded03167a61e42e"
url = "https://www.notion.so/14a0eda608be4da284229fe06491ecb7?v=53daff4c831a489f915dab78e92b7a6c"
url = "https://www.notion.so/14a0eda608be4da284229fe06491ecb7?v=c58ff66a861c4128aab3b1b10182fd19"
url = "https://www.notion.so/14a0eda608be4da284229fe06491ecb7?v=c58ff66a861c4128aab3b1b10182fd19&p=1415fec98e114594b127810bfd18f031&pm=s"
page = client.get_block(url)
print("The old title is:", page.title)

# Note: You can use Markdown! We convert on-the-fly to Notion's internal formatted text data structure.
page.title = "Board Games List"

cv = client.get_collection_view(url)
client.
cv.name
for row in cv.collection.get_rows():
    print("We estimate the value of '{}' at {}".format(row.name, row.estimated_value))

new_game = cv.collection.add_row()
new_game.name = 'Test'
new_game.bgg_id = 0
new_game.bgg_url = "https://boardgamegeek.com/boardgame/209010/mechs-vs-minions"


game_id ="1415fec98e114594b127810bfd18f031"
record_data = client.get_record_data(cv, id="1415fec98e114594b127810bfd18f031")
record_data = client.get_record_data(url, id="1415fec98e114594b127810bfd18f031")
client.get_block("https://www.notion.so/14a0eda608be4da284229fe06491ecb7?v=c58ff66a861c4128aab3b1b10182fd19&p=1415fec98e114594b127810bfd18f031&pm=s")


